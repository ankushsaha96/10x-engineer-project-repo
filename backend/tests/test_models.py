from app.models import Prompt, Tag


def test_create_prompt_with_tags():
    prompt = Prompt(
        id="test-prompt",
        title="Test Prompt",
        content="This is a test prompt.",
        tags=["test-tag-1", "test-tag-2"],
    )
    assert prompt.tags == ["test-tag-1", "test-tag-2"]

def test_create_tag():
    tag = Tag(id="test-tag", name="Test Tag")
    assert tag.id == "test-tag"
    assert tag.name == "Test Tag"
