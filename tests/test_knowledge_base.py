import pytest
import tempfile
from pathlib import Path
from obsidian_boy.knowledge_base import FileSystemKnowledgeBase

@pytest.fixture
def temp_kb():
    with tempfile.TemporaryDirectory() as tmpdirname:
        kb = FileSystemKnowledgeBase(tmpdirname)
        yield kb

def test_store_and_retrieve(temp_kb):
    key = "test_key"
    content = "This is test content"
    
    # Store content
    temp_kb.store(key, content)
    
    # Retrieve content
    retrieved_content = temp_kb.retrieve(key)
    
    assert retrieved_content == content

def test_retrieve_nonexistent_key(temp_kb):
    with pytest.raises(KeyError):
        temp_kb.retrieve("nonexistent_key")

def test_overwrite_existing_key(temp_kb):
    key = "existing_key"
    original_content = "Original content"
    new_content = "New content"
    
    temp_kb.store(key, original_content)
    temp_kb.store(key, new_content)
    
    retrieved_content = temp_kb.retrieve(key)
    assert retrieved_content == new_content

def test_multiple_entries(temp_kb):
    entries = {
        "key1": "Content 1",
        "key2": "Content 2",
        "key3": "Content 3"
    }
    
    for key, content in entries.items():
        temp_kb.store(key, content)
    
    for key, content in entries.items():
        assert temp_kb.retrieve(key) == content

def test_file_creation(temp_kb):
    key = "test_file"
    content = "File content"
    
    temp_kb.store(key, content)
    
    file_path = Path(temp_kb.base_path) / f"{key}.json"
    assert file_path.exists()
    assert file_path.is_file()
