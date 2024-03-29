# Generated by Django 4.2.9 on 2024-01-13 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0003_topic_quiz_question_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='courseinstance',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='quiz',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='topic',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
