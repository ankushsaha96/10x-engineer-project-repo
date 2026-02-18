# Tagging System Specification

## 1. Overview

This document specifies a new **Tagging System** for the PromptLab API. This feature will allow users to add descriptive tags to their prompts, making it easier to organize, search, and filter them.

## 2. User Stories

-   **As a user, I want to add tags to a prompt.**
    -   **Acceptance Criteria:**
        -   When creating or editing a prompt, I can add one or more tags.
        -   Tags are simple strings (e.g., "summarization", "creative-writing").
-   **As a user, I want to remove tags from a prompt.**
    -   **Acceptance Criteria:**
        -   I can easily remove tags from a prompt I am editing.
-   **As a user, I want to search for prompts by tags.**
    -   **Acceptance Criteria:**
        -   The `GET /prompts` endpoint should support filtering by one or more tags.
        -   I can combine tag-based filtering with other filters (like `collection_id` and `search`).
-   **As a user, I want to see all tags associated with a prompt.**
    -   **Acceptance Criteria:**
        -   When I view a prompt, I can see a list of all its tags.

## 3. Data Model Changes

### `Tag` Model

A new `Tag` model will be introduced.

```python
class Tag:
    id: str  # Unique identifier for the tag
    name: str  # The tag name (e.g., "summarization")
```

### `PromptTag` Association Table

A many-to-many relationship between prompts and tags will be established through an association table.

```python
class PromptTag:
    prompt_id: str  # Foreign key to the Prompt model
    tag_id: str  # Foreign key to the Tag model
```

### `Prompt` Model Modification

The `Prompt` model will be updated to include a list of tags.

```python
class Prompt:
    # ... existing fields ...
    tags: list[str]  # A list of tag names
```

## 4. API Endpoint Specifications

### Add/Update Tags for a Prompt

The existing `POST /prompts` and `PUT /prompts/{prompt_id}` endpoints will be updated to accept a `tags` field.

-   **Request Body (for `POST` and `PUT`):**
    ```json
    {
      "title": "My Prompt",
      "content": "This is my prompt.",
      "tags": ["summarization", "creative-writing"]
    }
    ```

### Filter Prompts by Tags

The `GET /prompts` endpoint will be updated to support a `tags` query parameter.

-   **Query Parameters:**
    -   `tags` (optional, string): A comma-separated list of tag names to filter by (e.g., `tags=summarization,creative-writing`).
-   **Request Example:**
    ```
    GET /prompts?tags=summarization,creative-writing
    ```

## 5. Search/Filter Requirements

-   **Combining Filters:** The `tags` filter should work in conjunction with the existing `collection_id` and `search` filters.
-   **Filtering Logic:** When multiple tags are provided, the API should return prompts that have *all* of the specified tags (an "AND" condition).
-   **Case-Insensitive Matching:** Tag matching should be case-insensitive to avoid duplicate tags (e.g., "Python" and "python" should be treated as the same tag).
