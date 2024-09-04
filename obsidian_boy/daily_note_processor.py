from typing import List, Optional
from dataclasses import dataclass, field
from langchain.chat_models.base import BaseChatModel
from langchain.schema import HumanMessage
import json
import logging

@dataclass
class Entry:
    title: Optional[str] = None
    link: Optional[str] = None
    description: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    todo: Optional[str] = None

class DailyNoteProcessor:
    def __init__(self, llm: BaseChatModel):
        self.llm = llm
        self.logger = logging.getLogger(__name__)

    def extract_entries(self, note_content: str) -> List[Entry]:
        """
        Extract entries from a daily note using an LLM.

        Args:
            note_content (str): The content of the daily note.

        Returns:
            List[Entry]: A list of extracted entries.
        """
        prompt = f"""
        Extract entries from the following daily note content. Each entry should have at least a title or a link, and may include a description, tags, and an optional todo item.
        Format the output as a JSON list of objects, where each object represents an entry with the following structure:
        {{
            "title": "Entry title (optional)",
            "link": "URL or markdown link (optional)",
            "description": "Brief description of the entry (optional)",
            "tags": ["tag1", "tag2", ...] (optional, default to empty list),
            "todo": "Optional todo item (null if not present)"
        }}
        Omit any fields that are not present in the entry.

        Daily note content:
        {note_content}

        JSON output:
        """

        try:
            response = self.llm.predict_messages([HumanMessage(content=prompt)])
            entries_data = json.loads(response.content)
            return [Entry(**{k: v for k, v in entry.items() if v is not None}) for entry in entries_data]
        except json.JSONDecodeError:
            self.logger.error("Error: LLM response is not valid JSON")
            return []
        except Exception as e:
            self.logger.error(f"Error processing daily note: {str(e)}")
            return []
