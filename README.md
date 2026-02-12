# PromptLab

PromptLab is a full-stack application for managing and engineering AI prompts. It provides a backend API and a React-based frontend to create, organize, and test prompts for various AI models.

## Project Overview and Purpose

This project is designed to be a comprehensive platform for prompt engineers and developers working with AI. It allows users to:
- Create and store AI prompts.
- Organize prompts into collections.
- Search and filter prompts.
- Version and iterate on prompts. (Future feature)
- Test prompts against different models. (Future feature)

The goal is to provide a robust and user-friendly tool to streamline the prompt engineering workflow.

## Features

- **Prompt Management:** Full CRUD (Create, Read, Update, Delete) operations for prompts.
- **Collection Management:** Organize prompts into collections.
- **Search:** Full-text search for prompts by title and content.
- **Filtering:** Filter prompts by collection.
- **Health Check:** An endpoint to verify API status.
- **CORS Enabled:** Ready for frontend integration.

## Prerequisites and Installation

### Prerequisites

- Python 3.10+
- [Poetry](https://python-poetry.org/) for managing Python dependencies (optional but recommended)
- Node.js 18+ and npm (for frontend)
- Docker and Docker Compose (for containerized setup)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/promptlab.git
    cd promptlab
    ```

2.  **Backend Setup:**
    ```bash
    cd backend
    pip install -r requirements.txt
    ```

3.  **Frontend Setup:**
    ```bash
    cd ../frontend
    npm install
    ```

## Quick Start Guide

### Running the Backend

1.  Navigate to the `backend` directory:
    ```bash
    cd backend
    ```

2.  Start the FastAPI server:
    ```bash
    python main.py
    ```
    The API will be available at `http://localhost:8000`. You can access the OpenAPI documentation at `http://localhost:8000/docs`.

### Running the Frontend

1.  Navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```

2.  Start the React development server:
    ```bash
    npm run dev
    ```
    The frontend will be available at `http://localhost:5173`.

### Using Docker

You can also run the entire application using Docker Compose.

1.  Ensure Docker is running.
2.  From the project root, run:
    ```bash
    docker-compose up --build
    ```
    This will build the containers and start both the backend and frontend services.

## API Endpoint Summary

All endpoints are prefixed with `/`.

| Method | Endpoint | Description | Example Request Body/Params |
| --- | --- | --- | --- |
| `GET` | `/health` | Check API health | |
| `GET` | `/prompts` | List all prompts | `?collection_id=<id>&search=<query>` |
| `POST` | `/prompts` | Create a new prompt | `{ "title": "...", "content": "..." }` |
| `GET` | `/prompts/{prompt_id}` | Get a single prompt | |
| `PUT` | `/prompts/{prompt_id}` | Update a prompt | `{ "title": "...", "content": "..." }` |
| `PATCH`| `/prompts/{prompt_id}` | Partially update a prompt | `{ "title": "..." }` |
| `DELETE`| `/prompts/{prompt_id}` | Delete a prompt | |
| `GET` | `/collections`| List all collections | |
| `POST` | `/collections`| Create a new collection | `{ "name": "..." }` |
| `GET` | `/collections/{collection_id}` | Get a single collection | |
| `DELETE`| `/collections/{collection_id}` | Delete a collection | |

### Example cURL Requests

**Create a prompt:**
```bash
curl -X POST "http://localhost:8000/prompts" -H "Content-Type: application/json" -d '{"title": "My first prompt", "content": "Generate a summary of..."}'
```

**Get all prompts:**
```bash
curl "http://localhost:8000/prompts"
```

## Development Setup

This project is set up to use Visual Studio Code Dev Containers for a consistent development environment.

1.  Install the [Remote - Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension in VS Code.
2.  Open the project folder in VS Code.
3.  When prompted, click "Reopen in Container".

This will build the development container with all the necessary dependencies and configurations.

## Contributing

Contributions are welcome! Please follow these steps:

1.  Fork the repository.
2.  Create a new branch: `git checkout -b feature/your-feature-name`
3.  Make your changes and commit them: `git commit -m 'Add some feature'`
4.  Push to the branch: `git push origin feature/your-feature-name`
5.  Submit a pull request.

Please make sure to update tests as appropriate. You can run tests with `pytest` in the `backend` directory.
```bash
cd backend
pytest
```