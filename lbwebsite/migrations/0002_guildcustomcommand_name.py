# Generated by Django 2.0.7 on 2018-07-08 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lbwebsite', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='guildcustomcommand',
            name='name',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]
