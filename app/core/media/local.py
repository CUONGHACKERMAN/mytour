from __future__ import annotations

import asyncio
import re
import uuid
from pathlib import Path
from typing import BinaryIO

from core.config import settings
from .base import MediaStorage

# Served by GET /api/media/files/{key} on the same FastAPI app
API_MEDIA_FILES_PREFIX = "/api/media/files"


def _safe_filename(filename: str) -> str:
    name = Path(filename or "upload.bin").name
    name = re.sub(r"[^A-Za-z0-9._-]", "_", name)
    return name or "upload.bin"


class LocalMediaStorage(MediaStorage):
    def __init__(self, root: str | None = None) -> None:
        self.root = Path(root or settings.MEDIA_ROOT).resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    async def upload(
        self,
        file: BinaryIO,
        *,
        filename: str,
        content_type: str | None = None,
        folder: str = "uploads",
    ) -> dict:
        safe_folder = re.sub(r"[^A-Za-z0-9/_-]", "", folder.strip("/")) or "uploads"
        safe_name = _safe_filename(filename)
        key = f"{safe_folder}/{uuid.uuid4().hex}_{safe_name}"
        destination = self.root / key
        destination.parent.mkdir(parents=True, exist_ok=True)

        data = file.read()

        def _write() -> None:
            destination.write_bytes(data)

        await asyncio.to_thread(_write)
        return {"key": key, "url": self.get_public_url(key)}

    async def delete(self, key: str) -> None:
        path = self.resolve_path(key)

        def _delete() -> None:
            if path.exists() and path.is_file():
                path.unlink()

        await asyncio.to_thread(_delete)

    def get_public_url(self, key: str) -> str:
        return f"{API_MEDIA_FILES_PREFIX}/{key.lstrip('/')}"

    def resolve_path(self, key: str) -> Path:
        normalized = key.lstrip("/").replace("\\", "/")
        if ".." in normalized.split("/"):
            raise ValueError("Invalid media key")
        candidate = (self.root / normalized).resolve()
        if not str(candidate).startswith(str(self.root)):
            raise ValueError("Invalid media key")
        return candidate
