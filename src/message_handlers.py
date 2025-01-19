import abc


# TODO simplify
# handlers = {
#     'default': "XXXXXX",
#     'compact': "XXXXXX",
#     'display_all': "XXXXXX",
# }

class MessageHandler(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def handle(*args, **kwargs):
        raise NotImplementedError("(ﾉ｀□´)ﾉ⌒┻━┻")


class DefaultMessageHandler(MessageHandler):
    @staticmethod
    def handle(message: dict, coin_name: str, *args, **kwargs):
        return f"{coin_name}: ${message['events'][0]['price']}"


class CompactMessageHandler(MessageHandler):
    @staticmethod
    def handle(message: dict, *args, **kwargs):
        return f"${message['events'][0]['price']}"


class DisplayAllTickersMessageHandler(MessageHandler):
    @staticmethod
    def handle(connections: list, *args, **kwargs):
        return '   '.join([DefaultMessageHandler().handle(**c.ticker_value) for c in connections])


class HiddenMessageHandler(MessageHandler):
    @staticmethod
    def handle(*args, **kwargs):
        return f">,O"  # Hidden
