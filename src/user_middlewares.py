"""
Тут можно добавить свои миддлвари которые будут прослушивать передачу данных с криптой
На этом можно сделать к примеру, телеграм бота который будет
обрабатывать эту информацию на ваше усмотрение.

Еще в разработке, и очень сырой код.
"""


class MiddlewareExample:
    async def process_crypto(self, data: dict):
        coin_name = data.get("coin_name")
        price = data.get("price")

        # print(f"Мы получили {coin_name}: {price}!")

        return data
