# ObsidianBoy Project Plan

## Project Overview
An AI-powered assistant (ObsidianBoy) that automates the process of managing knowledge in Obsidian. The goal is to transform daily note entries into compreghensive notes with full explanation and links to relevant resources. There are templates for different note types with hints how the template shall be filled. The solution will allow users to select daily notes to process, completes missing information of the daily note entries, perform research on daily note entries, create new discrete notes for each entry, tag them based on existing tags. There shall be a human review loop before finalizing changes. In the first iteration the interface will be terminal-based.

Obsidian background:
Obsidian is a note taking app that stores the notes as markdown files in a vault. In Obsidian daily notes are like bookmarks of ideas or inspirations used to capture findings or ideas. Usually daily notes contain a title, a link to relevant resources and a description, probably also tags and a task to remind the user on further exploration. Distilled notes are covering a bigger topic with more depth and are usually linking to related detailled notes.

## Envisoned Workflow
```plantuml
@startuml
start
:Parse a daily note into entries;
repeat: Create a new note for an entry;
  :Fill the missing fields of the entries.
  Do research when needed.;
  :Choose a note template that matches the entry;
  :Write the note according to the template. 
  Do research when needed.;
  :Tag the note according to existing tags;
repeat while (entries)
repeat :Human reviews a note;
  switch (Note review is?)
  case (approved)
    :Move note to note dir;
  case (rejected)
    :Take the human feedback;
    :Send to the note writer agent for correction;
  case (revision)
    :Take the human reason;
    :Move note to revision dir;
  endswitch  
repeat while (Notes in temp dir?) is (yes)
end
@enduml
```
- The terminal based interface allows the user to list and select daily notes to be processed.
- Fill the missing fields:
   1. Generate a title based on the description and the tags. If this is not possible, use the contents of the linked website
   2. Find the link to main website by searching the web based on the title, description and tags.
   3. Create a description based on the contents of the linked website
- The note writer inspects the assigned template and researches the knowledge needed to fill the note template using the research tools. Valuable researched knowledge is stored in the knowledge base and then writes the note based on the template using the researched knowledge.

## Tools and Types
This a UML model for the tools and types. The types are sterotyped with <<Pydantic>>. 

```plantuml
@startuml

class Note <<Pydantic>> {
  +Path: location
  +str: type
}
enum NoteStatus <<Pydantic>> {
  APPROVED
  REJECTED
  REVISION_NEEDED
}
class DailyNoteEntry <<Pydantic>> {
  +str: title
  +str: link
  +str: description
  +List[str]: tags
  +str: todo
}
class NoteReview <<Pydantic>> {
  +Note: note
  +NoteStatus: result
  +str: feedback
}
class Template <<Pydantic>> {
  +str: name
  +Path: location
  +str: description
}
class TerminalInterface {
  +show_menu()
  +show_daily_notes()
  +Path: select_daily_note()
  +NoteReview: review_note(Note note)
}
class ObsidianInterface {
  - VAULT_PATH
  - NEW_NOTE_DIR
  - REVISION_DIR
  - NOTE_DIR
  - DAILY_NOTE_DIR
  +List[Path]: list_daily_notes()
  +str: read_daily_note(Path: dailynote)
  +create_note(note: Note)
  +update_note(note: Note, content : str)
  +move_note(Note note, dir: Path)
  +List[str]: get_existing_tags()
}
class DailyNoteTools {
  +List[DailyNoteEntry]: extract_entries()
}
class NoteTemplateTools {
  - Path: NOTE_TEMPLATE_DIR
  +List[Template]: get_templates()
  +str: get_template(template_name: str)
}
class ResearchTools {
  +str: web_search(query: str)
  +str: ai_search(query: str)
  +str: knowledgebase(question: str)
}
class WebScraper {
  +str: scrape(url: str)
}
abstract class KnowledgeBase {
  {abstract} +add(key: str, value: str)
  {abstract} +delete(key: str)
  {abstract} +str: ask(question: str)
}
class FileSystemKnowledgeBase {
  +add(key: str, value: str)
  +delete(key: str)
  +str: ask(question: str)
}
KnowledgeBase <|-- FileSystemKnowledgeBase
@enduml
```
### Details
#### ObsidianInterface
Handles all interactions with the Obsidian vault file system. It provides methods to deal with daily notes, notes and the tags existing in the Obsidian vault. The Note object contains their location so that they can be accessed in the file system. The directory they are stored in reflects the status of a not. If it is in the NEW_NOTE_DIR it is a new note. If it is in the REVISION_DIR it is a note that needs manual revision by the user. If it is in the NOTE_DIR it is a note that is approved by the user.
#### TerminalInterface
Provides a terminal-based interface for interacting with the ObsidianBoy system. It allows users to select daily notes, review notes. The note review displays the note content and allows the user to approve, reject, or request revision of the note. The rejection and revision request shall include a reason for the rejection or revision request entered by the user.
#### DailyNoteTools
Provides methods for extracting entries from a daily note.
#### NoteTemplateTools
Provides methods for listing and getting note templates.
#### ResearchTools
Provides methods for web search, AI search, and knowledgebase search. 
- The web search performs a web search using a query and the result ususally conatains a list of websites and their descriptions. This is good to find websites related to a daily note or note. An agent can identify relevant results and then use the web scraper to get the content.
- The AI search is an AI based search tool which is expensive to use. It provides a refined result based on its own research. This is good if not much is known about the topic of a note. It might be useful to scrape the content of the links in the result to get more details.
- The knowledgebase question is a tool that answers question against a knowledge base related to a note. This is good if previous research about the note already collected a lot of knowleddge that had been stored in the knowledge base and can hereby be searched in the context of this note. You can see it as a searchable research cache. 
#### WebScraper
Responsible for scraping content from web resources to markdown. 
#### KnowledgeBase
Abstract base class for knowledge storage and retrieval. It adds knowledge related to a given key. The delete function deletes all knowledge related to key. The ask function answers questions against the knowledge base of a given key.
#### FileSystemKnowledgeBase
Concrete implementation of KnowledgeBase that stores the knowledge in the file system. The stored knowledge for a key will be loaded into the context of a cheap LLM to answer the question.

## Solution
The solution shall be implemented in Python with LangChain and LangGraph. The tools shall be implemented in descrete classes according to the UML model. An ObsidianBoy class shall contain the implementation of the workflow in LangGraph. Simple LangGraph nodes and nodes with agents. Both can use the provided tools. The code shall be put into the obsidian_boy module and tests go into the tests dir.

To be cost effective the solution shall utilize 3 different capable LLMs: 
- A simple and fast model to summarize texts, extract data from text, and perform simple tasks.
- A medium model for avaerage agentic tasks
- A smart model to perform complex tasks, planning and reasoning.

## Types and Templates
### The daily note entry type
```python
class DailyNoteEntry(BaseModel):
    title: Optional[str] = Field(description="Entry title (optional)")
    link: Optional[str] = Field(description="URL or markdown link (optional)")
    description: Optional[str] = Field(description="Brief description of the entry (optional)")
    tags: List[str] = Field(default_factory=list, description="List of tags (optional, default to empty list)")
    todo: Optional[str] = Field(default=None, description="Optional todo item (null if not present)")
```
Important fields that should be fileld if missing: title, link, description

### Note template example
LLM hints for the content are in {{}}
tech-tool.md
```
---
created: {current date}
updated: {current date}
type: tech-tool
tags: {{tags}}
description: {{short description of the tech-tool}}
---
# Description
{{long description of the tech-tool}}
## Concepts
{{explanation of the concepts used by the tech-tool}}
## Usages
{{explanation of the usages of the tech-tool}}
# Resources
## Official
{{bulleted list of links to official resources: the project main website, source code, webapp, documentation, research papers}}
## Know-How
{{bulleted list of links to know-how resources: articles, courses, blog-posts, medium, substack, YouTube, podcasts, linkedin}}
```