# Generated by Django 5.1.3 on 2024-11-25 09:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Book",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200, verbose_name="书名")),
                ("author", models.CharField(max_length=100, verbose_name="作者")),
                (
                    "isbn",
                    models.CharField(max_length=13, unique=True, verbose_name="ISBN"),
                ),
                (
                    "available",
                    models.BooleanField(default=True, verbose_name="是否可借"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="BorrowReturn",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "borrow_date",
                    models.DateField(auto_now_add=True, verbose_name="借出日期"),
                ),
                (
                    "return_date",
                    models.DateField(blank=True, null=True, verbose_name="归还日期"),
                ),
                (
                    "book",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="main.book",
                        verbose_name="图书",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="借阅者",
                    ),
                ),
            ],
        ),
    ]
