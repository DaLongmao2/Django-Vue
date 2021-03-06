# Generated by Django 3.1.7 on 2021-03-30 01:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_article_author'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'Category',
            },
        ),
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['-created']},
        ),
        migrations.AlterModelTable(
            name='article',
            table='Article',
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='article', to='article.category'),
        ),
    ]
