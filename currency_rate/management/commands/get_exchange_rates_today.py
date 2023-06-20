import traceback
from json import JSONDecodeError

from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.utils import timezone

import requests
import time

from django.utils.datetime_safe import date

from currency_rate.models import Currency, ExchangeRate


class Command(BaseCommand):
    help = 'Получает и записывает данные о курсах валют на сегодня'

    def handle(self, *args, **kwargs):

        api_url = 'https://www.cbr-xml-daily.ru/daily_json.js'

        data = None

        for attempt in range(1, 6):
            try:
                response = requests.get(api_url)
            except TimeoutError or ConnectionError as ex:
                self.stdout.write(f"Oops, there was an error: {ex}")
                if attempt < 6:
                    self.stdout.write(f"Try again in 5 sec")
                    time.sleep(5)
                continue
            if response.status_code == 200:
                try:
                    data = response.json()
                    break
                except JSONDecodeError as ex:
                    traceback.print_exc()
                    self.stdout.write(f"Fail to parse JSON")
                    break
            else:
                self.stdout.write(f"Invalid status code {response.status_code}")
                break

        if data is None:
            self.stdout.write(f"Failed to update exchange rates")
        else:
            current_date = date.today()
            try:
                rates_list = data['Valute']
            except KeyError:
                self.stdout.write(f"There is no 'Valute' key")
                return

            for currency_code, currency_data in rates_list.items():
                currency_obj, _ = Currency.objects.get_or_create(
                    char_code=currency_code, defaults={'name': currency_data['Name']}
                )

                try:
                    ExchangeRate.objects.create(
                        currency_id=currency_obj.pk,
                        date=current_date,
                        value=float(currency_data['Value'])
                    )

                except IntegrityError:
                    self.stdout.write(f"{currency_code} is already exists")
                except Exception:
                    traceback.print_exc()
                    self.stdout.write(f"Fail to save model")

            self.stdout.write(f"Done!")
