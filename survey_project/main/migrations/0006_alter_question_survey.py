# Generated by Django 5.0.1 on 2024-02-08 13:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_answer_question_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='survey',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='main.survey'),
        ),
    ]
