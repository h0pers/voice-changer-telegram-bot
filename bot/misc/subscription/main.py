from abc import ABC, abstractmethod
from datetime import timedelta
from decimal import Decimal
from typing import Dict
from iso4217 import Currency

from bot.config import DEFAULT_CURRENCY


class SubscriptionControllerAbstract(ABC):
    @classmethod
    @abstractmethod
    def subscription_duration_left(cls):
        return

    @classmethod
    @abstractmethod
    def give_subscription(cls):
        return

    @classmethod
    @abstractmethod
    def claim_subscription(cls):
        return


class SubscriptionAbstract(ABC):
    __duration: timedelta = None
    __price: Decimal = None
    __currency: Currency = DEFAULT_CURRENCY
    obj: SubscriptionControllerAbstract = None

    def __init__(self, duration: timedelta, price: Decimal, currency: Currency = None):
        if self.obj is None:
            raise Exception('Manager class is not set. Please provide manager class into manager field.')

        self.duration = duration
        self.price = price
        self.currency = currency

    @property
    def duration(self):
        return self.__duration

    @duration.setter
    def duration(self, value: timedelta):
        self.__duration = value

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value: Decimal):
        self.__price = round(value, 2)

    @property
    def currency(self):
        return self.__currency

    @currency.setter
    def currency(self, value: Currency):
        self.__currency = value


class SubscriptionPlanAbstract(ABC):
    _available_plans: Dict[int, SubscriptionAbstract] = None

    @property
    @abstractmethod
    def available_plans(self):
        return self._available_plans

    @classmethod
    @abstractmethod
    def get_subscription(cls, subscription_id: int, currency: Currency = None) -> SubscriptionAbstract:
        if cls._available_plans.get(subscription_id) is None:
            raise KeyError(f'''
The {subscription_id} subscription ID is not exists. Please make sure you write available ID''')

        subscription = cls._available_plans[subscription_id]
        subscription.currency = currency

        return subscription
