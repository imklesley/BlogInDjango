from django.contrib import admin
# Para Criar um Custom Painel Admin
from django.contrib.auth.admin import UserAdmin
from account.models import Account


# Cria-se a clase que irá coordenar esse painel

class AccountAdmin(UserAdmin):  # Agora coloca-se os parâmetros obrigatórios que formam esse painel
    # Todos os objetos aqui instanciados, são requeridos para realizar um CustomPainel
    # São as colunas que serão exibidas na tela principal ao exibir os dados da tabela selecionada
    list_display = ('first_name', 'username', 'email', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    # Campos que poderei realizar a buscas
    search_fields = ('email', 'username','first_name')

    # campos que são somente leitura e não podem está disponíveis para alteração
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()

    list_filter = ()

    fieldsets = ()

#Sobrescreve o título que está no topo da página
# admin.site.site_header = 'Novo Nome De Header da Página'
admin.site.register(Account, AccountAdmin)
