# Generated by Django 2.2.4 on 2020-10-25 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_profilelike'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profilelike',
            name='created_on',
        ),
        migrations.AddField(
            model_name='profilelike',
            name='liked',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AddField(
            model_name='profilelike',
            name='liked_on',
            field=models.DateTimeField(db_index=True, null=True),
        ),
        migrations.AddField(
            model_name='profilelike',
            name='shortlisted',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AddField(
            model_name='profilelike',
            name='shortlisted_on',
            field=models.DateTimeField(db_index=True, null=True),
        ),
        migrations.AddField(
            model_name='profilelike',
            name='viewed',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AddField(
            model_name='profilelike',
            name='viewed_on',
            field=models.DateTimeField(db_index=True, null=True),
        ),
    ]
