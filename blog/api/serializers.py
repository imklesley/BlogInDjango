from rest_framework import serializers

from account.models import Account
from blog.models import BlogPost, upload_location


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['username', 'email', 'first_name']


class BlogPostSerializer(serializers.ModelSerializer):
    # Forma 1 - Parte 1 - de como pegar dados por uma relação no caso account e blogpost
    # author = serializers.SerializerMethodField(method_name='get_author_username')

    # Forma 2 de pegar dados por uma relação no caso account e blogpost
    # author = serializers.StringRelatedField(source='author.first_name')

    # Forma 3 - Usa-se um outro serializer para fazer somente a parte do author e por fim cria o campo aqui e insere em fields
    author = AccountSerializer(required=False, allow_null=False)

    class Meta:
        model = BlogPost
        fields = ['slug', 'title', 'body', 'image', 'tag', 'author', 'date_published']

    # Forma 1 de pegar dados por uma relação no caso account e blogpost
    def get_author_username(self, blog_post: BlogPost):
        author = blog_post.author
        return {'username': author.username, 'name': author.first_name, 'email': author.email}
