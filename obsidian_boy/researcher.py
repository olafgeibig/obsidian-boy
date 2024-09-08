from abc import ABC, abstractmethod
from typing import List
from obsidian_boy.daily_note_processor import DailyNoteEntry

class Researcher(ABC):
    """
    Abstract base class for researchers that perform research on entries.
    """

    @abstractmethod
    def research_entry(self, entries: List[DailyNoteEntry]) -> dict:
        """
        Abstract method to perform research on a list of entries.

        :param entries: The list of DailyNoteEntry objects to perform research on.
        :return: A dictionary containing the research results.
        """
        pass
