"""In-memory storage for PromptLab

This module provides simple in-memory storage for prompts and collections.
In a production environment, this would be replaced with a database.
"""

from typing import Dict, List, Optional
from app.models import Prompt, Collection


class Storage:
    """A simple in-memory storage system for prompts and collections.

    This class provides methods to create, retrieve, update, and delete prompts
    and collections. It also offers utility functions to clear all data and fetch
    prompts by their collection.

    Attributes:
        _prompts: A dictionary storing Prompt objects keyed by their IDs.
        _collections: A dictionary storing Collection objects keyed by their IDs.
    """

    def __init__(self):
        """Initializes the storage with empty prompts and collections."""
        self._prompts: Dict[str, Prompt] = {}
        self._collections: Dict[str, Collection] = {}
    
    # ============== Prompt Operations ==============
    
    def create_prompt(self, prompt: Prompt) -> Prompt:
        """Creates a new prompt and adds it to storage.

        Args:
            prompt: A Prompt object to be added.
        Returns:
            The added Prompt object.
    
        Example:
            prompt = Prompt(id="123", content="Sample")
            storage.create_prompt(prompt)
        """
        self._prompts[prompt.id] = prompt
        return prompt
    
    def get_prompt(self, prompt_id: str) -> Optional[Prompt]:
        """Retrieves a prompt by its ID.

        Args:
            prompt_id: The ID of the prompt to retrieve.
        Returns:
            The Prompt object if found, otherwise None.
    
        Example:
            prompt = storage.get_prompt("123")
        """
        return self._prompts.get(prompt_id)

    def get_all_prompts(self) -> List[Prompt]:
        """Retrieves all prompts from storage.

        Returns:
            A list of all Prompt objects.

        Example:
            all_prompts = storage.get_all_prompts()
        """
        return list(self._prompts.values())
    
    def update_prompt(self, prompt_id: str, prompt: Prompt) -> Optional[Prompt]:
        """Updates an existing prompt in storage.

        Args:
            prompt_id: The ID of the prompt to update.
            prompt: The new Prompt object to replace the old one.

        Returns:
            The updated Prompt object if the prompt was found, otherwise None.

        Example:
            updated_prompt = storage.update_prompt("123", new_prompt)
        """
        if prompt_id not in self._prompts:
            return None
        self._prompts[prompt_id] = prompt
        return prompt
    
    def delete_prompt(self, prompt_id: str) -> bool:
        """Deletes a prompt by its ID.

        Args:
            prompt_id: The ID of the prompt to delete.

        Returns:
            True if the prompt was successfully deleted, otherwise False.

        Example:
            success = storage.delete_prompt("123")
        """
        if prompt_id in self._prompts:
            del self._prompts[prompt_id]
            return True
        return False
    
    # ============== Collection Operations ==============
    def create_collection(self, collection: Collection) -> Collection:
        """Creates a new collection and adds it to storage.

        Args:
            collection: A Collection object to be added.

        Returns:
            The added Collection object.

        Example:
            collection = Collection(id="456", name="My Collection")
            storage.create_collection(collection)
        """
        self._collections[collection.id] = collection
        return collection
    
    def get_collection(self, collection_id: str) -> Optional[Collection]:
        """Retrieves a collection by its ID.

        Args:
            collection_id: The ID of the collection to retrieve.

        Returns:
            The Collection object if found, otherwise None.

        Example:
            collection = storage.get_collection("456")
        """
        return self._collections.get(collection_id)
    
    def get_all_collections(self) -> List[Collection]:
        """Retrieves all collections from storage.

        Returns:
            A list of all Collection objects.

        Example:
            all_collections = storage.get_all_collections()
        """
        return list(self._collections.values())
    
    def delete_collection(self, collection_id: str) -> bool:
        """Deletes a collection by its ID.

        Args:
            collection_id: The ID of the collection to delete.

        Returns:
            True if the collection was successfully deleted, otherwise False.

        Example:
            success = storage.delete_collection("456")
        """
        if collection_id in self._collections:
            del self._collections[collection_id]
            return True
        return False
    
    def get_prompts_by_collection(self, collection_id: str) -> List[Prompt]:
        """Retrieves all prompts belonging to a specific collection.

        Args:
            collection_id: The ID of the collection to filter prompts by.

        Returns:
            A list of Prompt objects belonging to the specified collection.

        Example:
            prompts = storage.get_prompts_by_collection("456")
        """
        return [p for p in self._prompts.values() if p.collection_id == collection_id]
    
    # ============== Utility ==============
    
    def clear(self):
        """Clears all prompts and collections from the storage.

        Example:
            storage.clear()
        """
        self._prompts.clear()
        self._collections.clear()


# Global storage instance
storage = Storage()

