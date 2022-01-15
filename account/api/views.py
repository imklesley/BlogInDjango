from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from rest_framework.authtoken.models import Token

from .serializers import RegisterSerializer, LoginAccountSerializer, AccountSerializer
from .throttling import LoginThrottleDay, LoginThrottleSec


@api_view(['POST'])
@permission_classes([AllowAny])
def api_register_user_view(request):
    """
       This endpoint will create an user
   """
    data = {}

    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            data['detail'] = 'User Successfully Created'
            data['token'] = Token.objects.get(user=account).key
            data['data'] = serializer.data
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data['detail'] = 'User Not Created'
            data['errors'] = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([LoginThrottleSec, LoginThrottleDay, ])
def api_login_account_view(request):
    data = {}

    if request.method == 'POST':
        serializer = LoginAccountSerializer(data=request.data)

        # Caso o email ou a senha sejam nulos devolve a response 400
        if serializer.is_valid():
            # Caso os cam   pos estejam okay tenta autenticar
            user = serializer.get_user()

            if user:
                try:
                    # Para atualizar o token ao logar consegui fazer de duas formas, deletando o token antigo e criando outro
                    # old_token = Token.objects.get(user=user)
                    # old_token.delete()
                    # new_token = Token.objects.create(user=user)

                    # Ou filtrando o token com filter e usando o método update para atualizar somente o campo key usando
                    # o generate_key só que ao fazer isso o django vai retornar 0 ou 1 de acordo com o resultado da operação update
                    Token.objects.filter(user=user).update(key=Token.generate_key())
                    # Logo é necessário fazer novamente  a busca pelo token
                    token = Token.objects.get(user=user)
                except Token.DoesNotExist:
                    token = Token.objects.create(user=user)

                # Passa o token e mensagem de sucesso
                data['token'] = token.key
                data['detail'] = 'User authenticated'

                return Response(data, status.HTTP_200_OK)
            else:
                data['detail'] = 'Invalid Credentials'
                return Response(data, status.HTTP_400_BAD_REQUEST)

        else:
            # Caso os dados sejam inválidos retorna a response com mensagem de erro e a lista de erros de cada field
            data['errors'] = serializer.errors
            data['detail'] = 'Email or password are invalid'
            return Response(data, status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_user_data(request):
    if request.method == 'GET':
        serializer = AccountSerializer(request.user, many=False)
        data = {'detail': 'Data successfully collected', 'data': serializer.data}
        return Response(data, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def api_update_user(request):
    if request.method == 'PUT':
        data = {}
        user = request.user
        serializer = AccountSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            data['detail'] = 'User successfully updated'
            data['data'] = serializer.data
        else:
            data['detail'] = 'User not was updated'
            data['errors'] = serializer.errors

        return Response(data, status=status.HTTP_400_BAD_REQUEST)
