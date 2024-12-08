import os
from flask import Blueprint, render_template, request, jsonify, current_app, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.models import Book, ReadingProgress, Bookmark, Review
from app import db
from app.utils.file_handler import process_book_file, allowed_file

books_bp = Blueprint('books', __name__)

@books_bp.route('/books/upload', methods=['GET', 'POST'])
@login_required
def upload_book():
    if request.method == 'POST':
        if 'book_file' not in request.files:
            flash('No file selected', 'danger')
            return redirect(request.url)
            
        file = request.files['book_file']
        if file.filename == '':
            flash('No file selected', 'danger')
            return redirect(request.url)
            
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            book_info = process_book_file(filepath)
            
            book = Book(
                title=request.form.get('title', book_info.get('title', filename)),
                author=request.form.get('author', book_info.get('author', 'Unknown')),
                description=request.form.get('description', ''),
                file_path=filepath,
                file_type=os.path.splitext(filename)[1][1:].upper(),
                total_pages=book_info.get('total_pages', 0),
                user_id=current_user.id
            )
            
            db.session.add(book)
            db.session.commit()
            
            flash('Book uploaded successfully!', 'success')
            return redirect(url_for('books.view_book', book_id=book.id))
            
    return render_template('books/upload.html')

@books_bp.route('/books/<int:book_id>')
def view_book(book_id):
    book = Book.query.get_or_404(book_id)
    if current_user.is_authenticated:
        progress = ReadingProgress.query.filter_by(
            user_id=current_user.id,
            book_id=book_id
        ).first()
    else:
        progress = None
    return render_template('books/view.html', book=book, progress=progress)

@books_bp.route('/books/<int:book_id>/read')
@login_required
def read_book(book_id):
    book = Book.query.get_or_404(book_id)
    progress = ReadingProgress.query.filter_by(
        user_id=current_user.id,
        book_id=book_id
    ).first()
    
    if not progress:
        progress = ReadingProgress(user_id=current_user.id, book_id=book_id)
        db.session.add(progress)
        db.session.commit()
        
    return render_template('books/reader.html', book=book, progress=progress)

@books_bp.route('/api/books/<int:book_id>/progress', methods=['POST'])
@login_required
def update_progress(book_id):
    data = request.get_json()
    progress = ReadingProgress.query.filter_by(
        user_id=current_user.id,
        book_id=book_id
    ).first()
    
    if progress:
        progress.update_progress(
            current_page=data['current_page'],
            total_pages=data['total_pages']
        )
        db.session.commit()
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error'}), 404

@books_bp.route('/api/books/<int:book_id>/bookmark', methods=['POST'])
@login_required
def add_bookmark(book_id):
    data = request.get_json()
    bookmark = Bookmark(
        user_id=current_user.id,
        book_id=book_id,
        page_number=data['page_number'],
        note=data.get('note', '')
    )
    db.session.add(bookmark)
    db.session.commit()
    return jsonify({'status': 'success', 'id': bookmark.id})

@books_bp.route('/api/books/<int:book_id>/review', methods=['POST'])
@login_required
def add_review(book_id):
    data = request.get_json()
    review = Review(
        user_id=current_user.id,
        book_id=book_id,
        rating=data['rating'],
        comment=data.get('comment', '')
    )
    db.session.add(review)
    db.session.commit()
    return jsonify({'status': 'success', 'id': review.id})
