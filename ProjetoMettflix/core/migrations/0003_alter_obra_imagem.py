# Generated by Django 4.2.3 on 2023-07-15 18:12

from django.db import migrations
import stdimage.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_obra_imagem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='obra',
            name='imagem',
            field=stdimage.models.StdImageField(force_min_size=False, null=True, upload_to='media/', variations={}, verbose_name='Imagem'),
        ),
    ]
