import pytest
from pathlib import Path
from langchain_openai import ChatOpenAI
from obsidian_boy.daily_note_processor import DailyNoteProcessor, DailyNoteEntry
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Assuming the vault directory is in the same directory as the test file
VAULT_DIR = Path(os.getenv('VAULT_DIR', './vault'))

@pytest.fixture
def daily_note_file():
    # Provide the path to the daily note file
    return VAULT_DIR / 'Daily' / '2024-01-01.md'

@pytest.mark.integration_test
def test_process_daily_note(daily_note_file):
    # Initialize the LLM using the same configuration as in test_boy.py
    API_KEY = os.getenv("DEEPSEEK_API_KEY")
    llm = ChatOpenAI(
        model="deepseek-chat",
        api_key=API_KEY,
        base_url="https://api.deepseek.com/v1",
        temperature=0.0
    )

    # Initialize the DailyNoteProcessor with the real LLM
    processor = DailyNoteProcessor(llm=llm)

    # Read the content of the daily note file
    with open(daily_note_file, 'r') as file:
        note_content = file.read()

    # Process the daily note
    entries = processor.extract_entries(note_content)

    # Assert that the entries are correctly extracted
    assert entries is not None
    assert isinstance(entries, list)
    assert len(entries) == 3  # There should be exactly 3 entries in the note

    # Check the format of the entries
    for entry in entries:
        assert isinstance(entry, DailyNoteEntry)
        assert entry.title is not None or entry.link is not None
        assert isinstance(entry.tags, list)
        assert entry.todo is None or isinstance(entry.todo, str)

    # Add specific assertions for each entry based on the expected content of the note
    expected_entries = [
        DailyNoteEntry(
            title="Test 1",
            link="https://www.test1.com",
            description="The first test, a full entry",
            tags=["test"],
            todo="Test it harder"
        ),
        DailyNoteEntry(
            title="Test 2",
            link=None,
            description="The first test, a full entry",
            tags=["test"],
            todo=None
        ),
        DailyNoteEntry(
            title="Test 3",
            link="https://www.test3.com",
            description="The first test, a full entry",
            tags=[],
            todo=None
        )
    ]

    for expected_entry in expected_entries:
        assert expected_entry in entries