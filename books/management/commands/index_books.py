import json
from pathlib import Path

import typesense
from django.conf import settings
from django.core.management.base import BaseCommand
from pdfminer.high_level import extract_text


class Command(BaseCommand):
    help = "Index books into Typesense"

    def handle(self, *args, **options):
        client = typesense.Client(settings.TYPESENSE_CONFIG)
        schema = {
            "name": "books",
            "fields": [
                {"name": "id", "type": "string"},
                {"name": "title", "type": "string"},
                {"name": "text", "type": "string"},
            ],
        }
        try:
            client.collections["books"].retrieve()
            self.stdout.write(self.style.NOTICE("Collection already exists"))
        except typesense.exceptions.ObjectNotFound:
            client.collections.create(schema)
            self.stdout.write(self.style.SUCCESS("Collection created"))

        data_path = Path(settings.BASE_DIR) / "data" / "books.jsonl"
        records = []
        with open(data_path, "r") as f:
            records.extend(json.loads(line) for line in f)

        pdf_dir = Path(settings.BASE_DIR) / "data" / "pdfs"
        if pdf_dir.exists():
            for pdf_file in pdf_dir.glob("*.pdf"):
                text = extract_text(pdf_file)
                records.append(
                    {"id": pdf_file.stem, "title": pdf_file.stem, "text": text}
                )

        client.collections["books"].documents.import_(records, {"action": "upsert"})
        self.stdout.write(self.style.SUCCESS(f"Indexed {len(records)} books"))
