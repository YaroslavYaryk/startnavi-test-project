# Generated by Django 4.1.7 on 2023-03-29 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_alter_postlike_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postlike',
            name='created_at',
            field=models.DateField(null=True),
        ),
    ]
