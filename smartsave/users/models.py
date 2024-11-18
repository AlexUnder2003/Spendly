from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUser(AbstractUser):
    GENDERS = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    ]
    first_name = models.CharField(
        max_length=30,
        verbose_name='Имя',
        blank=True
        )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия',
        blank=True
        )
    address = models.CharField(
        max_length=256,
        verbose_name='Адрес',
        blank=True
        )
    city = models.CharField(
        max_length=256,
        erbose_name='Город',
        blank=True
        )
    gender = models.CharField(
        max_length=1,
        choices=GENDERS,
        verbose_name='Гендер',
        blank=True
        )
