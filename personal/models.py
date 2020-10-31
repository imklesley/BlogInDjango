from django.db import models

"""Para adicionar um model ao banco de dados basta:
1-) python manage.py makemigrations
2-) python manage.py migrate
"""


#NÃO IREMOS PRECISAR DESSE CÓDIGO ERA SÓ PRA PRATICAR
# PRIORITY = [
#     ('H', 'High'),
#     ('M', 'Medium'),
#     ('L', 'Low')
# ]
#
#
# class Question(models.Model):
#     title = models.CharField(max_length=60)
#     question = models.TextField(max_length=400)
#     priority = models.CharField(max_length=1, choices=PRIORITY)
#
#     # Serve para dar um override no método toString do python
#     def __str__(self):
#         return f'The title is {self.title}, the question is {self.question} and the priority is {self.priority}'
#
#
#
#     #Está classe ser para alterar meta dados no django, isso na tabela criada
#     class Meta:
#         verbose_name = 'The question'
#         verbose_name_plural = 'Peoples Questions'