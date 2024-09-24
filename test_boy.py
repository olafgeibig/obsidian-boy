import os
from pathlib import Path
from typing import List
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.schema import HumanMessage
from obsidian_boy.obsidian_interface import ObsidianInterface
from obsidian_boy.terminal_interface import TerminalInterface
from obsidian_boy.daily_note_processor import DailyNoteProcessor, DailyNoteEntry
from obsidian_boy.web_scraper import WebScraper
from dotenv import load_dotenv
from phoenix.otel import register
from openinference.instrumentation.openai import OpenAIInstrumentor
from openinference.instrumentation.crewai import CrewAIInstrumentor
from openinference.instrumentation.langchain import LangChainInstrumentor

# Set the default vault path
VAULT_PATH = Path(os.getenv('VAULT_PATH', './vault'))

def main():
    # Load environment variables from .env file
    load_dotenv()
    tracer_provider = register(
    project_name="obsidian-boy",
    endpoint="http://localhost:6006/v1/traces"
    )
    # OpenAIInstrumentor().instrument(tracer_provider=tracer_provider)
    LangChainInstrumentor().instrument(tracer_provider=tracer_provider)
    
    # Initialize the file system interface
    obsidian_interface = ObsidianInterface(vault_path=VAULT_PATH)

    # Initialize the terminal interface
    terminal_interface = TerminalInterface(obsidian_interface)

    # Initialize the daily note processor with the Anthropic Chat model

    # API_KEY = os.getenv("ANTHROPIC_API_KEY")
    # llm = ChatAnthropic(
    #     model="claude-3-5-sonnet-20240620", 
    #     api_key=API_KEY, 
    #     temperature=0.0
    # )
    # API_KEY = os.getenv("DEEPSEEK_API_KEY")
    # llm = ChatOpenAI(
    #     model="deepseek-chat", 
    #     api_key=API_KEY,
    #     base_url="https://api.deepseek.com/v1", 
    #     temperature=0.0
    # )
    llm = ChatOpenAI(
        model="gpt-4o-mini", 
        temperature=0.0
    )
    daily_note_processor = DailyNoteProcessor(llm=llm)

    # Display the menu and get user input
    terminal_interface.display_menu()
    selected_notes = terminal_interface.select_daily_notes()

    # Process each selected note
    for note_path in selected_notes:
        note_content = obsidian_interface.read_daily_note(note_path)
        entries = daily_note_processor.extract_entries(note_content)
        print(entries)

        # Display the extracted entries
        print(f"\nEntries extracted from {note_path.name}:")
        for entry in entries:
            print(f"Title: {entry.title}")
            print(f"Link: {entry.link}")
            print(f"Description: {entry.description}")
            print(f"Tags: {', '.join(entry.tags)}")
            print(f"Todo: {entry.todo}")
            print("-" * 40)
    # scraper = WebScraper()
    # c = scraper.scrape("https://docs.crewai.com/core-concepts/Agents/")
    # print(c)

if __name__ == "__main__":
    main()
