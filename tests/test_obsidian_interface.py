import pytest
from pathlib import Path
from obsidian_boy.obsidian_interface import ObsidianInterface

@pytest.fixture
def fs_interface(tmp_path):
    vault_path = tmp_path / "vault"
    temp_dir = tmp_path / "temp"
    vault_path.mkdir()
    temp_dir.mkdir()
    return ObsidianInterface(vault_path, temp_dir)

def test_list_daily_notes(fs_interface):
    # Create Daily directory and some test notes
    daily_dir = fs_interface.vault_path / "Daily"
    daily_dir.mkdir()
    (daily_dir / "2023-05-01.md").touch()
    (daily_dir / "2023-05-02.md").touch()
    (daily_dir / "2023-05-03.md").touch()

    notes = fs_interface.list_daily_notes()
    assert len(notes) == 3
    assert [note.name for note in notes] == ["2023-05-03.md", "2023-05-02.md", "2023-05-01.md"]

def test_read_daily_note(fs_interface):
    note_path = fs_interface.vault_path / "test_note.md"
    note_path.write_text("Test content", encoding="utf-8")

    content = fs_interface.read_daily_note(note_path)
    assert content == "Test content"

def test_create_temp_note(fs_interface):
    temp_note = fs_interface.create_temp_note("temp_note", "Temporary content")
    assert temp_note.exists()
    assert temp_note.read_text(encoding="utf-8") == "Temporary content"

def test_update_note(fs_interface):
    note_path = fs_interface.vault_path / "update_test.md"
    note_path.write_text("Original content", encoding="utf-8")

    fs_interface.update_note(note_path, "Updated content")
    assert note_path.read_text(encoding="utf-8") == "Updated content"

def test_get_existing_tags(fs_interface):
    (fs_interface.vault_path / "note1.md").write_text("Content with #tag1 and #tag2", encoding="utf-8")
    (fs_interface.vault_path / "note2.md").write_text("Content with #tag2 and #tag3", encoding="utf-8")

    tags = fs_interface.get_existing_tags()
    assert tags == ["tag1", "tag2", "tag3"]

def test_move_temp_to_vault(fs_interface):
    temp_note = fs_interface.create_temp_note("temp_note", "Temporary content")
    moved_note = fs_interface.move_temp_to_vault(temp_note, "final_note")

    assert not temp_note.exists()
    assert moved_note.exists()
    assert moved_note.read_text(encoding="utf-8") == "Temporary content"
    assert moved_note.name == "final_note.md"
