# Generated by Django 5.0.1 on 2024-02-08 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_question_depends_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='choices',
            field=models.CharField(blank=True, default=None, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='is_choices',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='question',
            name='right_choice',
            field=models.CharField(blank=True, default=None, max_length=64, null=True),
        ),
    ]