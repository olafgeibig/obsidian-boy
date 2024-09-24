from pydantic import BaseModel, Field
from pathlib import Path
from typing import List, Optional
from enum import Enum

class Note(BaseModel):
    location: Path = Field(..., description="The file path of the note within the Obsidian vault")
    type: str = Field(..., description="The type of the note (e.g., 'tech-tool', 'concept', etc.)")

class NoteStatus(str, Enum):
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    REVISION_NEEDED = "REVISION_NEEDED"

class DailyNoteEntry(BaseModel):
    title: Optional[str] = Field(None, description="The title of the daily note entry")
    link: Optional[str] = Field(None, description="URL link related to the entry")
    description: Optional[str] = Field(None, description="Brief description of the entry")
    tags: List[str] = Field(default_factory=list, description="List of tags associated with the entry")
    todo: Optional[str] = Field(None, description="Optional todo item related to the entry")

class NoteReview(BaseModel):
    note: Note = Field(..., description="The note being reviewed")
    result: NoteStatus = Field(..., description="The result of the review (APPROVED, REJECTED, or REVISION_NEEDED)")
    feedback: str = Field(..., description="Feedback or comments from the reviewer")

class Template(BaseModel):
    name: str = Field(..., description="The name of the template")
    location: Path = Field(..., description="The file path of the template")
    description: str = Field(..., description="A brief description of the template's purpose or content")

class ProcessedNote(BaseModel):
    original_entry: DailyNoteEntry = Field(..., description="The original daily note entry that was processed")
    note: Note = Field(..., description="The resulting note created from the daily note entry")
    content: str = Field(..., description="The full content of the processed note")
