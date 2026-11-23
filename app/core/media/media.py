from __future__ import annotations

from pathlib import Path
from typing import BinaryIO

from core.config import settings
from .base import MediaStorage
from .local import LocalMediaStorage
from .r2 import R2MediaStorage
from .s3 import S3MediaStorage


class MediaService:
    """Facade that delegates to the configured media storage provider."""

    def __init__(self, storage: MediaStorage | None = None) -> None:
        self._storage = storage or self._build_storage()

    @staticmethod
    def _build_storage() -> MediaStorage:
        provider = (settings.MEDIA_PROVIDER or "local").strip().lower()
        if provider == "local":
            return LocalMediaStorage()
        if provider == "r2":
            return R2MediaStorage(api_key=settings.R2_API_KEY)
        if provider == "s3":
            return S3MediaStorage(api_key=settings.S3_API_KEY)
        raise ValueError(f"Unsupported MEDIA_PROVIDER: {provider}")

    async def upload(
        self,
        file: BinaryIO,
        *,
        filename: str,
        content_type: str | None = None,
        folder: str = "uploads",
    ) -> dict:
        return await self._storage.upload(
            file,
            filename=filename,
            content_type=content_type,
            folder=folder,
        )

    async def delete(self, key: str) -> None:
        await self._storage.delete(key)

    def get_public_url(self, key: str) -> str:
        return self._storage.get_public_url(key)

    def resolve_path(self, key: str) -> Path:
        return self._storage.resolve_path(key)


def get_media_service() -> MediaService:
    return MediaService()
