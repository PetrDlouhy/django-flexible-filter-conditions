# Generated by Django 2.2.9 on 2020-01-14 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TestModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_field', models.CharField(help_text='Foo help_text', max_length=255, verbose_name='Foo verbose name')),
            ],
        ),
    ]
