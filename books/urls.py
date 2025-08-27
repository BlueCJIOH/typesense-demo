from django.urls import path
from .views import SearchView, UploadBookView

urlpatterns = [
    path('search/', SearchView.as_view(), name='search'),
    path('import/', UploadBookView.as_view(), name='import'),
]
