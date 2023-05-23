from decimal import Decimal

import requests
from django.db import models


URL = "https://www.random.org/integers/"


class RandomOrgManager(models.Manager):
    def create_with_random_api(self, min_value: int = -1e9, max_value: int = 1e9):
        if min_value == max_value:
            raise ValueError("The minimum and maximum values cannot be the same")

        res = requests.get(
            URL,
            params={
                "num": 1,
                "base": 10,
                "min": min_value,
                "max": max_value,
                "col": 1,
                "format": "plain",
                "rnd": "new",
            },
        )
        res.raise_for_status()
        value = Decimal(res.text)
        return self.create(value=value)


class RandomResult(models.Model):
    value = models.DecimalField(decimal_places=6, max_digits=12)
    objects = RandomOrgManager()
