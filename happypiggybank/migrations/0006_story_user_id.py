# Generated by Django 2.0.1 on 2018-01-18 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('happypiggybank', '0005_storycomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='user_id',
            field=models.BigIntegerField(db_index=True, default=0),
            preserve_default=False,
        ),
    ]
