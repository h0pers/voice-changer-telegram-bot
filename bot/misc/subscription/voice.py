from datetime import timedelta
from decimal import Decimal
from iso4217 import Currency

from bot.misc.subscription import SubscriptionAbstract, SubscriptionPlanAbstract, SubscriptionControllerAbstract


class VoiceSubscriptionController(SubscriptionControllerAbstract):
    @classmethod
    def give_subscription(cls):
        pass

    @classmethod
    def claim_subscription(cls):
        pass

    @classmethod
    def subscription_duration_left(cls):
        pass


class VoiceSubscription(SubscriptionAbstract):
    obj = VoiceSubscriptionController()


class VoiceSubscriptionPlan(SubscriptionPlanAbstract):
    _available_plans = {
        1: VoiceSubscription(duration=timedelta(days=7), price=Decimal(6.99)),
        2: VoiceSubscription(duration=timedelta(days=14), price=Decimal(12.99)),
        3: VoiceSubscription(duration=timedelta(days=30), price=Decimal(19.99)),
    }

    @property
    def available_plans(self):
        return super().available_plans()

    @classmethod
    def get_subscription(cls, subscription_id: int, currency: Currency = None) -> VoiceSubscription:
        return super(VoiceSubscriptionPlan, cls).get_subscription(subscription_id, currency)
