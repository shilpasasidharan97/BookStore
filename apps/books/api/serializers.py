import django.db
from rest_framework import serializers

from apps.books.models import Author, Book


class AuthorInlineSerializer(serializers.Serializer):
    name = serializers.CharField()
    bio = serializers.CharField(allow_blank=True, required=False)


class BookSerializer(serializers.ModelSerializer):
    author_id = serializers.IntegerField(required=False, write_only=True)
    author = AuthorInlineSerializer(required=False)
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'description', 'published_date', 'is_active', 'author_id']

    def create(self, validated_data):
        request = self.context['request']
        
        author_id = validated_data.pop('author_id', None)
        if author_id:
            try:
                author = Author.objects.get(id=author_id)
            except Author.DoesNotExist:
                raise serializers.ValidationError({'author_id': 'Author with this ID does not exist.'})
        else:
            author_data = validated_data.pop('author')
            author, created = Author.objects.get_or_create(
                name=author_data['name'],
                defaults={'bio': author_data.get('bio', '')}
            )
        return Book.objects.create(author=author, added_by=request.user, **validated_data)
    
    
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'