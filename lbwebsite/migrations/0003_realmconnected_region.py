# Generated by Django 2.0.7 on 2018-08-11 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lbwebsite', '0002_realmconnected'),
    ]

    operations = [
        migrations.AddField(
            model_name='realmconnected',
            name='region',
            field=models.IntegerField(choices=[(1, 'US'), (2, 'EU'), (3, 'TW'), (4, 'KR')], default=1),
        ),
    ]