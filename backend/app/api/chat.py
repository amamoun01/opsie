import datetime
import logging
from os import getenv

from fastapi import APIRouter, HTTPException, status
from litellm import acompletion
from pydantic import BaseModel, Field


router = APIRouter(prefix="/v1")
logger = logging.getLogger("opsie.backend")

logging.getLogger("LiteLLM").setLevel(logging.WARNING)

OPSIE_SYSTEM_PROMPT = (
    "You are Opsie, a DevOps assistant.\n"
    "Help with CI/CD, infrastructure, containers, cloud platforms, monitoring,\n"
    "and incident response.\n\n"
    "Current date: {current_date}\n\n"
    "Response rules:\n"
    "- Default to 3-6 sentences or a short bullet list. Expand only for\n"
    "  multi-step procedures (e.g. incident runbooks, migrations) — and even\n"
    "  then, use numbered steps, not prose.\n"
    "- Lead with the answer or fix, not background explanation. Add context\n"
    "  only if it changes what the user should do.\n"
    "- Use code blocks for any command, config, or log snippet — never inline.\n"
    "- If a question is ambiguous (e.g. missing platform, version, or\n"
    "  environment), ask one clarifying question instead of guessing.\n"
    "- If you're not confident in a technical detail (version-specific\n"
    "  behavior, exact flag names, recent product changes), say so rather than\n"
    "  presenting it as fact.\n"
    '- No filler ("Great question!", "I\'d be happy to help"). No sign-offs.\n'
    "- Match the channel's tone: casual phrasing, not corporate-speak — but\n"
    "  never sacrifice precision for brevity."
)


class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="The text input sent by the user.",
    )
    model_override: str | None = Field(
        default=None, description="Optional target model chosen via chat UI."
    )


class ChatResponse(BaseModel):
    response: str = Field(
        ..., description="The computed text reply from the AI engine."
    )
    model_used: str = Field(
        ..., description="The exact model identifier that fulfilled the request."
    )


@router.post("/chat", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def chat_with_ai(payload: ChatRequest):
    """
    Ingests message payloads, evaluates model targets, and triggers asynchronous
    inference with an automated high-availability failover policy.
    """
    primary_model = payload.model_override or getenv(
        "OPENAI_MODEL", "gemini/gemini-2.5-flash"
    )

    fallback_chain = ["openai/gpt-4o-mini", "gemini/gemini-2.5-flash"]

    if primary_model in fallback_chain:
        fallback_chain.remove(primary_model)

    current_date = datetime.date.today().strftime("%B %d, %Y")
    try:
        logger.info(
            f"Initiating inference. Primary: {primary_model} | "
            f"Fallbacks configured: {fallback_chain}"
        )

        response = await acompletion(
            model=primary_model,
            fallbacks=fallback_chain,
            messages=[
                {
                    "role": "system",
                    "content": OPSIE_SYSTEM_PROMPT.format(current_date=current_date),
                },
                {"role": "user", "content": payload.message},
            ],
        )

        ai_reply = response.choices[0].message.content
        actual_model = response._hidden_params.get("model", primary_model)

        logger.info(f"Inference complete. Fulfilled by engine: {actual_model}")
        return ChatResponse(response=ai_reply, model_used=actual_model)

    except Exception as exc:
        logger.critical(
            "All configured upstream AI engines in fallback matrix exhausted: "
            f"{str(exc)}"
        )
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=(
                "Upstream AI provider failure or token limit restrictions encountered."
            ),
        ) from exc
