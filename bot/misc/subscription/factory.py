from typing import Dict

from bot.misc.subscription import SubscriptionAbstract
from bot.misc.subscription.voice import VoiceSubscriptionPlan


class SubscriptionPlanFactory:
    __available_subscriptions: Dict[str, SubscriptionAbstract] = {
        'voice': VoiceSubscriptionPlan(),
    }

    def __call__(self, name: str, *args, **kwargs) -> SubscriptionAbstract:
        return self.get_subscription(name)

    def get_subscription(self, name: str) -> SubscriptionAbstract:
        return self.__available_subscriptions[name.lower()]
