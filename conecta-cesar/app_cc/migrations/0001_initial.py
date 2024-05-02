# Generated by Django 5.0.4 on 2024-05-02 01:04

import app_cc.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Disciplina',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Turma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Aluno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, null=True)),
                ('ra', models.CharField(default=app_cc.models.generate_unique_ra, max_length=10, unique=True)),
                ('usuario', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='aluno', to=settings.AUTH_USER_MODEL)),
                ('turma', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='alunos', to='app_cc.turma')),
            ],
        ),
        migrations.CreateModel(
            name='Diario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100, null=True)),
                ('texto', models.TextField()),
                ('data', models.DateField(auto_now_add=True)),
                ('disciplina', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='diarios', to='app_cc.disciplina')),
            ],
        ),
        migrations.CreateModel(
            name='Falta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField()),
                ('justificada', models.BooleanField(default=False)),
                ('aluno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='faltas', to='app_cc.aluno')),
                ('disciplina', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='faltas', to='app_cc.disciplina')),
            ],
        ),
        migrations.CreateModel(
            name='Nota',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.FloatField(default='0', null=True)),
                ('aluno', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notas', to='app_cc.aluno')),
                ('disciplina', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notas', to='app_cc.disciplina')),
            ],
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, null=True)),
                ('ra', models.CharField(default=app_cc.models.generate_unique_ra, max_length=10, unique=True)),
                ('usuario', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='professor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='disciplina',
            name='professor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='disciplinas', to='app_cc.professor'),
        ),
        migrations.AddField(
            model_name='disciplina',
            name='turmas',
            field=models.ManyToManyField(related_name='disciplinas', to='app_cc.turma'),
        ),
    ]
