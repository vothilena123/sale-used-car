# Generated by Django 4.0.6 on 2023-02-17 15:47

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower', models.CharField(max_length=100)),
                ('user', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='LikePost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_liked_id', models.CharField(max_length=500)),
                ('username', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='PostSell',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('user', models.CharField(max_length=100)),
                ('carName', models.CharField(max_length=100)),
                ('image1', models.ImageField(upload_to='post_images')),
                ('yearOfManufacture', models.IntegerField()),
                ('carStatus', models.CharField(max_length=100)),
                ('transmission', models.CharField(max_length=100)),
                ('fuel', models.CharField(max_length=100)),
                ('color', models.CharField(max_length=100)),
                ('kilimetersRun', models.IntegerField()),
                ('locationSell', models.CharField(max_length=100)),
                ('carPrice', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('createdAt', models.DateTimeField(default=datetime.datetime.now)),
                ('numberOfLike', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userID', models.IntegerField()),
                ('about', models.TextField(blank=True)),
                ('profileImage', models.ImageField(default='default-avatar-profile.jpeg', upload_to='profile_images')),
                ('backgroundImage', models.ImageField(default='default-background.jpeg', upload_to='profile_images')),
                ('location', models.CharField(blank=True, max_length=100)),
                ('detailAdress', models.CharField(blank=True, max_length=150)),
                ('phoneNumber', models.CharField(blank=True, max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('first_person', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='thread_first_person', to=settings.AUTH_USER_MODEL)),
                ('second_person', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='thread_second_person', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('first_person', 'second_person')},
            },
        ),
        migrations.CreateModel(
            name='PostSellImages',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('carImage', models.FileField(upload_to='post_images')),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usedCar.postsell')),
            ],
        ),
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('thread', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chatmessage_thread', to='usedCar.thread')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
