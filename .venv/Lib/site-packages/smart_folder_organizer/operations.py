"""
operations.py

Core file organization functions for Smart Folder Organizer.
"""

from pathlib import Path
from shutil import move
from typing import Dict, List


FILE_CATEGORIES = {
    "Images": [
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".bmp",
        ".webp",
        ".svg",
        ".tiff",
    ],
    "Documents": [
        ".doc",
        ".docx",
        ".odt",
        ".txt",
        ".rtf",
    ],
    "PDF": [
        ".pdf",
    ],
    "Spreadsheets": [
        ".xls",
        ".xlsx",
        ".csv",
        ".ods",
    ],
    "Presentations": [
        ".ppt",
        ".pptx",
        ".odp",
    ],
    "Videos": [
        ".mp4",
        ".avi",
        ".mkv",
        ".mov",
        ".wmv",
        ".webm",
    ],
    "Audio": [
        ".mp3",
        ".wav",
        ".flac",
        ".aac",
        ".ogg",
        ".m4a",
    ],
    "Archives": [
        ".zip",
        ".rar",
        ".7z",
        ".tar",
        ".gz",
    ],
    "Code": [
        ".py",
        ".js",
        ".ts",
        ".java",
        ".cpp",
        ".c",
        ".h",
        ".html",
        ".css",
        ".sql",
    ],
}


def get_category(file_path: Path) -> str:
    """
    Determine the category of a file based on its extension.

    Args:
        file_path: Path to the file.

    Returns:
        The category name.
    """

    extension = file_path.suffix.lower()

    for category, extensions in FILE_CATEGORIES.items():
        if extension in extensions:
            return category

    return "Others"


def get_unique_destination(destination: Path) -> Path:
    """
    Prevent overwriting an existing file.

    If example.pdf already exists, the new file becomes:
    example (1).pdf
    example (2).pdf
    etc.
    """

    if not destination.exists():
        return destination

    counter = 1

    while True:
        new_name = (
            f"{destination.stem} ({counter})"
            f"{destination.suffix}"
        )

        new_destination = destination.parent / new_name

        if not new_destination.exists():
            return new_destination

        counter += 1


def organize_folder(
    folder: str,
    dry_run: bool = False
) -> Dict[str, List[str]]:
    """
    Organize files inside a folder into category folders.

    Args:
        folder: Folder that should be organized.
        dry_run: If True, show what would happen without moving files.

    Returns:
        Dictionary containing files organized by category.
    """

    source_folder = Path(folder).expanduser().resolve()

    if not source_folder.exists():
        raise FileNotFoundError(
            f"Folder does not exist: {source_folder}"
        )

    if not source_folder.is_dir():
        raise NotADirectoryError(
            f"Not a directory: {source_folder}"
        )

    organized = {}

    for file_path in source_folder.iterdir():

        # Ignore directories
        if not file_path.is_file():
            continue

        category = get_category(file_path)

        destination_folder = source_folder / category
        destination = destination_folder / file_path.name

        destination = get_unique_destination(destination)

        organized.setdefault(category, []).append(file_path.name)

        if dry_run:
            print(
                f"[DRY RUN] {file_path.name} "
                f"-> {category}/{destination.name}"
            )
        else:
            destination_folder.mkdir(
                parents=True,
                exist_ok=True
            )

            move(str(file_path), str(destination))

            print(
                f"Moved: {file_path.name} "
                f"-> {category}/{destination.name}"
            )

    return organized