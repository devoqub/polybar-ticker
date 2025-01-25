import unittest

from src.message_formatters import (
    DefaultMessageFormatter,
    CompactMessageFormatter,
    DisplayAllTickersMessageFormatter,
    HiddenMessageFormatter
)


class TestMessageFormatter(unittest.TestCase):

    def test_default_message_formatter(self):
        message = "1000"
        coin_name = "BTC"
        expected = "BTC: $1000"
        result = DefaultMessageFormatter.handle(message, coin_name)
        self.assertEqual(result, expected)

    def test_compact_message_formatter(self):
        message = "1000"
        expected = "$1000"
        result = CompactMessageFormatter.handle(message)
        self.assertEqual(result, expected)

    def test_display_all_tickers_message_formatter(self):
        class ConnectionMock:
            def __init__(self, ticker_value):
                self.ticker_value = ticker_value

        connections = [
            ConnectionMock({'message': '1000', 'coin_name': 'BTC'}),
            ConnectionMock({'message': '2000', 'coin_name': 'ETH'})
        ]

        # Ожидаемый вывод
        expected = "BTC: $1000   ETH: $2000"
        result = DisplayAllTickersMessageFormatter.handle(connections)
        self.assertEqual(result, expected)

    def test_hidden_message_formatter(self):
        expected = ">,O"
        result = HiddenMessageFormatter.handle()
        self.assertEqual(result, expected)

