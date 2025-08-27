# Typesense Demo

Proof of concept for full text search using [Typesense](https://github.com/typesense/typesense) and Django REST Framework.

## Architecture

```
client --> Django API --> Typesense
                           ↑
                        dataset
```

* **Django/DRF** – exposes `/api/search/?q=...` endpoint
* **Typesense** – stores book documents and performs full‑text search with highlighting
* **Dataset** – small collection of public‑domain book excerpts stored in `data/books.jsonl`

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
3. Query the API:
   ```bash
   curl 'http://localhost:8000/api/search/?q=Alice'
   ```

Each result contains a book ID, title and snippet with the matching text highlighted by `<mark>` tags.

## References

* [Typesense Documentation](https://typesense.org/docs/)
* [Django REST Framework](https://www.django-rest-framework.org/)
