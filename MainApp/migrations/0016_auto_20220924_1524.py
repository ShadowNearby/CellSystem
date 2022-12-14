# Generated by Django 3.0.7 on 2022-09-24 07:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0015_merge_20220923_2135'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['user', '-date'], 'verbose_name': '留言', 'verbose_name_plural': '留言'},
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='留言日期'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(verbose_name='留言内容'),
        ),
        migrations.AlterField(
            model_name='tankcellhistory',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='unitgroup',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.CreateModel(
            name='CommentReply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='回复日期')),
                ('text', models.TextField(verbose_name='回复内容')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='留言回复', to='MainApp.Comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='回复者', to='MainApp.User')),
            ],
            options={
                'verbose_name': '留言回复',
                'verbose_name_plural': '留言回复',
                'ordering': ['user', '-date'],
            },
        ),
    ]
