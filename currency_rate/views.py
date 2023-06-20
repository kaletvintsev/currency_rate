from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import ExchangeRate


def show_rates(request):
    date = request.GET.get('date')

    if date:
        try:
            exchange_rates = ExchangeRate.objects.filter(date=date)
            return render(request, 'currency_rate/show_rates.html', {'exchange_rates': exchange_rates, 'date': date})
        except ExchangeRate.DoesNotExist:
            pass
    return HttpResponseNotFound("Страница не найдена")
