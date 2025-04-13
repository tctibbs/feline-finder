"""File system image repository."""

from pathlib import Path

from loguru import logger
from PIL import Image

from source.cat import Cat

from .. import CatImageRepository


class FilesystemImageRepository(CatImageRepository):
    """
    Saves cat images as PNGs on the local filesystem.
    """

    def __init__(self, base_dir: Path) -> None:
        self.base_dir = base_dir
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def save_images(self, cat: Cat, images: list[Image.Image]) -> None:
        if not images:
            logger.warning(f"No images provided for {cat.name}.")
            return

        # Create subdirectory: e.g., "Yoplait_15988"
        safe_name = cat.name.replace(" ", "_")
        cat_folder = self.base_dir / f"{safe_name}_{cat.cat_id}"
        cat_folder.mkdir(parents=True, exist_ok=True)

        for idx, img in enumerate(images):
            try:
                filename = f"{idx + 1}.png"
                filepath = cat_folder / filename
                img.save(filepath)
                logger.debug(f"Saved image to: {filepath}")
            except OSError as e:
                logger.error(f"Failed to save image {idx} for {cat.name}: {e}")
