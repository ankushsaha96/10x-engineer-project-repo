"""Utility functions for PromptLab"""

from typing import List
from app.models import Prompt


def sort_prompts_by_date(prompts: List[Prompt], descending: bool = True) -> List[Prompt]:
    """Sort prompts by creation date.
    
    Note: There might be a bug here. Check the sort order!
    """
    # BUG #3: This sorts ascending (oldest first) when it should sort descending (newest first)
    # The 'descending' parameter is ignored!
    # Fix: Use 'reverse' parameter to respect 'descending' flag
    return sorted(prompts, key=lambda p: p.created_at, reverse=descending)


def filter_prompts_by_collection(prompts: List[Prompt], collection_id: str) -> List[Prompt]:
    """Filters a list of Prompt objects by collection ID.

    Args:
        prompts (List[Prompt]): A list of Prompt objects to be filtered.
        collection_id (str): The ID of the collection to filter prompts by.

    Returns:
        List[Prompt]: A list of Prompt objects that belong to the specified collection.

    Example usage:
        filter_prompts_by_collection(all_prompts, 'collection_123')
    """
    return [p for p in prompts if p.collection_id == collection_id]


def search_prompts(prompts: List[Prompt], query: str) -> List[Prompt]:
    """Searches through a list of Prompt objects and returns those that match the query.

    Args:
        prompts (List[Prompt]): A list of Prompt objects to search through.
        query (str): The search query to filter prompts by.
    Returns:
        List[Prompt]: A list of Prompt objects that match the search query in their title or description.

    Example usage:
        search_prompts(all_prompts, 'keyword')
    """
    query_lower = query.lower()
    return [
        p for p in prompts 
        if query_lower in p.title.lower() or 
           (p.description and query_lower in p.description.lower())
    ]


def validate_prompt_content(content: str) -> bool:
    """Check if prompt content is valid.
    
    A valid prompt should:
    - Not be empty
    - Not be just whitespace
    - Be at least 10 characters
    """
    if not content or not content.strip():
        return False
    return len(content.strip()) >= 10


def extract_variables(content: str) -> List[str]:
    """Extract template variables from prompt content.
    
    Variables are in the format {{variable_name}}
    """
    import re
    pattern = r'\{\{(\w+)\}\}'
    return re.findall(pattern, content)

