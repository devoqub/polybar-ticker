import asyncio


class CommandServer:

    def __init__(self, manager, host="127.0.0.1", port=14888):
        self.port = port
        self.manager = manager
        self.host = host
        self.commands = {
            "next": self.manager.next_connection,
            "prev": self.manager.prev_connection,
            "change-handler": self.manager.change_message_formatter,
        }

    async def handle_client(self, reader, writer):
        try:
            data = await reader.read(100)
            command = data.decode().strip()

            await self.commands[command]

            writer.write(b"OK\n")
            await writer.drain()
        except OSError:
            print("Address alr use")
            return
        except Exception as e:
            writer.write(f"Error: {e}\n".encode())
            await writer.drain()
        finally:
            writer.close()

    async def start(self):

        try:
            async with await asyncio.start_server(self.handle_client, self.host, self.port) as server:

                # server = await asyncio.start_server(
                #     self.handle_client, self.host, self.port
                # )
                async with server:
                    await server.serve_forever()
        except OSError:
            print("Address alr use")
            return
        except:
            print("ERRRR")
