from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.books.api.views import AuthorBookList, AuthorList, BookViewSet



router = DefaultRouter()
router.register('books', BookViewSet, basename='books')

urlpatterns = [
    path('', include(router.urls)),
    path('author/', include([
        path('list/', AuthorList.as_view(), name='autor-books'),
        path('<int:author_id>/books/', AuthorBookList.as_view(), name='autor-books'),
    ]))
    
]