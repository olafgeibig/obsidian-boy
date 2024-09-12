import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from obsidian_boy.terminal_interface import TerminalInterface
from obsidian_boy.obsidian_interface import ObsidianInterface

@pytest.fixture
def mock_fs_interface():
    return MagicMock(spec=ObsidianInterface)

@pytest.fixture
def terminal_interface(mock_fs_interface):
    return TerminalInterface(mock_fs_interface)

def test_display_menu(terminal_interface, capsys):
    terminal_interface.display_menu()
    captured = capsys.readouterr()
    assert "ObsidianBoy Menu:" in captured.out
    assert "1. List daily notes" in captured.out
    assert "2. Select daily notes" in captured.out
    assert "3. Exit" in captured.out

def test_get_user_input(terminal_interface):
    with patch('builtins.input', return_value='test input'):
        result = terminal_interface.get_user_input("Enter something: ")
    assert result == 'test input'

def test_show_daily_notes(terminal_interface, mock_fs_interface, capsys):
    mock_fs_interface.list_daily_notes.return_value = [
        Path('2023-05-01.md'),
        Path('2023-05-02.md'),
        Path('2023-05-03.md')
    ]
    terminal_interface.show_daily_notes()
    captured = capsys.readouterr()
    assert "Daily Notes:" in captured.out
    assert "1. 2023-05-01" in captured.out
    assert "2. 2023-05-02" in captured.out
    assert "3. 2023-05-03" in captured.out

def test_select_daily_notes(terminal_interface, mock_fs_interface):
    mock_fs_interface.list_daily_notes.return_value = [
        Path('2023-05-01.md'),
        Path('2023-05-02.md'),
        Path('2023-05-03.md')
    ]
    with patch('builtins.input', return_value='1,3'):
        selected = terminal_interface.select_daily_notes()
    assert selected == [Path('2023-05-01.md'), Path('2023-05-03.md')]

def test_select_daily_notes_invalid_input(terminal_interface, mock_fs_interface):
    mock_fs_interface.list_daily_notes.return_value = [
        Path('2023-05-01.md'),
        Path('2023-05-02.md'),
        Path('2023-05-03.md')
    ]
    with patch('builtins.input', return_value='1,4,2'):
        selected = terminal_interface.select_daily_notes()
    assert selected == [Path('2023-05-01.md'), Path('2023-05-02.md')]
