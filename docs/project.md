# ObsidianBoy: Project Plan

## Project Overview

Develop an AI-powered assistant (ObsidianBoy) that automates the process of managing knowledge in Obsidian. The assistant will allow users to select daily notes to process, perform research on entries using a flexible research implementation, create new notes, tag them based on existing tags, and update distilled notes. It will use Anthropic's Claude API and include an AI review feedback loop using LangGraph, followed by a human review step before finalizing changes. The interface will be terminal-based.

## Requirements

1. List and allow selection of daily notes sorted by date
2. Process selected daily notes in Obsidian
3. Extract entries from daily notes
4. Perform research on each entry using GPTResearcher
5. Create new notes for each entry
6. Tag new notes based on existing tags in Obsidian
7. Update relevant distilled notes
8. Integrate with LangGraph for workflow management
9. Implement AI review feedback loop using LangGraph
10. Use LangChain with Anthropic's Claude API for AI model interaction
11. Access Obsidian vault files directly in the file system
12. Generate new files in a temporary directory for AI and human review
13. Provide a diff view for changes to existing notes
14. Allow human approval before finalizing changes
15. Operate entirely through a terminal-based interface

## Architecture

```plantuml
@startuml
class ObsidianBoy {
  +run()
  -define_workflow()
  -execute_workflow()
}
class FileSystemInterface {
  +list_daily_notes()
  +read_daily_note()
  +create_temp_note()
  +update_note()
  +get_existing_tags()
  +move_temp_to_vault()
}
class DailyNoteProcessor {
  +extract_entries()
}
abstract class Researcher {
  {abstract} +research_entry()
}
class GPTResearcherImplementation {
  +research_entry()
}
class NoteCreator {
  +create_note()
}
class NoteTagger {
  +tag_note()
  +extract_existing_tags()
}
class DistilledNoteUpdater {
  +update_distilled_note()
}
class AIReviewLoop {
  +review_content()
  +provide_feedback()
  +refine_content()
}
class HumanReviewInterface {
  +review_new_notes()
  +review_note_changes()
}
class DiffGenerator {
  +generate_diff()
}
class TerminalInterface {
  +display_menu()
  +get_user_input()
  +show_daily_notes()
  +select_daily_notes()
}

ObsidianBoy --> FileSystemInterface
ObsidianBoy --> DailyNoteProcessor
ObsidianBoy --> Researcher
Researcher <|-- GPTResearcherImplementation
ObsidianBoy --> NoteCreator
ObsidianBoy --> NoteTagger
ObsidianBoy --> DistilledNoteUpdater
ObsidianBoy --> AIReviewLoop
ObsidianBoy --> HumanReviewInterface
ObsidianBoy --> TerminalInterface
ObsidianBoy --> DiffGenerator
@enduml
```

## Implementation Tasks for Aider

1. Implement FileSystemInterface class
   1. Implement method to list daily notes sorted by date
   2. Implement method to read daily notes from file system
   3. Implement method to create new notes in a temporary directory
   4. Implement method to update existing notes
   5. Implement method to retrieve existing tags
   6. Implement method to move files from temporary directory to Obsidian vault

2. Implement TerminalInterface class
   1. Implement method to display menu options
   2. Implement method to get user input
   3. Implement method to show list of daily notes
   4. Implement method to allow selection of daily notes

3. Implement DailyNoteProcessor class
   1. Create method to extract entries from daily notes
   2. Implement logic to parse entry format (name, link, description)

4. Implement Researcher abstract class and GPTResearcherImplementation
   1. Define abstract research_entry method in Researcher class
   2. Implement GPTResearcherImplementation class
   3. Set up GPTResearcher as a submodule or dependency
   4. Implement research_entry method using GPTResearcher

5. Implement NoteCreator class
   1. Create method to generate new note content based on research
   2. Integrate with FileSystemInterface to create the note in temp directory

6. Implement NoteTagger class
   1. Develop logic to suggest tags based on note content and existing tags
   2. Implement method to extract existing tags from a note
   3. Integrate with FileSystemInterface to apply tags to notes

7. Implement DistilledNoteUpdater class
   1. Create method to identify relevant distilled notes
   2. Implement logic to update distilled notes with new information

8. Implement AIReviewLoop class
   1. Define review_content method to analyze generated or updated notes
   2. Implement provide_feedback method to generate improvement suggestions
   3. Create refine_content method to apply AI-suggested improvements

9. Implement DiffGenerator class
   1. Create method to generate diff between original and updated notes

10. Implement HumanReviewInterface class
    1. Develop method to present AI-reviewed notes for human review in terminal
    2. Implement method to show diff and get approval for note changes in terminal

11. Implement ObsidianBoy class
    1. Set up integration with Anthropic's Claude API
    2. Implement define_workflow method using LangGraph to orchestrate all components
    3. Implement execute_workflow method to run the LangGraph workflow
    4. Implement main run method to initialize and execute the entire process
    5. Ensure proper sequencing of AI review before human review

12. Develop configuration management
    1. Create a configuration file for API keys, file paths, etc.
    2. Implement a configuration loader

13. Create integration tests
    1. Develop end-to-end tests that cover the entire workflow
    2. Create test fixtures and mock data for integration testing

14. Create main script
    1. Implement a main.py script to run ObsidianBoy

15. Document the code and create user guide
    1. Write docstrings for all classes and methods
    2. Create a README.md with setup and usage instructions

## Notes for Aider

- Task 1 (project setup) will be provided by the user
- When integrating GPTResearcher, refer to its GitHub repository for usage instructions
- For file system operations, use Python's built-in `os` and `shutil` modules
- To generate diffs, consider using the `difflib` module from Python's standard library
- When working with markdown files, you may want to use a library like `markdown` or `commonmark`
- Use a mocking library like `unittest.mock` or `pytest-mock` for creating test doubles
- Consider using a test runner like `pytest` for easier test organization and execution
- For the terminal interface, you can use Python's built-in `input()` function or a library like `prompt_toolkit` for more advanced features
- When implementing the Researcher class and its GPTResearcher implementation, use the Strategy pattern to allow for easy swapping of research implementations in the future
- The ObsidianBoy class will be responsible for orchestrating all components using LangGraph. Implement the workflow as a series of steps that can be easily modified and extended
- Ensure proper error handling and API rate limiting when interacting with the Anthropic API
- For the AI review feedback loop, use LangGraph to create a multi-step review process that can iterate on content improvements