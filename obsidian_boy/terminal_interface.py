from typing import List
from pathlib import Path
from .obsidian_interface import ObsidianInterface

class TerminalInterface:
    def __init__(self, fs_interface: ObsidianInterface):
        self.fs_interface = fs_interface

    def display_menu(self) -> None:
        """
        Display the main menu options.
        """
        print("\nObsidianBoy Menu:")
        print("1. List daily notes")
        print("2. Select daily notes")
        print("3. Exit")

    def get_user_input(self, prompt: str) -> str:
        """
        Get user input with a given prompt.

        Args:
            prompt (str): The prompt to display to the user.

        Returns:
            str: The user's input.
        """
        return input(prompt)

    def show_daily_notes(self) -> None:
        """
        Display a list of daily notes.
        """
        notes = self.fs_interface.list_daily_notes()
        print("\nDaily Notes:")
        for i, note in enumerate(notes, 1):
            print(f"{i}. {note.stem}")

    def select_daily_notes(self) -> List[Path]:
        """
        Allow the user to select daily notes from a list.

        Returns:
            List[Path]: A list of selected note paths.
        """
        notes = self.fs_interface.list_daily_notes()
        self.show_daily_notes()
        selected_indices = self.get_user_input("Enter the numbers of the notes you want to select (comma-separated): ")
        selected_indices = [int(idx.strip()) for idx in selected_indices.split(',') if idx.strip().isdigit()]
        
        selected_notes = []
        for idx in selected_indices:
            if 1 <= idx <= len(notes):
                selected_notes.append(notes[idx - 1])
            else:
                print(f"Invalid selection: {idx}. Skipping.")
        
        return selected_notes
