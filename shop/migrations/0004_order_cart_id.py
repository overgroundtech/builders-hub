# Generated by Django 3.2.9 on 2022-01-31 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_category_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='cart_id',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]