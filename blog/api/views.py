from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView

from rest_framework.filters import SearchFilter, OrderingFilter

from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

# My Models
from blog.models import BlogPost

# serializers
from blog.api.serializers import BlogPostSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def api_detail_blog_view(request, slug):
    try:
        blog_post = BlogPost.objects.get(slug=slug)
    except BlogPost.DoesNotExist:
        return Response({'detail': 'Post Does Not Exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BlogPostSerializer(blog_post)
        return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def api_update_blog_view(request, slug):
    try:
        blog_post = BlogPost.objects.get(slug=slug)
    except BlogPost.DoesNotExist:
        return Response({'detail': 'Post Does Not Exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.user != blog_post.author:
        return Response({'detail': 'You dont have permission to access this page'}, status=status.HTTP_403_FORBIDDEN)

    data = {}

    if request.method == 'PUT':
        serializer = BlogPostSerializer(blog_post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            data['detail'] = 'Post Successfully Updated'
            data['data'] = serializer.data
            return Response(data, status=status.HTTP_200_OK)
        else:
            data['detail'] = 'Post not Updated'
            data['erros'] = serializer.errors
            return Response(data, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def api_delete_blog_view(request, slug):
    try:
        blog_post = BlogPost.objects.get(slug=slug)
    except BlogPost.DoesNotExist:
        return Response({'detail': 'Post Does Not Exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.user != blog_post.author:
        return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

    data = {}

    if request.method == 'DELETE':

        delete_operation = blog_post.delete()

        if delete_operation:
            data['detail'] = 'Post Successfully Deleted'
            return Response(data, status=status.HTTP_200_OK)
        else:
            data['detail'] = 'Post not Deleted'
            return Response(data, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_create_blog_view(request):
    """
    This endpoint will create a blogpost
    """
    if request.method == 'POST':
        print(request.data)
        author = request.user

        data = {}

        # Iniciamos o processo de criação do post para podermos inserir o autor da postagem
        post = BlogPost.objects.create(author=author)

        serializer = BlogPostSerializer(post, data=request.data)

        if serializer.is_valid():
            serializer.save()
            data['detail'] = 'Post Successfully Created'
            data['data'] = serializer.data
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            post.delete()
            data['detail'] = 'Post Not Created'
            data['errors'] = serializer.errors
            return Response(data, status=status.HTTP_404_NOT_FOUND)


class ApiListView(ListAPIView):
    queryset = BlogPost.objects.all()

    serializer_class = BlogPostSerializer

    # Caso necessário verificar o usuário poderia adicionar a variável authentication_classes e passar [IsAuthenticated]
    permission_classes = (AllowAny,)

    pagination_class = PageNumberPagination

    filter_backends = (SearchFilter, OrderingFilter)

    search_fields = ('title', 'body', 'author__username')


@api_view(['GET'])
@permission_classes([AllowAny])
def api_list_view(request):
    if request.method == 'GET':
        posts = BlogPost.objects.all()

        paginator = PageNumberPagination()

        # Caso queira permitir o cliente decidir quantos post serão coletados por página
        paginator.page_size = request.GET.get('page_size', 10)

        query = request.GET.get('search')

        if query is not None:
            posts = posts.filter(
                Q(title__icontains=query, body__icontains=query, author__username__icontains=query, _connector='or')
            ).distinct()

        result_page = paginator.paginate_queryset(posts, request)

        serializer = BlogPostSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_user_posts(request):
    if request.method == 'GET':
        data = {}
        user = request.user
        posts_user = BlogPost.objects.filter(author=user)
        serializer = BlogPostSerializer(posts_user, many=True)
        data['data'] = serializer.data
        return Response(data, status=status.HTTP_200_OK)
