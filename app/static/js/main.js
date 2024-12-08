// Dark Mode Toggle
document.addEventListener('DOMContentLoaded', function() {
    const darkModeToggle = document.getElementById('darkModeToggle');
    
    if (darkModeToggle) {
        darkModeToggle.addEventListener('change', function() {
            // Send Dark Mode Preference to Server
            updateDarkModePreference(this.checked)
                .then((data) => {
                    if (data.status === 'success') {
                        document.body.classList.toggle('dark-mode');
                    }
                })
                .catch((error) => {
                    console.error('Error updating dark mode:', error);
                });
        });
    }
});

// Function to Update Dark Mode Preference
function updateDarkModePreference(isDarkMode) {
    return fetch('/settings', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ dark_mode: isDarkMode }),
    })
    .then(response => response.json())
    .catch((error) => {
        console.error('Error updating dark mode preference:', error);
        throw error;
    });
}

// Book Reader Class
class BookReader {
    constructor(containerId, bookId) {
        this.container = document.getElementById(containerId);
        this.bookId = bookId;
        this.currentPage = 1;
        this.totalPages = 1;
        this.zoom = 100;
        
        this.initializeControls();
        this.loadCurrentPage();
    }

    initializeControls() {
        // Navigation controls
        this.addEventListenerToElement('prevPage', this.prevPage.bind(this));
        this.addEventListenerToElement('nextPage', this.nextPage.bind(this));
        this.addEventListenerToElement('pageNumber', this.handlePageChange.bind(this), 'change');
        
        // Zoom controls
        this.addEventListenerToElement('zoomIn', this.zoomIn.bind(this));
        this.addEventListenerToElement('zoomOut', this.zoomOut.bind(this));
        
        // Bookmark control
        this.addEventListenerToElement('addBookmark', this.addBookmark.bind(this));
    }

    addEventListenerToElement(elementId, eventHandler, eventType = 'click') {
        const element = document.getElementById(elementId);
        if (element) {
            element.addEventListener(eventType, eventHandler);
        }
    }

    loadCurrentPage() {
        if (!this.container) return;

        fetch(`/api/books/${this.bookId}/page/${this.currentPage}`)
            .then(response => response.json())
            .then(data => {
                this.container.innerHTML = data.content;
                this.totalPages = data.total_pages;  // Update total pages from response
                this.updateProgress();
            })
            .catch((error) => {
                console.error('Error loading page:', error);
            });
    }

    prevPage() {
        if (this.currentPage > 1) {
            this.currentPage--;
            this.loadCurrentPage();
        }
    }

    nextPage() {
        if (this.currentPage < this.totalPages) {
            this.currentPage++;
            this.loadCurrentPage();
        }
    }

    handlePageChange(event) {
        const pageNum = parseInt(event.target.value);
        if (pageNum >= 1 && pageNum <= this.totalPages) {
            this.currentPage = pageNum;
            this.loadCurrentPage();
        }
    }

    zoomIn() {
        this.zoom = Math.min(this.zoom + 10, 200);
        this.updateZoom();
    }

    zoomOut() {
        this.zoom = Math.max(this.zoom - 10, 50);
        this.updateZoom();
    }

    updateZoom() {
        if (this.container) {
            this.container.style.zoom = `${this.zoom}%`;
        }
    }

    updateProgress() {
        const progress = (this.currentPage / this.totalPages) * 100;

        fetch(`/api/books/${this.bookId}/progress`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                current_page: this.currentPage,
                total_pages: this.totalPages
            })
        }).catch((error) => {
            console.error('Error updating progress:', error);
        });

        // Update UI Progress Bar
        const progressBar = document.getElementById('readingProgress');
        if (progressBar) {
            progressBar.style.width = `${progress}%`;
            progressBar.setAttribute('aria-valuenow', progress);
        }
    }

    addBookmark() {
        const note = prompt('Add a note to this bookmark (optional):');
        
        fetch(`/api/books/${this.bookId}/bookmark`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                page_number: this.currentPage,
                note: note
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('Bookmark added successfully!');
            }
        })
        .catch((error) => {
            console.error('Error adding bookmark:', error);
        });
    }
}

// Book Search and Filtering with Debounce
document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('searchForm');
    
    if (searchForm) {
        let timeout;
        const debounceSearch = function() {
            clearTimeout(timeout);
            timeout = setTimeout(() => {
                const searchQuery = document.getElementById('searchQuery').value;
                const category = document.getElementById('categoryFilter').value;

                fetch(`/discover?search=${searchQuery}&category=${category}`)
                    .then(response => response.text())
                    .then(html => {
                        document.getElementById('bookResults').innerHTML = html;
                    })
                    .catch((error) => {
                        console.error('Error fetching search results:', error);
                    });
            }, 500); // Adjust delay as needed (500ms for debounce)
        };

        searchForm.addEventListener('input', debounceSearch);  // Trigger on input change
    }
});
