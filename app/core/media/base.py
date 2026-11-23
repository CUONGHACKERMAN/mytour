from abc import ABC, abstractmethod
from pathlib import Path
from typing import BinaryIO


class MediaStorage(ABC):
    """Interface for media storage providers."""

    @abstractmethod
    async def upload(
        self,
        file: BinaryIO,
        *,
        filename: str,
        content_type: str | None = None,
        folder: str = "uploads",
    ) -> dict:
        """
        Persist a file and return storage metadata.

        Returns:
            {"key": str, "url": str}
        """

    @abstractmethod
    async def delete(self, key: str) -> None:
        """Delete an object by storage key."""

    @abstractmethod
    def get_public_url(self, key: str) -> str:
        """Build an app-relative public URL path for a storage key."""

    @abstractmethod
    def resolve_path(self, key: str) -> Path:
        """
        Resolve a storage key to a local filesystem path when supported.

        Cloud providers may raise NotImplementedError.
        """
