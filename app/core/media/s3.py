from pathlib import Path
from typing import BinaryIO

from .base import MediaStorage


class S3MediaStorage(MediaStorage):
    """AWS S3 provider stub — not configured in this pass."""

    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key

    async def upload(
        self,
        file: BinaryIO,
        *,
        filename: str,
        content_type: str | None = None,
        folder: str = "uploads",
    ) -> dict:
        raise NotImplementedError(
            "S3 media provider is not configured. Set MEDIA_PROVIDER=local or implement S3 upload."
        )

    async def delete(self, key: str) -> None:
        raise NotImplementedError(
            "S3 media provider is not configured. Set MEDIA_PROVIDER=local or implement S3 delete."
        )

    def get_public_url(self, key: str) -> str:
        raise NotImplementedError(
            "S3 media provider is not configured. Set MEDIA_PROVIDER=local or implement S3 URLs."
        )

    def resolve_path(self, key: str) -> Path:
        raise NotImplementedError(
            "S3 media provider does not expose local filesystem paths."
        )
