# Generated by Django 4.2.6 on 2023-10-18 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitacaoservico',
            name='endereco',
            field=models.TextField(blank=True, null=True),
        ),
    ]
