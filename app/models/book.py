from datetime import datetime
from app import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100))
    description = db.Column(db.Text)
    cover_image = db.Column(db.String(200))
    file_path = db.Column(db.String(200), nullable=False)
    file_type = db.Column(db.String(10), nullable=False)  # PDF or EPUB
    total_pages = db.Column(db.Integer)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    category = db.Column(db.String(50))
    language = db.Column(db.String(20))
    accessible_without_login = db.Column(db.Boolean, default=False)  # New column to indicate public access
    
    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationships
    reading_progress = db.relationship('ReadingProgress', backref='book', lazy=True)
    bookmarks = db.relationship('Bookmark', backref='book', lazy=True)
    reviews = db.relationship('Review', backref='book', lazy=True)

    def __repr__(self):
        return f'<Book {self.title}>'

    @property
    def average_rating(self):
        if not self.reviews:
            return 0
        return sum(review.rating for review in self.reviews) / len(self.reviews)
