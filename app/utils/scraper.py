import requests
from bs4 import BeautifulSoup

class OpenLibraryScraper:
    BASE_URL = 'https://openlibrary.org'

    @staticmethod
    def search_books(query):
        search_url = f'{OpenLibraryScraper.BASE_URL}/search.json?q={query}'
        try:
            response = requests.get(search_url)
            if response.status_code == 200:
                data = response.json()
                books = []
                for doc in data.get('docs', []):
                    books.append({
                        'title': doc.get('title', 'Unknown'),
                        'author': ', '.join(doc.get('author_name', ['Unknown'])),
                        'cover': f'https://covers.openlibrary.org/b/id/{doc.get("cover_i", "")}-L.jpg' if doc.get('cover_i') else None,
                        'link': f'{OpenLibraryScraper.BASE_URL}/works/{doc.get("key")}'
                    })
                return books
            print("OpenLibrary Search Failed")  # Debug log
        except Exception as e:
            print(f"Error in OpenLibraryScraper: {e}")
        return []

class GutenbergScraper:
    BASE_URL = 'https://www.gutenberg.org'

    @staticmethod
    def search_books(query):
        search_url = f'{GutenbergScraper.BASE_URL}/ebooks/search/?query={query}'
        try:
            response = requests.get(search_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                books = []
                for result in soup.select('.booklink'):
                    title = result.select_one('.title').text
                    author = result.select_one('.subtitle').text if result.select_one('.subtitle') else 'Unknown'
                    cover = result.select_one('img')['src'] if result.select_one('img') else None
                    link = GutenbergScraper.BASE_URL + result.select_one('a')['href']
                    books.append({
                        'title': title,
                        'author': author,
                        'cover': cover,
                        'link': link
                    })
                return books
            print("Gutenberg Search Failed")  # Debug log
        except Exception as e:
            print(f"Error in GutenbergScraper: {e}")
        return []

class GoodreadsScraper:
    BASE_URL = 'https://www.goodreads.com'

    @staticmethod
    def search_books(query):
        search_url = f'{GoodreadsScraper.BASE_URL}/search?q={query}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        try:
            response = requests.get(search_url, headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                books = []
                for result in soup.select('tr[itemtype="http://schema.org/Book"]'):
                    title_element = result.select_one('.bookTitle')
                    author_element = result.select_one('.authorName')
                    cover_element = result.select_one('img.bookCover')
                    if title_element and author_element:
                        books.append({
                            'title': title_element.text.strip(),
                            'author': author_element.text.strip(),
                            'cover': cover_element['src'] if cover_element else None,
                            'link': GoodreadsScraper.BASE_URL + title_element['href']
                        })
                return books
            print("Goodreads Search Failed")  # Debug log
        except Exception as e:
            print(f"Error in GoodreadsScraper: {e}")
        return []

class GoogleBooksScraper:
    BASE_URL = 'https://www.googleapis.com/books/v1/volumes'

    @staticmethod
    def search_books(query, api_key):
        search_url = f'{GoogleBooksScraper.BASE_URL}?q={query}&key={api_key}'
        try:
            response = requests.get(search_url)
            if response.status_code == 200:
                data = response.json()
                books = []
                for item in data.get('items', []):
                    volume_info = item.get('volumeInfo', {})
                    books.append({
                        'title': volume_info.get('title', 'Unknown'),
                        'author': ', '.join(volume_info.get('authors', ['Unknown'])),
                        'cover': volume_info.get('imageLinks', {}).get('thumbnail'),
                        'link': volume_info.get('infoLink')
                    })
                return books
            print("GoogleBooks Search Failed")  # Debug log
        except Exception as e:
            print(f"Error in GoogleBooksScraper: {e}")
        return []

class BookDepositoryScraper:
    BASE_URL = 'https://www.bookdepository.com'

    @staticmethod
    def search_books(query):
        search_url = f'{BookDepositoryScraper.BASE_URL}/search?searchTerm={query}'
        try:
            response = requests.get(search_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                books = []
                for result in soup.select('.book-item'):
                    title = result.select_one('.title').text.strip()
                    author = result.select_one('.author').text.strip() if result.select_one('.author') else 'Unknown'
                    cover = result.select_one('img')['data-lazy'] if result.select_one('img') else None
                    link = BookDepositoryScraper.BASE_URL + result.select_one('.title')['href']
                    books.append({
                        'title': title,
                        'author': author,
                        'cover': cover,
                        'link': link
                    })
                return books
            print("BookDepository Search Failed")  # Debug log
        except Exception as e:
            print(f"Error in BookDepositoryScraper: {e}")
        return []

# Example usage
if __name__ == '__main__':
    query = "Harry Potter"

    # OpenLibrary
    print("OpenLibrary Results:", OpenLibraryScraper.search_books(query))

    # Gutenberg
    print("Gutenberg Results:", GutenbergScraper.search_books(query))

    # Goodreads
    print("Goodreads Results:", GoodreadsScraper.search_books(query))

    # Google Books (requires API key)
    # api_key = 'YOUR_GOOGLE_API_KEY'
    # print("Google Books Results:", GoogleBooksScraper.search_books(query, api_key))

    # Book Depository
    print("Book Depository Results:", BookDepositoryScraper.search_books(query))
