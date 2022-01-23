from django.core.exceptions import PermissionDenied


def login_required(func):

    # Essa função é a nossa view, ela recebe a request, e todos os possíveis parâmetros
    def wrapped_func(request, *args, **kwargs):

        # Verificamos se o usuário está authenticado, caso não esteja criamos um erro do tipo "Permissão Negada"
        if not request.user.is_authenticated:
            raise PermissionDenied

        # Caso o usuário esteja logado retorna a função com os devidos parâmetros
        return func(request, *args, **kwargs)

    # Retorna-se a função alterada
    return wrapped_func
