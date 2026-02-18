"""Pydantic models for PromptLab"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from uuid import uuid4


from uuid import uuid4
from datetime import datetime

def generate_id() -> str:
    """Generates a unique identifier.

    This function generates a unique identifier using UUID version 4.
    UUID4 (Universally Unique Identifier) is randomly generated and provides an ID that is practically unique.

    Returns:
        str: A string representation of the generated UUID.

    Example:
        >>> unique_id = generate_id()
        >>> isinstance(unique_id, str)
        True
    """
    return str(uuid4())


def get_current_time() -> datetime:
    """Gets the current UTC time.

    This function returns the current Coordinated Universal Time (UTC)
    as a datetime object.

    Returns:
        datetime: The current time in UTC.

    Example:
        >>> current_time = get_current_time()
        >>> isinstance(current_time, datetime)
        True
    """
    return datetime.utcnow()


# ============== Prompt Models ==============

class PromptBase(BaseModel):
    """
    Base model for prompts with validation on fields.

    Attributes:
        title (str): Title of the prompt, must be between 1 and 200 characters.
        content (str): Content of the prompt, must have at least 1 character.
        description (Optional[str]): Optional description of the prompt, up to 500 characters.
        collection_id (Optional[str]): Optional ID for the collection the prompt belongs to.

    Example:
        prompt = PromptBase(title="Sample Title", content="This is a sample.", description="A brief description.")
    """
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    description: Optional[str] = Field(None, max_length=500)
    collection_id: Optional[str] = None


class PromptCreate(PromptBase):
    pass


class PromptUpdate(PromptBase):
    pass


class PromptPatch(BaseModel):
    """Model representing a patch for a prompt.

    This model is used to update the properties of a prompt, allowing optional
    fields for title, content, and description. It uses constraints to ensure
    that the updated fields meet certain length requirements.

    Attributes:
        title (Optional[str]): The title of the prompt, with a minimum length of 1
            and a maximum length of 200 characters.
        content (Optional[str]): The content of the prompt, having a minimum length of 1.
        description (Optional[str]): A description of the prompt, with a maximum length of 500 characters.
        collection_id (Optional[str]): An optional collection identifier associated with the prompt.

    Example:
        prompt_patch = PromptPatch(
            title="New Title",
            content="Updated content",
            description="A brief description of the changes",
        )
    """
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = Field(None, max_length=500)
    collection_id: Optional[str] = None


class Prompt(PromptBase):
    """Model representing a full prompt entity.

    This model defines a prompt with an identifier and timestamps for creation
    and last update. It extends the `PromptBase` class with additional attributes
    for management in a database or storage system.

    Attributes:
        id (str): Unique identifier for the prompt, generated automatically.
        created_at (datetime): Timestamp when the prompt was created, set by default.
        updated_at (datetime): Timestamp for the last update to the prompt, set by default.

    Example:
        prompt = Prompt(
            id="1234abcd",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
    """
    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)
    updated_at: datetime = Field(default_factory=get_current_time)

    class Config:
        from_attributes = True


# ============== Collection Models ==============

class CollectionBase(BaseModel):
    """Base model for a Collection.

    Attributes:
        name (str): Name of the collection (1-100 characters).
        description (Optional[str]): Description of the collection with a maximum of 500 characters.
    """
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class CollectionCreate(CollectionBase):
    """Model for creating a new collection.

    Inherits all attributes from CollectionBase and is used for collection creation.
    """


class Collection(CollectionBase):
    """Model representing a collection.

    Inherits all attributes from CollectionBase and adds additional identifier and timestamps.

    Attributes:
        id (str): Unique identifier for the collection.
        created_at (datetime): Timestamp when the collection was created.
    """

    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)


    class Config:
        from_attributes = True


# ============== Response Models ==============

class PromptList(BaseModel):
    """Model for a list of prompts.

    Attributes:
        prompts (List[Prompt]): List of prompts.
        total (int): Total number of prompts in the list.
    """    
    prompts: List[Prompt]
    total: int


class CollectionList(BaseModel):
    """Model for a list of collections.

    Attributes:
        collections (List[Collection]): List of collections.
        total (int): Total number of collections in the list.
    """
    collections: List[Collection]
    total: int


class HealthResponse(BaseModel):
    """Model for health response.

    Attributes:
        status (str): Status of the application.
        version (str): Current version of the application.
    """
    status: str
    version: str
