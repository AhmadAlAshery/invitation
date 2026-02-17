from fastapi import APIRouter, Depends, Request, Query, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session


from src.core.session import get_db

from src.auth.service import AuthService
from src.auth.schema import (
    Token,
    HostCreate,
    HostResponse,
)

from src.auth.repository import get_current_host
from src.auth.model import Host


router = APIRouter()
auth_service = AuthService()


@router.post("/login", response_model=Token)
async def login(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    """Login endpoint"""
    return auth_service.login(db, form_data.username, form_data.password)


@router.post("/register", response_model=HostResponse)
async def register(
    request: Request,
    host_data: HostCreate,
    db: Session = Depends(get_db),
):
    """Host registration endpoint - requires API key"""
    full_url = str(request.url).rstrip("/").replace("/register", "")
    return auth_service.register(db, host_data, full_url)


@router.get(
    "/validate-token",
    responses={
        400: {"description": "Host inactive"},
        401: {"description": "Invalid, expired, or missing token"},
    },
)
async def validate_api_token(current_host: Host = Depends(get_current_host)):
    """
    Validates the host's access token.

    It checks:
    1.  The token's signature and expiration using `decode_access_token`.
    2.  If the host associated with the token's 'sub' claim (host ID)
        still exists in the database and is active.

    Returns 200 OK if the token is valid and the host is active.
    Raises 401 Unauthorized if the token is invalid/expired/missing, or host not found.
    Raises 400 Bad Request if the host is found but inactive.
    """
    return {"message": "Token is valid"}


@router.get(
    "/get_host",
    responses={
        401: {"description": "Unauthorized - Invalid, expired, or missing token"},
        404: {"description": "Host not found"},
    },
)
async def get_hosts(
    db: Session = Depends(get_db),
    current_host: Host = Depends(get_current_host),
):
    """Login endpoint"""
    return auth_service.get_all_hosts(db, current_host.email)


@router.get(
    "/activate_host",
    responses={
        401: {"description": "Unauthorized - Invalid, expired, or missing token"},
        404: {"description": "Host not found"},
    },
)
async def activate_host(
    db: Session = Depends(get_db),
    current_host: Host = Depends(get_current_host),
    host_email=Query(str, description="The host email that needs activation."),
):
    """Login endpoint"""
    return auth_service.activate_host(db, host_email)


@router.post("/process-invitation-file")
async def process_invitation_file(
    db: Session = Depends(get_db),
    current_host: Host = Depends(get_current_host),
    invitation_name: str = Query(..., description="Invitation name"),
    file: UploadFile = File(...),
):
    """
    Upload an Excel file, add column 'x',
    save it inside src/excel, and return it.
    """

    # Ensure parent directory exists
    return await auth_service.generate_images(db, file, invitation_name)


@router.get("/excel_files")
async def list_files(
    current_host: Host = Depends(get_current_host),
):
    base_path = Path("src") / "excel"

    if not base_path.exists() or not base_path.is_dir():
        raise HTTPException(status_code=404, detail="Folder not found")

    files = [f.name for f in base_path.iterdir() if f.is_file()]

    return {"files": files}


@router.get("/images_folders")
async def list_folders(
    current_host: Host = Depends(get_current_host),
):
    base_path = Path("src") / "images"

    if not base_path.exists() or not base_path.is_dir():
        raise HTTPException(status_code=404, detail="Folder not found")

    folders = [f.name for f in base_path.iterdir() if f.is_dir()]

    return {"folders": folders}


@router.get("/images_files/{id}")
async def list_images(
    id: str | int,
    current_host: Host = Depends(get_current_host),
):
    base_path = Path("src") / f"images/{id}"

    if not base_path.exists() or not base_path.is_dir():
        raise HTTPException(status_code=404, detail="Folder not found")

    images = [f.name for f in base_path.iterdir() if f.is_file()]

    return {"images": images}


@router.get("/image_file/{id}")
async def get_image(
    id: str | int,
    img_name: str | int,
    current_host: Host = Depends(get_current_host),
):
    img_path = Path("src") / f"images/{id}/{img_name}"
    return FileResponse(
        path=img_path,
        filename="".join(str(img_path.name).split("_")[:-1]) + ".png",
        media_type="image/png",
    )


@router.get("/excel_file/{id}")
async def get_excel(
    excel_name: str | int,
    current_host: Host = Depends(get_current_host),
):
    excel_path = Path("src") / f"excel/{excel_name}"
    return FileResponse(
        path=excel_path,
        filename=excel_path.name,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
