from django.contrib import admin
from .models import Coin, UserCoin


admin.site.register(Coin)
admin.site.register(UserCoin)
