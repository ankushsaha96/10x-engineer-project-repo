# PromptLab API Reference

Welcome to the PromptLab API documentation. This reference provides detailed information about all available endpoints, including request/response examples and error handling.

## Authentication

The PromptLab API is currently open and does not require authentication. However, authentication will be implemented in a future version.

## API Version

The current API version is **1.0.0**.

## Base URL

All API endpoints are relative to the following base URL:

```
http://127.0.0.1:8000
```

---

## Endpoints

This section provides detailed information about each API endpoint, including the request format, response examples, and potential errors.

### Health Check

-   **Endpoint:** `GET /health`
-   **Description:** Performs a basic health check for the API, returning the current API version and health status.
-   **Request:**
    -   **Method:** `GET`
    -   **URL:** `/health`
    -   **Headers:** `Content-Type: application/json`
-   **Success Response:**
    -   **Code:** `200 OK`
    -   **Content:**
        ```json
        {
          "status": "healthy",
          "version": "1.0.0"
        }
        ```

---

### Prompts

#### List Prompts

-   **Endpoint:** `GET /prompts`
-   **Description:** Retrieves a list of prompts, with optional filtering by collection and search query.
-   **Query Parameters:**
    -   `collection_id` (optional, string): The ID of the collection to filter prompts by.
    -   `search` (optional, string): A search query to filter prompts by.
-   **Request:**
    -   **Method:** `GET`
    -   **URL:** `/prompts?collection_id=some-collection-id&search=some-query`
    -   **Headers:** `Content-Type: application/json`
-   **Success Response:**
    -   **Code:** `200 OK`
    -   **Content:**
        ```json
        {
          "prompts": [
            {
              "id": "some-prompt-id",
              "title": "My Prompt",
              "content": "This is my prompt.",
              "description": "This is a description.",
              "collection_id": "some-collection-id",
              "created_at": "2024-01-01T12:00:00Z",
              "updated_at": "2024-01-01T12:00:00Z"
            }
          ],
          "total": 1
        }
        ```

#### Get Prompt

-   **Endpoint:** `GET /prompts/{prompt_id}`
-   **Description:** Retrieves a specific prompt by its ID.
-   **Request:**
    -   **Method:** `GET`
    -   **URL:** `/prompts/some-prompt-id`
    -   **Headers:** `Content-Type: application/json`
-   **Success Response:**
    -   **Code:** `200 OK`
    -   **Content:**
        ```json
        {
          "id": "some-prompt-id",
          "title": "My Prompt",
          "content": "This is my prompt.",
          "description": "This is a description.",
          "collection_id": "some-collection-id",
          "created_at": "2024-01-01T12:00:00Z",
          "updated_at": "2024-01-01T12:00:00Z"
        }
        ```
-   **Error Response:**
    -   **Code:** `404 Not Found`
    -   **Content:**
        ```json
        {
          "detail": "Prompt not found"
        }
        ```

#### Create Prompt

-   **Endpoint:** `POST /prompts`
-   **Description:** Creates a new prompt.
-   **Request:**
    -   **Method:** `POST`
    -   **URL:** `/prompts`
    -   **Headers:** `Content-Type: application/json`
    -   **Body:**
        ```json
        {
          "title": "My Prompt",
          "content": "This is my prompt.",
          "description": "This is a description.",
          "collection_id": "some-collection-id"
        }
        ```
-   **Success Response:**
    -   **Code:** `201 Created`
    -   **Content:**
        ```json
        {
          "id": "new-prompt-id",
          "title": "My Prompt",
          "content": "This is my prompt.",
          "description": "This is a description.",
          "collection_id": "some-collection-id",
          "created_at": "2024-01-01T12:00:00Z",
          "updated_at": "2024-01-01T12:00:00Z"
        }
        ```
-   **Error Response:**
    -   **Code:** `400 Bad Request`
    -   **Content:**
        ```json
        {
          "detail": "Collection not found"
        }
        ```

#### Update Prompt

-   **Endpoint:** `PUT /prompts/{prompt_id}`
-   **Description:** Updates an existing prompt.
-   **Request:**
    -   **Method:** `PUT`
    -   **URL:** `/prompts/some-prompt-id`
    -   **Headers:** `Content-Type: application/json`
    -   **Body:**
        ```json
        {
          "title": "Updated Prompt Title",
          "content": "Updated prompt content.",
          "description": "Updated prompt description.",
          "collection_id": "some-collection-id"
        }
        ```
-   **Success Response:**
    -   **Code:** `200 OK`
    -   **Content:**
        ```json
        {
          "id": "some-prompt-id",
          "title": "Updated Prompt Title",
          "content": "Updated prompt content.",
          "description": "Updated prompt description.",
          "collection_id": "some-collection-id",
          "created_at": "2024-01-01T12:00:00Z",
          "updated_at": "2024-01-02T12:00:00Z"
        }
        ```
-   **Error Responses:**
    -   **Code:** `404 Not Found`
    -   **Content:**
        ```json
        {
          "detail": "Prompt not found"
        }
        ```
    -   **Code:** `400 Bad Request`
    -   **Content:**
        ```json
        {
          "detail": "Collection not found"
        }
        ```

#### Patch Prompt

-   **Endpoint:** `PATCH /prompts/{prompt_id}`
-   **Description:** Partially updates an existing prompt.
-   **Request:**
    -   **Method:** `PATCH`
    -   **URL:** `/prompts/some-prompt-id`
    -   **Headers:** `Content-Type: application/json`
    -   **Body:**
        ```json
        {
          "title": "Updated Prompt Title"
        }
        ```
-   **Success Response:**
    -   **Code:** `200 OK`
    -   **Content:**
        ```json
        {
          "id": "some-prompt-id",
          "title": "Updated Prompt Title",
          "content": "This is my prompt.",
          "description": "This is a description.",
          "collection_id": "some-collection-id",
          "created_at": "2024-01-01T12:00:00Z",
          "updated_at": "2024-01-02T12:00:00Z"
        }
        ```
-   **Error Responses:**
    -   **Code:** `404 Not Found`
    -   **Content:**
        ```json
        {
          "detail": "Prompt not found"
        }
        ```
    -   **Code:** `400 Bad Request`
    -   **Content:**
        ```json
        {
          "detail": "Collection not found"
        }
        ```

#### Delete Prompt

-   **Endpoint:** `DELETE /prompts/{prompt_id}`
-   **Description:** Deletes a prompt by its ID.
-   **Request:**
    -   **Method:** `DELETE`
    -   **URL:** `/prompts/some-prompt-id`
-   **Success Response:**
    -   **Code:** `204 No Content`
-   **Error Response:**
    -   **Code:** `404 Not Found`
    -   **Content:**
        ```json
        {
          "detail": "Prompt not found"
        }
        ```

---

### Collections

#### List Collections

-   **Endpoint:** `GET /collections`
-   **Description:** Retrieves a list of all collections.
-   **Request:**
    -   **Method:** `GET`
    -   **URL:** `/collections`
    -   **Headers:** `Content-Type: application/json`
-   **Success Response:**
    -   **Code:** `200 OK`
    -   **Content:**
        ```json
        {
          "collections": [
            {
              "id": "some-collection-id",
              "name": "My Collection"
            }
          ],
          "total": 1
        }
        ```

#### Get Collection

-   **Endpoint:** `GET /collections/{collection_id}`
-   **Description:** Retrieves a specific collection by its ID.
-   **Request:**
    -   **Method:** `GET`
    -   **URL:** `/collections/some-collection-id`
    -   **Headers:** `Content-Type: application/json`
-   **Success Response:**
    -   **Code:** `200 OK`
    -   **Content:**
        ```json
        {
          "id": "some-collection-id",
          "name": "My Collection"
        }
        ```
-   **Error Response:**
    -   **Code:** `404 Not Found`
    -   **Content:**
        ```json
        {
          "detail": "Collection not found"
        }
        ```

#### Create Collection

-   **Endpoint:** `POST /collections`
-   **Description:** Creates a new collection.
-   **Request:**
    -   **Method:** `POST`
    -   **URL:** `/collections`
    -   **Headers:** `Content-Type: application/json`
    -   **Body:**
        ```json
        {
          "name": "My New Collection"
        }
        ```
-   **Success Response:**
    -   **Code:** `201 Created`
    -   **Content:**
        ```json
        {
          "id": "new-collection-id",
          "name": "My New Collection"
        }
        ```

#### Delete Collection

-   **Endpoint:** `DELETE /collections/{collection_id}`
-   **Description:** Deletes a collection by its ID.
-   **Request:**
    -   **Method:** `DELETE`
    -   **URL:** `/collections/some-collection-id`
-   **Success Response:**
    -   **Code:** `204 No Content`
-   **Error Response:**
    -   **Code:** `404 Not Found`
    -   **Content:**
        ```json
        {
          "detail": "Collection not found"
        }
        ```

---

## Error Responses

In case of an error, the API will return a JSON object with a `detail` key containing a description of the error.

**Example:**

```json
{
  "detail": "Error message"
}
```