# Generated by Django 2.2 on 2019-05-02 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='possibleanswer',
            name='number',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='number',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
