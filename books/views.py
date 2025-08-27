from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings
from pdfminer.high_level import extract_text
from uuid import uuid4
import typesense


client = typesense.Client(settings.TYPESENSE_CONFIG)


class SearchView(APIView):
    """Search books by title and text using Typesense."""

    def get(self, request):
        query = request.query_params.get("q", "")
        if not query:
            return Response({"results": []})

        search_parameters = {
            "q": query,
            "query_by": "title,text",
            "highlight_fields": "title,text",
            "per_page": 5,
        }
        search_result = client.collections["books"].documents.search(search_parameters)

        hits = []
        for hit in search_result.get("hits", []):
            doc = hit.get("document", {})
            snippet_parts = []
            for hl in hit.get("highlights", []):
                field = hl.get("field")
                snippet = hl.get("snippet")
                snippet_parts.append(f"{field}: {snippet}")
            hits.append(
                {
                    "id": doc.get("id"),
                    "title": doc.get("title"),
                    "snippet": " ... ".join(snippet_parts),
                }
            )
        return Response({"results": hits})


class UploadBookView(APIView):
    """Import a PDF book and index it in Typesense."""

    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        pdf_file = request.FILES.get("file")
        if not pdf_file:
            return Response({"error": "No file provided"}, status=400)

        title = request.data.get("title") or pdf_file.name
        pdf_file.seek(0)
        text = extract_text(pdf_file)
        doc_id = str(uuid4())
        client.collections["books"].documents.upsert(
            {"id": doc_id, "title": title, "text": text}
        )
        return Response({"id": doc_id, "title": title})
