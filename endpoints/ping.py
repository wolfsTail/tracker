from fastapi import APIRouter


router = APIRouter(prefix="/ping", tags=["ping",])


@router.get("/app")
async def check_app() -> dict[str, str]:
    return {
        "mesage": "application -> ok!",
    }


@router.get("/database")
async def check_db() -> dict[str, str]:
    return {
        "mesage": "database -> ok!",
    }