import os
from datetime import datetime, timezone
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

db = SQLAlchemy()

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    slug = db.Column(db.String(180), nullable=False, unique=True)
    excerpt = db.Column(db.String(300), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(60), nullable=False, default="General")
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {"id": self.id, "title": self.title, "slug": self.slug,
                "excerpt": self.excerpt, "content": self.content, "category": self.category,
                "created_at": self.created_at.isoformat()}

def create_app(config=None):
    app = Flask(__name__)
    database_url = os.getenv("DATABASE_URL", "sqlite:///blog.db")
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    app.config.update(SQLALCHEMY_DATABASE_URI=database_url, SQLALCHEMY_TRACK_MODIFICATIONS=False)
    if config:
        app.config.update(config)
    db.init_app(app)
    CORS(app, origins=os.getenv("FRONTEND_URL", "http://localhost:3000").split(","))

    @app.get("/api/health")
    def health():
        return jsonify(status="ok")

    @app.get("/api/posts")
    def list_posts():
        category = request.args.get("category")
        stmt = select(Post).order_by(Post.created_at.desc(), Post.id.desc())
        if category:
            stmt = stmt.where(Post.category == category)
        return jsonify([p.to_dict() for p in db.session.scalars(stmt).all()])

    @app.get("/api/posts/<slug>")
    def get_post(slug):
        post = db.session.scalar(select(Post).where(Post.slug == slug))
        return (jsonify(post.to_dict()), 200) if post else (jsonify(error="Article not found"), 404)

    @app.post("/api/posts")
    def create_post():
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify(error="A JSON object is required"), 400
        required = ("title", "slug", "excerpt", "content", "category")
        if any(not isinstance(data.get(k), str) or not data[k].strip() for k in required):
            return jsonify(error="All fields are required"), 400
        import re
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", data["slug"]):
            return jsonify(error="Slug must contain lowercase letters, numbers and hyphens"), 400
        limits = {"title": 160, "slug": 180, "excerpt": 300, "category": 60}
        if any(len(data[k]) > limit for k, limit in limits.items()):
            return jsonify(error="One or more fields exceed the length limit"), 400
        post = Post(**{k: data[k].strip() for k in required})
        db.session.add(post)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return jsonify(error="This slug already exists"), 409
        return jsonify(post.to_dict()), 201

    with app.app_context():
        db.create_all()
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
