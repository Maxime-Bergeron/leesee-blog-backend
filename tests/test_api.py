import pytest
from app import create_app, db

@pytest.fixture
def client(tmp_path):
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": f"sqlite:///{tmp_path / 'test.db'}"})
    with app.test_client() as client:
        yield client
    with app.app_context():
        db.drop_all()

def example():
    return {"title": "Test post", "slug": "test-post", "excerpt": "A test excerpt", "content": "Hello world", "category": "Testing"}

def test_health(client):
    assert client.get("/api/health").json == {"status": "ok"}

def test_posts_crud_read(client):
    assert client.get("/api/posts").json == []
    response = client.post("/api/posts", json=example())
    assert response.status_code == 201
    assert response.json["title"] == "Test post"
    assert len(client.get("/api/posts").json) == 1
    assert client.get("/api/posts/test-post").json["content"] == "Hello world"
    assert len(client.get("/api/posts?category=Other").json) == 0

def test_duplicate_slug(client):
    client.post("/api/posts", json=example())
    assert client.post("/api/posts", json=example()).status_code == 409

def test_validation(client):
    assert client.post("/api/posts", json={}).status_code == 400
    assert client.post("/api/posts", json={**example(), "slug": "Invalid Slug"}).status_code == 400
    assert client.get("/api/posts/missing").status_code == 404
