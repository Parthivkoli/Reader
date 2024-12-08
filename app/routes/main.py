from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from app.models import Book, ReadingProgress
from app.utils.api_client import OpenLibraryAPI, GoogleBooksAPI, InternetArchiveAPI
from app.utils.scraper import OpenLibraryScraper, GutenbergScraper, GoodreadsScraper

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    featured_books = Book.query.limit(6).all()
    public_books = Book.query.filter_by(category='Public', accessible_without_login=True).limit(6).all()
    
    # Get trending books from different sources
    trending_query = "trending books"
    openlibrary_books = OpenLibraryScraper.search_books(trending_query)[:4]
    goodreads_books = GoodreadsScraper.search_books(trending_query)[:4]
    gutenberg_books = GutenbergScraper.search_books(trending_query)[:4]
    
    scraped_books = {
        'OpenLibrary': openlibrary_books,
        'Goodreads': goodreads_books,
        'Gutenberg': gutenberg_books
    }
    
    return render_template('main/index.html', 
                         featured_books=featured_books, 
                         public_books=public_books,
                         scraped_books=scraped_books)

@main_bp.route('/dashboard')
@login_required
def dashboard():
    user_books = Book.query.filter_by(user_id=current_user.id).all()
    reading_progress = ReadingProgress.query.filter_by(user_id=current_user.id).all()
    return render_template('main/dashboard.html', 
                         books=user_books, 
                         reading_progress=reading_progress)

@main_bp.route('/discover')
def discover():
    books = Book.query.all()
    return render_template('main/discover.html', books=books)

@main_bp.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')
    openlibrary_results = OpenLibraryScraper.search_books(query)
    gutenberg_results = GutenbergScraper.search_books(query)
    goodreads_results = GoodreadsScraper.search_books(query)

    # Combine results from all sources
    all_results = {
        'openlibrary': openlibrary_results,
        'gutenberg': gutenberg_results,
        'goodreads': goodreads_results
    }
    return render_template('main/search_results.html', 
                           openlibrary_results=openlibrary_results,
                           gutenberg_results=gutenberg_results,
                           all_results=all_results)
