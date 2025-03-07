#!/usr/bin/env python3
import os
import asyncio

from src.api_extractors import get_extractor_class
from src.connections import ConnectionManager, get_ws_connection_class
from src import (
    utils,
    config,
    actions,
    message_formatters as mh
)


async def main():
    # Initialize and get arguments
    args = utils.init_parser().parse_args()

    # During debugging, it won't kill another running polybar-ticker (a.k.a. the ticker)
    # This is needed to modify the source code without interrupting polybar
    # (if polybar is run together with this script, they will kill each other on startup)
    if not args.debug:
        # Killing the previously working ticker and create a file with the PID
        utils.kill_pid_from_file()
        utils.kill_process_by_port(config.SERVER_PORT)
        utils.create_pid_file()

    if not config.tickers:
        raise ValueError("The list of connections (tickers) cannot be empty!!")

    # Create a list of connections (tasks) for each pair "coin name - URL".
    # Each item in the list is a WSConnection object initialized with the specified parameters.

    ws_connection_class = get_ws_connection_class(config.LIBRARY_USE)
    extractor = get_extractor_class(config.API_SERVICE)()
    connections = [
        ws_connection_class(
            coin_name=coin_name, url=url, extractor=extractor
        )
        for coin_name, url in config.tickers
    ]

    # Define the list of message formatters,
    # these formatters are used to manage ticker display
    # example: BTC: $104456.34 / $104456.34 / <all tickers> / hidden
    formatters = (
        mh.DefaultMessageFormatter,
        mh.CompactMessageFormatter,
        mh.DisplayAllTickersMessageFormatter,
        mh.HiddenMessageFormatter,
    )

    # The ConnectionManager object manages all connections
    # the greeting_event is passed for synchronizing the hiding of the greeting splash screen greeting()
    greeting_event = asyncio.Event()
    manager = ConnectionManager(
        connections=connections, formatters=formatters, greeting_event=greeting_event
    )

    # CommandServer is responsible for managing actions (read: actions) and interactions through Polybar.
    # example: *clicking on a ticker in polybar* -> *ConnectionManager executes an action*
    # Honestly, I don’t know how to implement it any other way, this is the best I came up with. :(
    # More details in the actions.py file
    server = actions.CommandServer(manager)

    # Start all processes asynchronously
    # 1. Greeting message / animation
    # 2. Start the manager, under the hood it establishes each connection to the resource
    # 3. Start the server for interaction with the ticker
    await asyncio.gather(
        utils.greeting(greeting_event), manager.start(), server.start()
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        raise e
    finally:
        if os.path.exists(config.TEMP_PID_PATH):
            os.remove(config.TEMP_PID_PATH)
