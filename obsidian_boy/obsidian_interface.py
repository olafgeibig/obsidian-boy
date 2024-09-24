from pathlib import Path
from typing import List
from .types import Note

class ObsidianInterface:
    def __init__(self, vault_path: Path):
        self.VAULT_PATH = vault_path
        self.NEW_NOTE_DIR = self.VAULT_PATH / "ObsidianBoy/New"
        self.REVISION_DIR = self.VAULT_PATH / "ObsidianBoy/Revision"
        self.NOTE_DIR = self.VAULT_PATH / "ObsidianBoy/Notes"
        self.DAILY_NOTE_DIR = self.VAULT_PATH / "Daily"

    def list_daily_notes(self) -> List[Path]:
        """
        List daily notes sorted by date.

        Returns:
            List[Path]: A list of paths to daily notes, sorted by date (newest first).
        """
        daily_notes = list(self.DAILY_NOTE_DIR.glob("*.md"))
        return sorted(daily_notes, key=lambda x: x.stem, reverse=True)

    def read_daily_note(self, dailynote: Path) -> str:
        """
        Read the contents of a daily note.

        Args:
            dailynote (Path): The path to the daily note.

        Returns:
            str: The contents of the daily note.
        """
        return dailynote.read_text(encoding="utf-8")

    def create_note(self, note: Note) -> None:
        """
        Create a new note in the NEW_NOTE_DIR.

        Args:
            note (Note): The Note object containing the note's information.
        """
        note_path = self.NEW_NOTE_DIR / f"{note.location.stem}.md"
        note_path.write_text(note.content, encoding="utf-8")
        note.location = note_path

    def update_note(self, note: Note, content: str) -> None:
        """
        Update an existing note with new content.

        Args:
            note (Note): The Note object to be updated.
            content (str): The new content for the note.
        """
        note.location.write_text(content, encoding="utf-8")

    def move_note(self, note: Note, dir: Path) -> None:
        """
        Move a note to a new directory within the Obsidian vault.

        Args:
            note (Note): The Note object to be moved.
            dir (Path): The directory to move the note to.
        """
        new_location = dir / note.location.name
        note.location.rename(new_location)
        note.location = new_location

    def get_existing_tags(self) -> List[str]:
        """
        Retrieve existing tags from all notes in the vault.

        Returns:
            List[str]: A list of unique tags found in the vault.
        """
        tags = set()
        for note in self.VAULT_PATH.glob("**/*.md"):
            content = note.read_text(encoding="utf-8")
            tags.update(tag.strip("#") for tag in content.split() if tag.startswith("#"))
        return sorted(tags)
