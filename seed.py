from app import app, db, Post

samples = [
    ("The art of starting small", "the-art-of-starting-small", "Why the smallest beginnings often lead to the biggest ideas.", "Every meaningful project begins with a first step.\n\nStart with one clear idea, build something useful, and improve it through feedback. Progress comes from consistency, not perfection.", "Mindset"),
    ("Designing for the everyday", "designing-for-the-everyday", "Thoughtful details make digital experiences feel effortless.", "Good design starts by listening.\n\nFocus on readability, predictable navigation, and the small moments that make a product feel welcoming.", "Design"),
    ("A quieter way to build", "a-quieter-way-to-build", "A few lessons on focus, curiosity, and making things that last.", "You do not need every feature on day one.\n\nBuild the essential experience first, test it with real people, and leave room to grow.", "Development"),
]
with app.app_context():
    for title, slug, excerpt, content, category in samples:
        if not db.session.query(Post).filter_by(slug=slug).first():
            db.session.add(Post(title=title, slug=slug, excerpt=excerpt, content=content, category=category))
    db.session.commit()
print("Seed data ready")
