# Prompt Versioning Specification

## 1. Overview

This document specifies a new feature for the PromptLab API: **Prompt Versioning**. This feature will allow users to track changes to their prompts over time, view a history of revisions, and revert to previous versions if needed. This is crucial for maintaining a record of prompt evolution and for A/B testing different prompt variations.

## 2. User Stories

-   **As a user, I want to see a history of all changes made to a prompt.**
    -   **Acceptance Criteria:**
        -   When viewing a prompt, I can access a list of its historical versions.
        -   Each version in the history should have a version number, a timestamp, and the user who made the change.
-   **As a user, I want to view the content of a previous version of a prompt.**
    -   **Acceptance Criteria:**
        -   I can select any version from the history to see its full content.
-   **As a user, I want to revert a prompt to a previous version.**
    -   **Acceptance Criteria:**
        -   When viewing a previous version, I have an option to "revert" to this version.
        -   Reverting creates a new version that is a copy of the selected historical version.

## 3. Data Model Changes

### `PromptVersion` Model

A new model, `PromptVersion`, will be introduced to store historical versions of prompts.

```python
class PromptVersion:
    id: str  # Unique identifier for the version
    prompt_id: str  # Foreign key to the Prompt model
    version: int  # Version number (e.g., 1, 2, 3)
    content: str  # The full content of the prompt at this version
    created_at: str  # Timestamp of when this version was created
```

### `Prompt` Model Modification

The existing `Prompt` model will be updated to include a `latest_version` field.

```python
class Prompt:
    # ... existing fields ...
    latest_version: int  # The version number of the current version
```

## 4. API Endpoint Specifications

### Get Prompt Version History

-   **Endpoint:** `GET /prompts/{prompt_id}/versions`
-   **Description:** Retrieves a list of all historical versions for a given prompt.
-   **Success Response:**
    -   **Code:** `200 OK`
    -   **Content:**
        ```json
        {
          "versions": [
            {
              "id": "version-id-1",
              "prompt_id": "some-prompt-id",
              "version": 1,
              "created_at": "2024-01-01T12:00:00Z"
            },
            {
              "id": "version-id-2",
              "prompt_id": "some-prompt-id",
              "version": 2,
              "created_at": "2024-01-02T12:00:00Z"
            }
          ],
          "total": 2
        }
        ```

### Get Specific Prompt Version

-   **Endpoint:** `GET /prompts/{prompt_id}/versions/{version_number}`
-   **Description:** Retrieves the content of a specific version of a prompt.
-   **Success Response:**
    -   **Code:** `200 OK`
    -   **Content:**
        ```json
        {
          "id": "version-id-1",
          "prompt_id": "some-prompt-id",
          "version": 1,
          "content": "The content of version 1.",
          "created_at": "2024-01-01T12:00:00Z"
        }
        ```

### Revert to a Previous Version

-   **Endpoint:** `POST /prompts/{prompt_id}/revert`
-   **Description:** Reverts a prompt to a previous version. This creates a new version that is a copy of the selected historical version.
-   **Request Body:**
    ```json
    {
      "version_to_revert_to": 1
    }
    ```
-   **Success Response:**
    -   **Code:** `201 Created`
    -   **Content:** The new, reverted prompt object.

## 5. Edge Cases

-   **Deleting a prompt:** When a prompt is deleted, all its historical versions should also be deleted.
-   **Initial prompt creation:** When a new prompt is created, it should automatically get a version number of 1.
-   **Invalid version number:** Requests for non-existent version numbers should return a `404 Not Found` error.
-   **Reverting to the latest version:** If a user tries to revert to the current latest version, the API should handle this gracefully (e.g., by returning a `400 Bad Request` or simply doing nothing).
