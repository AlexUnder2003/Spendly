from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.utils import timezone
from datetime import datetime

from coins.functions import get_user_coins
from coins.models import DailyBalance

from django.contrib.auth.decorators import login_required


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        coins_with_prices = get_user_coins(user)
        context["coins"] = coins_with_prices
        return context


def get_chart_data(request):
    # Получаем текущую дату
    now = timezone.now()

    # Извлекаем параметры из запроса
    start_date_str = request.GET.get("start_date", None)
    end_date_str = request.GET.get("end_date", None)

    # Преобразуем даты в формат datetime, если они заданы
    if start_date_str and end_date_str:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        daily_balances = DailyBalance.objects.filter(
            user=request.user, date__range=[start_date, end_date]
        ).order_by(
            "date"
        )  # Сортировка по дате в порядке возрастания
    else:
        # Если даты не указаны, отображаем данные за текущий месяц
        daily_balances = DailyBalance.objects.filter(
            user=request.user, date__month=now.month, date__year=now.year
        ).order_by("date")

    # Генерация данных для графика
    chart_labels = [balance.date for balance in daily_balances]
    chart_data = [balance.balance for balance in daily_balances]

    return JsonResponse({"labels": chart_labels, "data": chart_data})
