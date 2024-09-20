from crewai import Crew, Agent, Task
from pydantic import BaseModel, Field
from typing import List, Optional

class DailyNoteEntry(BaseModel):
    title: Optional[str] = Field(description="Entry title (optional)")
    link: Optional[str] = Field(description="URL or markdown link (optional)")
    description: Optional[str] = Field(description="Brief description of the entry (optional)")
    tags: List[str] = Field(default_factory=list, description="List of tags (optional, default to empty list)")
    todo: Optional[str] = Field(default=None, description="Optional todo item (null if not present)")

class DailyNoteResponse(BaseModel):
    entries: List[DailyNoteEntry]

class NoteCrew:

    def extract_entries(self, note_content: str) -> DailyNoteResponse:
        note_agent = Agent(
            role='Daily note processor',
            goal='Parse daily notes',
            backstory='I am a champ.',
            verbose=True,
            llm="gpt-4o-mini",
            allow_delegation=False,
            tools=[]
        )

        note_task = Task(
            description=f"""
    Extract entries from the following daily note content. Each entry should have at least a title or a link, and may include a description, tags, and an optional todo item.                                                                                                                                                                                                                                                                       on with the extracted entries.
    Daily note content:
    {note_content}
            """,
            agent=note_agent,
            expected_output="Parsed daily notes",
            output_pydantic=DailyNoteResponse,
        )    
        crew = Crew(
            agents=[note_agent],
            tasks=[note_task],
            verbose=True
        )
        crew_output = crew.kickoff()
        return note_task.output.pydantic
