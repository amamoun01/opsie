from fastapi import APIRouter, status


router = APIRouter(tags=["Observability"])


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """Health checkendpoint."""
    return {"status": "UP", "services": {"llm_gateway": "UP", "database": "N/A"}}
