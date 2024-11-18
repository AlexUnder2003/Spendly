from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Coin(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название монеты")
    symbol = models.CharField(max_length=10, unique=True, verbose_name="Символ монеты")

    def __str__(self):
        return f"{self.name} ({self.symbol})"

    class Meta:
        verbose_name = "Монета"
        verbose_name_plural = "Монеты"


class UserCoin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_coins', verbose_name="ID Пользователя")
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE, related_name='user_coins', verbose_name="ID Монеты")
    quantity = models.DecimalField(max_digits=20, decimal_places=8, verbose_name="Количество")

    def __str__(self):
        return f"{self.user.username} - {self.coin.name}: {self.quantity}"

    class Meta:
        verbose_name = "Пользовательские накопления"
        unique_together = ('user', 'coin')


class DailyBalance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    balance = models.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        unique_together = ('user', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} - {self.date}: {self.balance}"
