"""FastAPI routes for PromptLab"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from app.models import (
    Prompt, PromptCreate, PromptUpdate, PromptPatch,
    Collection, CollectionCreate,
    PromptList, CollectionList, HealthResponse,
    get_current_time
)
from app.storage import storage
from app.utils import sort_prompts_by_date, filter_prompts_by_collection, search_prompts
from app import __version__


app = FastAPI(
    title="PromptLab API",
    description="AI Prompt Engineering Platform",
    version=__version__
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============== Health Check ==============

@app.get("/health", response_model=HealthResponse)
def health_check():
    """
    Health Check Endpoint

    Performs a basic health check for the API, returning the current API
    version and health status.

    Args:
        None

    Returns:
        HealthResponse: An object containing health status and version information.

    Example:
        To check the health of the API, make a GET request to the `/health` endpoint:

        >>> response = client.get("/health")
        >>> response.json()
        {"status": "healthy", "version": "1.0.0"}
    """
    return HealthResponse(status="healthy", version=__version__)

# ============== Prompt Endpoints ==============

@app.get("/prompts", response_model=PromptList)
def list_prompts(
    collection_id: Optional[str] = None,
    search: Optional[str] = None
):
    """
    Retrieves a list of prompts with optional filtering by collection and search query.

    Args:
        collection_id (Optional[str]): The ID of the collection to filter prompts.
        search (Optional[str]): A search query to filter prompts containing the term.

    Returns:
        PromptList: A list of prompts filtered and sorted by date.

    Example usage:
        >>> list_prompts(collection_id="123", search="example query")
    """
    prompts = storage.get_all_prompts()
    
    # Filter by collection if specified
    if collection_id:
        prompts = filter_prompts_by_collection(prompts, collection_id)
    
    # Search if query provided
    if search:
        prompts = search_prompts(prompts, search)
    
    # Sort by date (newest first)
    # Note: There might be an issue with the sorting...
    prompts = sort_prompts_by_date(prompts, descending=True)
    
    return PromptList(prompts=prompts, total=len(prompts))


@app.get("/prompts/{prompt_id}", response_model=Prompt)
def get_prompt(prompt_id: str):
    """
    Retrieves a specific prompt by its ID.

    Args:
        prompt_id (str): The unique identifier for the prompt.

    Returns:
        Prompt: The prompt corresponding to the ID.

    Raises:
        HTTPException: If the prompt does not exist (404 error).

    Example usage:
        >>> get_prompt("prompt_id_123")
    """
    prompt = storage.get_prompt(prompt_id)
    
    # Fix: Check if prompt is None and raise 404 if it doesn't exist
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    # Return the prompt
    return prompt


@app.post("/prompts", response_model=Prompt, status_code=201)
def create_prompt(prompt_data: PromptCreate):
    """
    Creates a new prompt, validating collection existence if specified.

    Args:
        prompt_data (PromptCreate): The data required to create a new prompt.

    Returns:
        Prompt: The newly created prompt.

    Raises:
        HTTPException: If the specified collection does not exist (400 error).

    Example usage:
        >>> create_prompt(prompt_data)
    """
    # Validate collection exists if provided
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")
    
    prompt = Prompt(**prompt_data.model_dump())
    return storage.create_prompt(prompt)


@app.put("/prompts/{prompt_id}", response_model=Prompt)
def update_prompt(prompt_id: str, prompt_data: PromptUpdate):
    """Updates an existing prompt with new data.

    Args:
        prompt_id (str): The unique identifier of the prompt to update.
        prompt_data (PromptUpdate): The new data for the prompt, including
            fields like title, content, description, and optionally, collection_id.

    Returns:
        Prompt: The updated prompt object.

    Raises:
        HTTPException: If the prompt does not exist (404) or if the provided
            collection_id is invalid (400).

    Example usage:
        >>> update_prompt(
                prompt_id="abc123",
                prompt_data=PromptUpdate(
                    title="New Title",
                    content="Updated content...",
                    description="New description",
                    collection_id="col123"
                )
            )
    """
    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    # Validate collection if provided
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")
    
    # BUG #2: We're not updating the updated_at timestamp!
    # The updated prompt keeps the old timestamp
    updated_prompt = Prompt(
        id=existing.id,
        title=prompt_data.title,
        content=prompt_data.content,
        description=prompt_data.description,
        collection_id=prompt_data.collection_id,
        created_at=existing.created_at,
        updated_at=get_current_time()  # Set to current time 
    )
    
    return storage.update_prompt(prompt_id, updated_prompt)


# NOTE: PATCH endpoint is missing! Students need to implement this.
# It should allow partial updates (only update provided fields)
@app.patch("/prompts/{prompt_id}", response_model=Prompt)
def patch_prompt(prompt_id: str, prompt_data: PromptPatch):
    """Update an existing prompt with new data.

    This function retrieves an existing prompt using its identifier,
    updates it with the provided new data, and validates any changes
    to its collection, if applicable. If successful, the updated prompt
    is stored back into the storage.

    Args:
        prompt_id (str): The unique identifier of the prompt to be updated.
        prompt_data (PromptPatch): An object containing the new data to update the prompt with.

    Returns:
        Prompt: The updated prompt object after the changes have been saved.

    Raises:
        HTTPException: If the prompt or its collection is not found in the storage.

    Example:
        prompt_data = PromptPatch(title="New Title")
        updated_prompt = patch_prompt("12345", prompt_data)
    """

    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")

    # Create a dict of the existing prompt
    updated_data = existing.model_dump()
    
    # Get the update data, excluding unset fields
    update_data = prompt_data.model_dump(exclude_unset=True)
    
    # Update the dict with the new data
    updated_data.update(update_data)
    
    # Create a new Prompt object from the updated data
    updated_prompt = Prompt(**updated_data)

    # Validate collection if provided
    if updated_prompt.collection_id and (not existing.collection_id or existing.collection_id != updated_prompt.collection_id):
        collection = storage.get_collection(updated_prompt.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")

    # Update the timestamp
    updated_prompt.updated_at = get_current_time()

    return storage.update_prompt(prompt_id, updated_prompt)


@app.delete("/prompts/{prompt_id}", status_code=204)
def delete_prompt(prompt_id: str):
    """Deletes a prompt by its unique identifier.

    Args:
        prompt_id (str): The unique identifier of the prompt to be deleted.

    Returns:
        None: This endpoint does not return any data.

    Raises:
        HTTPException: If the prompt is not found, an HTTP 404 error is raised.

    Example usage:
        delete_prompt("123456")
    """
    if not storage.delete_prompt(prompt_id):
        raise HTTPException(status_code=404, detail="Prompt not found")
    return None


# ============== Collection Endpoints ==============
@app.get("/collections", response_model=CollectionList)
def list_collections():
    """Lists all collections.

    Returns:
        CollectionList: An instance containing a list of all collections and their total count.

    Example usage:
        collections = list_collections()
    """
    collections = storage.get_all_collections()
    return CollectionList(collections=collections, total=len(collections))


@app.get("/collections/{collection_id}", response_model=Collection)
def get_collection(collection_id: str):
    """Fetches a collection by its unique identifier.

    Args:
        collection_id (str): The unique identifier of the collection to retrieve.

    Returns:
        Collection: The collection object if found.

    Raises:
        HTTPException: If the collection is not found, an HTTP 404 error is raised.

    Example usage:
        collection = get_collection("abc123")
    """
    collection = storage.get_collection(collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection
    

@app.post("/collections", response_model=Collection, status_code=201)
def create_collection(collection_data: CollectionCreate):
    """Creates a new collection.

    Args:
        collection_data (CollectionCreate): The data required to create a collection.

    Returns:
        Collection: The newly created collection object.

    Example usage:
        new_collection = create_collection(collection_data)
    """
    collection = Collection(**collection_data.model_dump())
    return storage.create_collection(collection)

@app.delete("/collections/{collection_id}", status_code=204)
def delete_collection(collection_id: str):
    """
    Deletes a specified collection from storage and unlinks all associated
    prompts by setting their `collection_id` to None.

    Args:
        collection_id (str): The unique identifier of the collection to be deleted.

    Raises:
        HTTPException: If the collection with the given ID does not exist (404).

    Returns:
        None: This function does not return any value. It sends a 204 No Content
              HTTP status code upon successful deletion.

    Example usage:
        >>> delete_collection("12345")
        (Returns a 204 HTTP status response)
    """

    # Check if collection exists
    collection = storage.get_collection(collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    
    # Unlink prompts from this collection
    prompts = storage.get_prompts_by_collection(collection_id)
    for prompt in prompts:
        # Create a new Prompt object with collection_id=None and updated timestamp
        updated_prompt = Prompt(
            id=prompt.id,
            title=prompt.title,
            content=prompt.content,
            description=prompt.description,
            collection_id=None,
            created_at=prompt.created_at,
            updated_at=get_current_time()
        )
        storage.update_prompt(prompt.id, updated_prompt)
    
    storage.delete_collection(collection_id)
    return None

