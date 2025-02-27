# Generated by Django 5.1.4 on 2024-12-13 19:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='exam',
        ),
        migrations.RemoveField(
            model_name='question',
            name='question_name',
        ),
        migrations.RemoveField(
            model_name='question',
            name='student',
        ),
        migrations.RemoveField(
            model_name='question',
            name='teacher',
        ),
        migrations.AddField(
            model_name='question',
            name='assignment',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='course.assignment'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='question_type',
            field=models.CharField(choices=[('text', 'Text Question'), ('multiple_choice', 'Multiple Choice Question')], default=2, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='text',
            field=models.TextField(default=3),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='AnswerOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200)),
                ('is_correct', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.question')),
            ],
        ),
        migrations.CreateModel(
            name='StudentAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.TextField(blank=True, null=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.question')),
                ('selected_options', models.ManyToManyField(to='course.answeroption')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.student')),
            ],
        ),
        migrations.DeleteModel(
            name='Option',
        ),
    ]
