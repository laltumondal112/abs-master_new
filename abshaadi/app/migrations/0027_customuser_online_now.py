# Generated by Django 2.2.4 on 2020-10-26 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_auto_20201025_2325'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='online_now',
            field=models.BooleanField(db_index=True, default=False),
        ),
    ]