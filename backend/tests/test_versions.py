from app.models import Prompt
from app.storage import storage

def test_create_prompt_creates_initial_version():
    prompt_data = {
        "title": "Versioned Prompt",
        "content": "This is the first version.",
        "tags": [],
    }
    prompt = Prompt(**prompt_data)
    created_prompt = storage.create_prompt(prompt)

    assert created_prompt.latest_version == 1
    versions = storage.get_prompt_versions(created_prompt.id)
    assert len(versions) == 1
    assert versions[0].version == 1
    assert versions[0].content == "This is the first version."

def test_update_prompt_creates_new_version():
    prompt_data = {
        "title": "Versioned Prompt",
        "content": "This is the first version.",
        "tags": [],
    }
    prompt = Prompt(**prompt_data)
    created_prompt = storage.create_prompt(prompt)

    updated_prompt_data = {
        "title": "Versioned Prompt",
        "content": "This is the second version.",
        "tags": [],
    }
    updated_prompt = Prompt(id=created_prompt.id, **updated_prompt_data)
    storage.update_prompt(created_prompt.id, updated_prompt)

    assert updated_prompt.latest_version == 2
    versions = storage.get_prompt_versions(created_prompt.id)
    assert len(versions) == 2
    assert versions[1].version == 2
    assert versions[1].content == "This is the second version."
