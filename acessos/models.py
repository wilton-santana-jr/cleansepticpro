from django.db import models

# Create your models here.


from django.contrib.auth.models import AbstractUser, Group

# pbkdf2_sha256$600000$h2wxOnat17bwUS1d3mFhEO$n7DWEerrybWYR52R19fne09Y56K7IXTmgTGYS7mZsGs=


class CustomUser(AbstractUser):
    # Adicione os campos personalizados que você deseja ao seu modelo
    nome = models.CharField(max_length=150)  # (89)99976-2610
    telefone = models.CharField(max_length=15)  # (89)99976-2610
    endereco = models.TextField()

    def save(self, *args, **kwargs):

        if not self.password.startswith("pbkdf2_sha256$"):
            # Apenas se a senha não estiver criptografada, defina-a como uma senha criptografada
            self.set_password(self.password)
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
