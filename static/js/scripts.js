// scripts.js
function showBookDetails(book) {
    document.getElementById('modal-book-cover').src = book.cover_url || 'https://via.placeholder.com/100x150';
    document.getElementById('modal-book-title').textContent = book.title;
    document.getElementById('modal-book-author').textContent = "Autor: " + book.author;
    document.getElementById('modal-book-description').textContent = book.description || 'Descrição não disponível.';
    document.getElementById('modal-whatsapp-link').href = "https://wa.me/55" + book.whatsapp;
    $('#bookDetailsModal').modal('show');
}

async function deleteBook(bookId) {
    try {
        const response = await fetch(`/delete_book/${bookId}`, {
            method: 'DELETE',
        });

        if (response.ok) {
            alert('Livro excluído com sucesso!');
            location.reload();
        } else {
            const data = await response.text();
            alert('Erro: ' + data);
        }
    } catch (error) {
        console.error('Erro ao tentar excluir o livro:', error);
        alert('Erro ao tentar excluir o livro.');
    }
}

function confirmDelete(bookId, event) {
    event.stopPropagation();
    if (confirm("Tem certeza de que deseja excluir este anúncio?")) {
        deleteBook(bookId);
    }
}

document.getElementById('addBookBtn').onclick = function() {
    $('#addBookModal').modal('show');
};

async function searchBooks(query) {
    const response = await fetch(`https://www.googleapis.com/books/v1/volumes?q=${query}&maxResults=5`);
    const data = await response.json();
    return data.items || [];
}

document.getElementById('bookTitle').addEventListener('input', async function() {
    const query = this.value;
    const autocompleteList = document.getElementById('autocomplete-list');
    autocompleteList.innerHTML = '';

    if (query.length < 2) return;

    const books = await searchBooks(query);
    books.forEach(book => {
        const title = book.volumeInfo.title;
        const authors = book.volumeInfo.authors ? book.volumeInfo.authors.join(', ') : 'Desconhecido';
        const coverUrl = book.volumeInfo.imageLinks ? book.volumeInfo.imageLinks.thumbnail : 'https://via.placeholder.com/50x75';
        const description = book.volumeInfo.description;

        const item = document.createElement('div');
        item.className = 'autocomplete-item';
        item.style.display = 'flex';
        item.style.alignItems = 'center';
        item.style.marginBottom = '5px';

        item.innerHTML = `
            <img src="${coverUrl}" alt="Capa do Livro" style="width: 50px; height: 75px; object-fit: cover; margin-right: 10px;">
            <div>
                <strong>${title}</strong><br>
                <small>Autor: ${authors}</small>
            </div>
        `;

        item.onclick = () => {
            document.getElementById('bookTitle').value = title;
            document.getElementById('bookAuthor').value = authors;
            document.getElementById('coverUrl').value = coverUrl;
            document.getElementById('description').value = description;
            autocompleteList.innerHTML = '';
        };
        autocompleteList.appendChild(item);
    });
});

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('addBookForm').onsubmit = async function(event) {
        event.preventDefault();

        const formData = new FormData(this);

        try {
            const response = await fetch('/add_book', {
                method: 'POST',
                body: formData,
            });

            const data = await response.json();

            if (response.ok) {
                alert(data.success);
                $('#addBookModal').modal('hide');
                location.reload();
            } else {
                console.error('Erro:', data.error);
                alert('Erro: ' + data.error);
            }
        } catch (error) {
            console.error('Erro de rede:', error);
            alert('Erro de rede ao tentar adicionar o livro.');
        }
    };
});
