# Generated by Django 2.0.7 on 2018-07-22 01:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.IntegerField(choices=[(1, 'US'), (2, 'EU'), (3, 'TW'), (4, 'KR')], default=1)),
                ('server_slug', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('guild_name', models.CharField(blank=True, max_length=50, null=True)),
                ('thumbnail', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='DiscordGuild',
            fields=[
                ('guild_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='GuildCustomCommand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('type', models.IntegerField(choices=[(1, 'Text')], default=1)),
                ('value', models.CharField(max_length=2000)),
                ('guild', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lbwebsite.DiscordGuild')),
            ],
        ),
        migrations.CreateModel(
            name='GuildPrefix',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prefix', models.CharField(max_length=10)),
                ('guild', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lbwebsite.DiscordGuild')),
            ],
        ),
        migrations.CreateModel(
            name='GuildServer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.IntegerField(choices=[(1, 'US'), (2, 'EU'), (3, 'TW'), (4, 'KR')], default=1)),
                ('server_slug', models.CharField(max_length=50)),
                ('guild_name', models.CharField(max_length=50, null=True)),
                ('default', models.BooleanField(default=False)),
                ('guild', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lbwebsite.DiscordGuild')),
            ],
        ),
        migrations.AddField(
            model_name='character',
            name='main_for_guild',
            field=models.ManyToManyField(to='lbwebsite.DiscordGuild'),
        ),
        migrations.AddField(
            model_name='character',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='guildcustomcommand',
            unique_together={('guild', 'name')},
        ),
        migrations.AlterUniqueTogether(
            name='character',
            unique_together={('region', 'server_slug', 'name')},
        ),
    ]
