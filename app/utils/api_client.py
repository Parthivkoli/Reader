import requests

# OpenLibrary API Client
class OpenLibraryAPI:
    BASE_URL = 'https://openlibrary.org'

    @staticmethod
    def search_books(query):
        response = requests.get(f'{OpenLibraryAPI.BASE_URL}/search.json?q={query}')
        if response.status_code == 200:
            return response.json().get('docs', [])
        return []

# Google Books API Client
class GoogleBooksAPI:
    BASE_URL = 'https://www.googleapis.com/books/v1'

    @staticmethod
    def search_books(query):
        response = requests.get(f'{GoogleBooksAPI.BASE_URL}/volumes?q={query}&key=AIzaSyD3RqDH_icgyfP0lAds58VVBQ_6frPx4-s')
        if response.status_code == 200:
            return response.json().get('items', [])
        return []

# Internet Archive API Client
class InternetArchiveAPI:
    BASE_URL = 'https://archive.org'

    @staticmethod
    def search_books(query):
        response = requests.get(f'{InternetArchiveAPI.BASE_URL}/search.php?q={query}&output=json')
        if response.status_code == 200:
            return response.json().get('response', {}).get('docs', [])
        return []

# Internet Archive API Client
class InternetArchiveAPI:
    BASE_URL = 'https://archive.org'

    @staticmethod
    def search_books(query):
        response = requests.get(f'{InternetArchiveAPI.BASE_URL}/search.php?q={query}&output=json')
        if response.status_code == 200:
            return response.json().get('response', {}).get('docs', [])
        return []
