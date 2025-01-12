from django.contrib import admin
from .models import Coin, DailyBalance, UserCoin


admin.site.register(Coin)
admin.site.register(UserCoin)
admin.site.register(DailyBalance)
