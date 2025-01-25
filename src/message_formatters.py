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
    def handle(message: str, coin_name: str, *args, **kwargs):
        return f"{coin_name}: ${message}"


class CompactMessageFormatter(MessageFormatter):
    @staticmethod
    def handle(message: str, *args, **kwargs):
        return f"${message}"


class DisplayAllTickersMessageFormatter(MessageFormatter):
    @staticmethod
    def handle(connections: list, *args, **kwargs):
        return '   '.join([DefaultMessageFormatter().handle(**c.ticker_value) for c in connections])


class HiddenMessageFormatter(MessageFormatter):
    @staticmethod
    def handle(*args, **kwargs):
        return f">,O"  # Hidden
