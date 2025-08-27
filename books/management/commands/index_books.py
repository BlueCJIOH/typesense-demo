import json
from pathlib import Path

import typesense
from django.conf import settings
from django.core.management.base import BaseCommand


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
            "default_sorting_field": "id",
        }
        try:
            client.collections["books"].retrieve()
            self.stdout.write(self.style.NOTICE("Collection already exists"))
        except typesense.exceptions.ObjectNotFound:
            client.collections.create(schema)
            self.stdout.write(self.style.SUCCESS("Collection created"))

        data_path = Path(settings.BASE_DIR) / "data" / "books.jsonl"
        with open(data_path, "r") as f:
            records = [json.loads(line) for line in f]
        client.collections["books"].documents.import_(records, {"action": "upsert"})
        self.stdout.write(self.style.SUCCESS(f"Indexed {len(records)} books"))
