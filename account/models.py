# Capítulo de criação de Custom User
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Capítulo de criação de token ao criar usuáiro
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.db.models.signals import post_save


class MyAccountManager(BaseUserManager):

    # Cria-se um usuário comum
    def create_user(self, email, username, first_name, password=None):
        # Verifica-se se os campos obrigatórios foram preenchidos
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have an username')
        if not first_name:
            raise ValueError('Users must have a first name')

        # Caso esteja tudo certo eu crio o usuário
        user = self.model(
            # normalize_email means put all letter on lowcase
            email=self.normalize_email(email),
            username=username,
            first_name=first_name
        )

        # Set a password
        user.set_password(password)
        # salva as configurações
        user.save(using=self._db)
        return user

    # Cria-se um usuário comum e então seta as caracteristicas de super
    def create_superuser(self, email, username, first_name, password=None):
        # Cria-se o usuário
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            first_name=first_name
        )

        # Seta as cartacteristicas de Usuário Administrador
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        # Agora salva-se as caracteristicas
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name='email', max_length=60, unique=True, blank=False)
    username = models.CharField(max_length=30, unique=True)

    # Os campos a seguir são requerimentos para usar o AbstractBaseUser
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    """
    auto_now_add : pega o horário atual e não é alterado
    auto_now : pega o horário atual e pode ser atualizado
    """
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    # É possivel adcionar quantos mais elementos quiser. name, date_of_birth, college etc
    first_name = models.CharField(max_length=30)

    # É definido qual dos elementos vai ser utilizado para logar-- o login(podia ser o email por exemplo)
    USERNAME_FIELD = 'email'
    # Posso definir campos que são obrigados a serem preenchidos
    REQUIRED_FIELDS = ['first_name', 'username']

    # override no toString do python
    def __str__(self):
        return self.username

    # Para criar um Custom User Model é preciso também adicionar alguns métodos que são necessários

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    # É preciso dizer ao Criador de contas (Account) aonde está o MyAccountManager, logo criamos um objeto chamado objects

    objects = MyAccountManager()

    # Para finalizar o processo de criação do Custom User Model é preciso ir em settings e adicionar o parâmetro
    # AUTH_USER_MODEL = 'account.Account', isso após ter importado o modulo aqui criado. Isso vai fazer com que o django
    # use o nosso model criado para criação e manutenção dos usuários


@receiver(post_save, sender=Account)
def create_user_token(sender, instance=None, created=False, *args, **kwargs):
    if created:
        Token.objects.create(user=instance)
