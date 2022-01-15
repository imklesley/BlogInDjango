from django.db import models
from django.db.models.signals import pre_save, post_delete
from django.utils.text import slugify  # Para colocar nomes nas urls de um determinado post aberto
from django.conf import settings
from django.dispatch import receiver


from datetime import datetime


def upload_location(instance, filename, *args, **kwargs):
    author_id = instance.author.id
    title = instance.title
    filename = filename
    timestamp = datetime.now().timestamp()
    file_path = f'blog/{author_id}/{title}-{timestamp}-{filename}'
    return file_path


class BlogPost(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    body = models.CharField(max_length=5000, null=False, blank=False)
    # para usar essa função é preciso já ter instalado a dependência Pillow
    image = models.ImageField(upload_to=upload_location, null=False, blank=False)

    date_published = models.DateTimeField(auto_now_add=True, verbose_name='date published')
    # Toda vez que esse objeto for atualizado o Django altera o valor no bd
    date_updated = models.DateTimeField(auto_now=True, verbose_name='date updated')
    # Estou criando uma foreigner key, criando um vinculo, entre alguma conta autenticado criada em Account e
    # dizendo que tudo pode ser apagado nesse post com exceção do campo author
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Permito o usuário não inserir um slug, caso ele não insira é criado um automáticamente
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.title


# É preciso criar um método para realizar o delete da image/imagens colocadas no serve, referente à esse post
@receiver(post_delete, sender=BlogPost)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)


def pre_save_blog_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        timestamp = datetime.now().timestamp()
        instance.slug = slugify(f'{instance.author.username}-{instance.title}-{timestamp}')


# A qualquer momento que for preciso salvar um post no db, chame pre_save_blog_post_receiver e
# verifique se há slug, se não crie
pre_save.connect(pre_save_blog_post_receiver, sender=BlogPost)
