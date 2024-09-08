from abc import ABC, abstractmethod
from pathlib import Path
import json

class KnowledgeBase(ABC):
    @abstractmethod
    def store(self, key: str, content: str) -> None:
        """
        Store content in the knowledge base.

        Args:
            key (str): The unique identifier for the content.
            content (str): The content to be stored.
        """
        pass

    @abstractmethod
    def retrieve(self, key: str) -> str:
        """
        Retrieve content from the knowledge base.

        Args:
            key (str): The unique identifier for the content.

        Returns:
            str: The retrieved content.

        Raises:
            KeyError: If the key is not found in the knowledge base.
        """
        pass

class FileSystemKnowledgeBase(KnowledgeBase):
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def store(self, key: str, content: str) -> None:
        """
        Store content in the file system.

        Args:
            key (str): The unique identifier for the content.
            content (str): The content to be stored.
        """
        file_path = self.base_path / f"{key}.json"
        data = {"key": key, "content": content}
        with file_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def retrieve(self, key: str) -> str:
        """
        Retrieve content from the file system.

        Args:
            key (str): The unique identifier for the content.

        Returns:
            str: The retrieved content.

        Raises:
            KeyError: If the key is not found in the knowledge base.
        """
        file_path = self.base_path / f"{key}.json"
        if not file_path.exists():
            raise KeyError(f"No content found for key: {key}")
        
        with file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return data["content"]
