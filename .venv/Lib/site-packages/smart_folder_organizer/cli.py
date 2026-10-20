"""
Command-line interface for Smart Folder Organizer.
"""

import argparse

from .operations import organize_folder


def main():
    parser = argparse.ArgumentParser(
        description="Automatically organize files into folders."
    )

    parser.add_argument(
        "folder",
        help="Folder to organize"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would happen without moving files"
    )

    args = parser.parse_args()

    try:
        organize_folder(
            args.folder,
            dry_run=args.dry_run
        )

        if args.dry_run:
            print("\nDry run complete.")
        else:
            print("\nFolder organization complete.")

    except (FileNotFoundError, NotADirectoryError) as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()