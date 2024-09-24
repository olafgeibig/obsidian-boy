from typing import List, Optional
from pathlib import Path
from .obsidian_interface import ObsidianInterface
from .types import Note, NoteReview, NoteStatus

class TerminalInterface:
    def __init__(self, obsidian_interface: ObsidianInterface):
        self.obsidian_interface = obsidian_interface

    def run(self) -> None:
        """
        Run the main loop of the terminal interface.
        """
        while True:
            self.display_menu()
            choice = self.get_user_input("Enter your choice: ")
            if choice == "1":
                self.list_daily_notes()
            elif choice == "2":
                self.process_daily_notes()
            elif choice == "3":
                self.review_notes()
            elif choice == "4":
                print("Exiting ObsidianBoy. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    def display_menu(self) -> None:
        """
        Display the main menu options.
        """
        print("\nObsidianBoy Menu:")
        print("1. List daily notes")
        print("2. Process daily notes")
        print("3. Review processed notes")
        print("4. Exit")

    def get_user_input(self, prompt: str) -> str:
        """
        Get user input with a given prompt.

        Args:
            prompt (str): The prompt to display to the user.

        Returns:
            str: The user's input.
        """
        return input(prompt)

    def list_daily_notes(self) -> None:
        """
        Display a list of daily notes.
        """
        notes = self.obsidian_interface.list_daily_notes()
        print("\nDaily Notes:")
        for i, note in enumerate(notes, 1):
            print(f"{i}. {note.stem}")

    def process_daily_notes(self) -> None:
        """
        Process selected daily notes.
        """
        selected_notes = self.select_daily_notes()
        if not selected_notes:
            print("No notes selected. Returning to main menu.")
            return

        print(f"Processing {len(selected_notes)} selected notes...")
        # Here you would call the actual processing logic
        # For now, we'll just print a placeholder message
        for note in selected_notes:
            print(f"Processing note: {note.stem}")

        print("Processing complete. Processed notes are ready for review.")

    def select_daily_notes(self) -> List[Path]:
        """
        Allow the user to select daily notes from a list.

        Returns:
            List[Path]: A list of selected note paths.
        """
        notes = self.obsidian_interface.list_daily_notes()
        self.list_daily_notes()
        selected_indices = self.get_user_input("Enter the numbers of the notes you want to select (comma-separated): ")
        selected_indices = [int(idx.strip()) for idx in selected_indices.split(',') if idx.strip().isdigit()]
        
        selected_notes = []
        for idx in selected_indices:
            if 1 <= idx <= len(notes):
                selected_notes.append(notes[idx - 1])
            else:
                print(f"Invalid selection: {idx}. Skipping.")
        
        return selected_notes

    def review_notes(self) -> None:
        """
        Review processed notes.
        """
        # This is a placeholder for the actual review process
        # You would need to implement the logic to fetch processed notes
        processed_notes = self.get_processed_notes()
        
        if not processed_notes:
            print("No processed notes available for review.")
            return

        for note in processed_notes:
            self.display_note_content(note)
            review = self.get_note_review()
            self.handle_review_result(note, review)

    def get_processed_notes(self) -> List[Note]:
        """
        Get the list of processed notes ready for review.
        This is a placeholder and should be implemented based on your system's design.
        """
        # Placeholder implementation
        return []

    def display_note_content(self, note: Note) -> None:
        """
        Display the content of a note for review.
        """
        print(f"\nReviewing note: {note.location.stem}")
        print("Content:")
        print(self.obsidian_interface.read_daily_note(note.location))

    def get_note_review(self) -> NoteReview:
        """
        Get the user's review for a note.
        """
        while True:
            choice = self.get_user_input("Enter your review (A)pprove, (R)eject, or (N)eeds revision: ").upper()
            if choice in ['A', 'R', 'N']:
                status = NoteStatus.APPROVED if choice == 'A' else NoteStatus.REJECTED if choice == 'R' else NoteStatus.REVISION_NEEDED
                feedback = self.get_user_input("Enter any feedback or comments: ")
                return NoteReview(note=Note(location=Path(), type=""), result=status, feedback=feedback)
            else:
                print("Invalid choice. Please enter A, R, or N.")

    def handle_review_result(self, note: Note, review: NoteReview) -> None:
        """
        Handle the result of a note review.
        """
        if review.result == NoteStatus.APPROVED:
            print(f"Note approved. Moving to final location.")
            # Implement logic to move the note to its final location
        elif review.result == NoteStatus.REJECTED:
            print(f"Note rejected. Deleting processed note.")
            # Implement logic to delete the processed note
        else:
            print(f"Note needs revision. Marking for further processing.")
            # Implement logic to mark the note for revision

        print(f"Feedback: {review.feedback}")
