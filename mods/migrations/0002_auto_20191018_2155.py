# Generated by Django 2.2.6 on 2019-10-18 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mods', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('1', 'Combat'), ('2', 'Building'), ('3', 'Other')], default='other', max_length=1),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=40),
        ),
    ]
