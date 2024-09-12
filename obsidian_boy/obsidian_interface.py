from pathlib import Path
from typing import List
import shutil

class ObsidianInterface:
    def __init__(self, vault_path: Path, temp_dir: Path):
        self.vault_path = vault_path
        self.temp_dir = temp_dir

    def list_daily_notes(self) -> List[Path]:
        """
        List daily notes sorted by date.

        Returns:
            List[Path]: A list of paths to daily notes, sorted by date (newest first).
        """
        daily_notes_dir = self.vault_path / "Daily"
        daily_notes = list(daily_notes_dir.glob("*.md"))
        return sorted(daily_notes, key=lambda x: x.stem, reverse=True)

    def read_daily_note(self, note_path: Path) -> str:
        """
        Read the contents of a daily note.

        Args:
            note_path (Path): The path to the daily note.

        Returns:
            str: The contents of the daily note.
        """
        return note_path.read_text(encoding="utf-8")

    def create_temp_note(self, note_name: str, content: str) -> Path:
        """
        Create a new note in the temporary directory.

        Args:
            note_name (str): The name of the new note (without extension).
            content (str): The content of the new note.

        Returns:
            Path: The path to the newly created temporary note.
        """
        temp_note_path = self.temp_dir / f"{note_name}.md"
        temp_note_path.write_text(content, encoding="utf-8")
        return temp_note_path

    def update_note(self, note_path: Path, content: str) -> None:
        """
        Update an existing note with new content.

        Args:
            note_path (Path): The path to the note to be updated.
            content (str): The new content for the note.
        """
        note_path.write_text(content, encoding="utf-8")

    def get_existing_tags(self) -> List[str]:
        """
        Retrieve existing tags from all notes in the vault.

        Returns:
            List[str]: A list of unique tags found in the vault.
        """
        tags = set()
        for note in self.vault_path.glob("**/*.md"):
            content = note.read_text(encoding="utf-8")
            tags.update(tag.strip("#") for tag in content.split() if tag.startswith("#"))
        return sorted(tags)

    def move_temp_to_vault(self, temp_note_path: Path, destination_name: str) -> Path:
        """
        Move a file from the temporary directory to the Obsidian vault.

        Args:
            temp_note_path (Path): The path to the temporary note.
            destination_name (str): The desired name for the note in the vault (without extension).

        Returns:
            Path: The path to the note in the Obsidian vault.
        """
        destination_path = self.vault_path / f"{destination_name}.md"
        shutil.move(temp_note_path, destination_path)
        return destination_path
