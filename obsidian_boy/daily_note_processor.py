from typing import List
from langchain.chat_models.base import BaseChatModel
import logging
from pydantic import BaseModel
import markdownify
from .types import DailyNoteEntry
# Define the Pydantic model for the daily note entry
# class DailyNoteEntry(BaseModel):
#     title: Optional[str] = Field(description="Entry title (optional)")
#     link: Optional[str] = Field(description="URL or markdown link (optional)")
#     description: Optional[str] = Field(description="Brief description of the entry (optional)")
#     tags: List[str] = Field(default_factory=list, description="List of tags (optional, default to empty list)")
#     todo: Optional[str] = Field(default=None, description="Optional todo item (null if not present)")

class DailyNoteResponse(BaseModel):
    entries: List[DailyNoteEntry]

class DailyNoteProcessor:
    def __init__(self, llm: BaseChatModel):
        self.llm = llm
        self.logger = logging.getLogger(__name__)

    def extract_entries(self, note_content: str) -> List[DailyNoteEntry]:
        """
        Extract entries from a daily note using an LLM.

        Args:
            note_content (str): The content of the daily note.

        Returns:
            List[DailyNoteEntry]: A list of extracted entries.
        """
        # Convert HTML content to Markdown
        note_content = markdownify.markdownify(note_content)

        prompt = f"""
        Extract entries from the following daily note content. Each entry should have at least a title or a link, and may include a description, tags, and an optional todo item.
        Make sure to call the DailyNoteResponse function with the extracted entries.

        Daily note content:
        {note_content}
        """

        try:
            # Create a structured LLM with the Pydantic model
            structured_llm = self.llm.with_structured_output(DailyNoteResponse)
            response = structured_llm.invoke(prompt)
            return response.entries
        except Exception as e:
            self.logger.error(f"Error processing daily note: {str(e)}")
            return []
