import logging
import os
import sys

import discord
import httpx
from discord.ext import commands


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("opsie.bot")

TOKEN = os.getenv("DISCORD_TOKEN")
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000/v1/chat")

if not TOKEN:
    logger.critical(
        "Initialization Failure: DISCORD_TOKEN environment variable is missing."
    )
    sys.exit(1)

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

async_http_client = httpx.AsyncClient(timeout=45.0)

CHANNEL_MODEL_MAPPING = {}
VALID_ALIASES = {"gpt": "openai/gpt-4o-mini", "gemini": "gemini/gemini-2.5-flash"}


@bot.event
async def on_ready():
    logger.info(
        f"Opsie Bot connection established successfully. Operational as: {bot.user}"
    )
    await bot.change_presence(activity=discord.CustomActivity(name="Ready to help 🤖"))


@bot.command(name="setmodel")
async def set_model(ctx, model_alias: str.lower):
    """Dynamically updates the active AI model configuration."""
    if model_alias in VALID_ALIASES:
        target_model = VALID_ALIASES[model_alias]
        CHANNEL_MODEL_MAPPING[ctx.channel.id] = target_model
        await ctx.reply(
            f"🎯 Channel infrastructure routed to execute model: `{target_model}`"
        )
    else:
        allowed = ", ".join([f"`{k}`" for k in VALID_ALIASES.keys()])
        await ctx.reply(f"❌ Unknown model alias. Supported environments: {allowed}")


@bot.event
async def on_message(message: discord.Message):
    await bot.process_commands(message)

    if message.author == bot.user or message.content.startswith("!"):
        return

    is_dm = message.guild is None

    is_targeted_ping = bot.user in message.mentions

    if not (is_dm or is_targeted_ping):
        return

    cleaned_prompt = message.content
    for mention_string in (f"<@{bot.user.id}>", f"<@!{bot.user.id}>"):
        cleaned_prompt = cleaned_prompt.replace(mention_string, "")
    cleaned_prompt = cleaned_prompt.strip()

    if not cleaned_prompt:
        return

    channel_override_model = CHANNEL_MODEL_MAPPING.get(message.channel.id, None)

    async with message.channel.typing():
        try:
            payload = {
                "message": cleaned_prompt,
                "model_override": channel_override_model,
            }

            response = await async_http_client.post(
                BACKEND_URL, json=payload, timeout=60.0
            )

            if response.status_code == 200:
                data = response.json()
                ai_response = data.get("response", "")
                engine_used = data.get("model_used", "unknown")

                final_text = f"{ai_response}\n\n*📊 Core Engine: `{engine_used}`*"

                if len(final_text) <= 2000:
                    await message.reply(final_text)
                else:
                    chunks = [
                        final_text[i : i + 1900]
                        for i in range(0, len(final_text), 1900)
                    ]
                    for chunk in chunks:
                        await message.channel.send(chunk)

            else:
                logger.error(
                    "[Gateway Error] Upstream cluster returned code: "
                    f"{response.status_code}"
                )
                await message.reply(
                    "❌ `[Gateway Error]` "
                    "Failed to receive a valid payload from the internal API cluster."
                )

        except httpx.TimeoutException:
            logger.error("Upstream processing window expired. Timeout limit exceeded.")
            await message.reply(
                "⏳ `[Gateway Timeout]` "
                "The inference cluster took too long to compile an answer."
            )

        except httpx.RequestError as exc:
            logger.error(
                f"Network transport connectivity failure targeting API layer: {exc}"
            )
            await message.reply(
                "⚠️ `[Service Unavailable]` "
                "The Core backend orchestration mesh is currently unreachable."
            )


@bot.event
async def close():
    """Hook into clean-shutdown signals to safely drain socket connection pools."""
    logger.info("Graceful shutdown initiated. Tearing down HTTP connection pools...")
    await async_http_client.aclose()
    await commands.Bot.close(bot)


if __name__ == "__main__":
    bot.run(TOKEN)
