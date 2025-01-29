import abc


# TODO simplify
# formatters = {
#     'default': "XXXXXX",
#     'compact': "XXXXXX",
#     'display_all': "XXXXXX",
# }

class MessageFormatter(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def handle(*args, **kwargs):
        raise NotImplementedError("(ﾉ｀□´)ﾉ⌒┻━┻")


class DefaultMessageFormatter(MessageFormatter):
    @staticmethod
    def handle(coin_name: str, price: str, *args, **kwargs):
        if price is None or coin_name is None:
            return ""
        return f"{coin_name}: ${price}"


class CompactMessageFormatter(MessageFormatter):
    @staticmethod
    def handle(price: str, *args, **kwargs):
        if price is None:
            return ""
        return f"${price}"


class DisplayAllTickersMessageFormatter(MessageFormatter):
    @staticmethod
    def handle(connections: list, *args, **kwargs):
        if not connections:
            return ""
        return '   '.join([DefaultMessageFormatter().handle(**c.ticker_value) for c in connections])


class HiddenMessageFormatter(MessageFormatter):
    @staticmethod
    def handle(*args, **kwargs):
        return f">,O"  # Hidden
