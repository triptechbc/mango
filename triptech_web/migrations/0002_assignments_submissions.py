# Generated by Django 2.0.5 on 2018-06-03 21:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('triptech_web', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('date', models.DateTimeField(verbose_name='date')),
                ('text', models.CharField(max_length=256)),
                ('metadata1', models.CharField(max_length=256)),
                ('metadata2', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Submissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_name', models.CharField(max_length=200)),
                ('date', models.DateTimeField(verbose_name='date')),
                ('data_location', models.CharField(max_length=256)),
                ('metadata1', models.CharField(max_length=256)),
                ('metadata2', models.CharField(max_length=256)),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='triptech_web.Assignments')),
            ],
        ),
    ]
