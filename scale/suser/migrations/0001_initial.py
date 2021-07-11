# Generated by Django 3.2.4 on 2021-07-11 09:59

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(blank=True, max_length=15, null=True)),
                ('last_name', models.CharField(blank=True, max_length=15, null=True)),
                ('username', models.CharField(blank=True, max_length=30, null=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('number', models.PositiveIntegerField(blank=True, null=True)),
                ('Student', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='BookInventry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_uniqueid', models.CharField(max_length=7, unique=True)),
                ('issued', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Category', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BookModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_name', models.CharField(blank=True, max_length=100)),
                ('author', models.CharField(blank=True, max_length=30, null=True)),
                ('publish_date', models.DateField(blank=True, null=True)),
                ('base_fee', models.PositiveIntegerField(blank=True, null=True)),
                ('current_count', models.PositiveIntegerField(blank=True, null=True)),
                ('no_of_issued', models.PositiveIntegerField(blank=True, null=True)),
                ('Book_categories', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Genre', to='suser.categories')),
            ],
        ),
        migrations.CreateModel(
            name='BookLogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_day', models.DateField(auto_now_add=True)),
                ('checkback', models.DateField(blank=True, null=True)),
                ('due_date', models.DateField(blank=True, null=True)),
                ('book_inventry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='id_book', to='suser.bookinventry')),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='issuer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='bookinventry',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Book_detail', to='suser.bookmodel'),
        ),
    ]