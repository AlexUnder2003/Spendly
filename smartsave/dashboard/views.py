from django.http import JsonResponse
from django.shortcuts import render

from coins.functions import get_user_coins
from coins.models import DailyBalance

from django.contrib.auth.decorators import login_required


@login_required
def dashboard_view(request):
    user = request.user

    coins_with_prices = get_user_coins(user)

    context = {'coins': coins_with_prices}
    return render(request, 'dashboard/dashboard.html', context)


def get_chart_data(request):
    daily_balances = DailyBalance.objects.filter(user=request.user)

    chart_labels = [balance.date for balance in daily_balances]
    chart_data = [balance.balance for balance in daily_balances]

    return JsonResponse({
        'labels': chart_labels,
        'data': chart_data
    })
