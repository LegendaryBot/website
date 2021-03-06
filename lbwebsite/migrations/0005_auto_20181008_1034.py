# Generated by Django 2.0.7 on 2018-10-08 14:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lbwebsite', '0004_auto_20180921_2304'),
    ]

    operations = [
        migrations.CreateModel(
            name='GuildRank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank_id', models.IntegerField(verbose_name='Rank ID')),
                ('discord_rank', models.CharField(max_length=200, verbose_name='Discord Rank')),
                ('guild', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lbwebsite.DiscordGuild')),
            ],
        ),
        migrations.AlterField(
            model_name='character',
            name='server_slug',
            field=models.CharField(max_length=50, verbose_name='Realm'),
        ),
        migrations.AlterUniqueTogether(
            name='guildrank',
            unique_together={('guild', 'rank_id')},
        ),
    ]
