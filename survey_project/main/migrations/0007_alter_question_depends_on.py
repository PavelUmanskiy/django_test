# Generated by Django 5.0.1 on 2024-02-08 14:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_question_survey'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='depends_on',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='branches', to='main.question'),
        ),
    ]
