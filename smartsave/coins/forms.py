from decimal import Decimal
from django.core.exceptions import ValidationError
from django import forms
from coins.models import Coin, UserCoin


class AddCoinForm(forms.Form):
    coin_id = forms.ModelChoiceField(
        queryset=Coin.objects.all().order_by('name'),
        label="Select Coin",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    quantity = forms.DecimalField(
        min_value=0.01,
        label="Quantity",
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )

    def save(self, user):
        coin = self.cleaned_data['coin_id']
        quantity = self.cleaned_data['quantity']

        user_coin, created = UserCoin.objects.get_or_create(
            user=user,
            coin=coin,
            defaults={'quantity': quantity}
        )

        if not created:
            user_coin.quantity += quantity
            user_coin.save()

        return user_coin
    
    
class EditCoinForm(forms.ModelForm):
    class Meta:
        model = UserCoin
        fields = ['quantity']  # Поле для редактирования количества монеты
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control'})
        }