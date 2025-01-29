class MiddlewareExample:
    async def process_crypto(self, data: dict):
        coin_name = data.get("coin_name")
        price = data.get("price")

        print(f"Мы получили {coin_name}: {price}!")

        return data
