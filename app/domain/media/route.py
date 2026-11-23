from io import BytesIO
from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile, status
from fastapi.responses import FileResponse

from core.media import MediaService, get_media_service

router = APIRouter(prefix="/media", tags=["Media"])


def _absolute_media_url(request: Request, relative_url: str) -> str:
    """Build an absolute URL on this same API app for stored media links."""
    if relative_url.startswith("http://") or relative_url.startswith("https://"):
        return relative_url
    base = str(request.base_url).rstrip("/")
    path = relative_url if relative_url.startswith("/") else f"/{relative_url}"
    return f"{base}{path}"


@router.post(
    "/upload",
    status_code=status.HTTP_201_CREATED,
    summary="Upload a media file",
)
async def upload_media(
    request: Request,
    file: UploadFile = File(...),
    folder: str = Form("uploads"),
    media: MediaService = Depends(get_media_service),
):
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename is required",
        )

    try:
        content = await file.read()
        result = await media.upload(
            BytesIO(content),
            filename=file.filename,
            content_type=file.content_type,
            folder=folder or "uploads",
        )
        result["url"] = _absolute_media_url(request, result["url"])
    except NotImplementedError as exc:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Upload failed: {exc}",
        ) from exc
    finally:
        await file.close()

    return result


@router.get(
    "/files/{file_key:path}",
    summary="Get a media file by storage key",
)
async def get_media_file(
    file_key: str,
    media: MediaService = Depends(get_media_service),
):
    try:
        path = media.resolve_path(file_key)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except NotImplementedError as exc:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail=str(exc),
        ) from exc

    if not path.exists() or not path.is_file():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media file not found",
        )

    return FileResponse(
        path,
        filename=Path(path).name,
        content_disposition_type="inline",
    )
