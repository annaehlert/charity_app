# Generated by Django 3.0.8 on 2020-08-05 13:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0005_delete_donation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('address', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=15)),
                ('city', models.CharField(max_length=100)),
                ('zip_code', models.CharField(max_length=6)),
                ('pick_up_date', models.DateField()),
                ('pick_up_time', models.TimeField()),
                ('pick_up_comment', models.CharField(max_length=255, null=True)),
                ('categories', models.ManyToManyField(to='main.Category')),
                ('institution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Institution')),
                ('user', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]