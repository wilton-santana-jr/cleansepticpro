from django.db import models

# Create your models here.


from django.contrib.auth.models import AbstractUser, Group
from django.db import models


class CustomUser(AbstractUser):
    # Adicione os campos personalizados que você deseja ao seu modelo
    nome = models.CharField(max_length=150)  # (89)99976-2610
    telefone = models.CharField(max_length=15)  # (89)99976-2610
    endereco = models.TextField()

    def save(self, *args, **kwargs):
        # Ao salvar, atribua o usuário ao grupo 'clientes'
        super().save(*args, **kwargs)


class CustomUserManager(models.Manager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O endereço de e-mail deve ser definido')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        print(f"Usuário criado: {user.username}, Senha: {user.password}")
        return user
