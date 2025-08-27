# Typesense Demo

Proof of concept for full text search using [Typesense](https://github.com/typesense/typesense) and Django REST Framework.

## Architecture

```
client --> Django API --> Typesense
                           ↑
                        dataset
```

* **Django/DRF** – exposes `/api/search/?q=...` and `/api/import/` endpoints
* **Typesense** – stores book documents and performs full‑text search with highlighting
* **Dataset** – small collection of public‑domain book excerpts stored in `data/books.jsonl`; additional PDFs placed in `data/pdfs/` are indexed automatically

## Requirements

* Docker & Docker Compose
* Make

## Usage

1. Build images and start services:
   ```bash
   make build
   make up
   ```
2. Index sample books into Typesense:
   ```bash
   make index
   ```
3. Import a new PDF book (optional):
   ```bash
   curl -F "file=@path/to/book.pdf" \
        -F "title=Custom Title" \
        http://localhost:8000/api/import/
   ```
4. Query the API:
   ```bash
   curl 'http://localhost:8000/api/search/?q=Alice'
   ```

Each result contains a book ID, title and snippet with the matching text highlighted by `<mark>` tags.

## References

* [Typesense Documentation](https://typesense.org/docs/)
* [Django REST Framework](https://www.django-rest-framework.org/)
