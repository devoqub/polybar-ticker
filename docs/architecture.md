ChatGPT generated

1. General Description

This project is an application that displays cryptocurrency prices on the Polybar panel, with the ability for
interactive control via a command server. It uses asynchronous programming with asyncio, along with several helper
modules for handling processes and WebSockets.

2. Project Structure
   2.1 actions.py

This file contains the CommandServer class, which manages user interactions through a command server. It listens for
commands from the user and passes them to the connection manager for execution. Specifically, it supports the following
commands:

    next — switch to the next connection.
    prev — switch to the previous connection.
    change-handler — change the message handler for displaying data.

Key Components:

    CommandServer: The main server responsible for receiving commands.
    handle_client(): Handles a command from the client and executes the corresponding action.
    start(): Starts the server on a specified host and port.

2.2 utils.py

This file contains utility functions for process and file management, including managing PID files and killing processes
by port.
Key Components:

    kill_pid_from_file(): Terminates a process by its PID stored in a file.
    create_pid_file(): Creates and locks a PID file for the current process.
    kill_process_by_port(): Terminates the process that is using a specified port.

2.3 message_handlers.py

This file contains abstract classes and concrete implementations for handling messages from servers. Message handlers
provide various output formats for cryptocurrency prices.
Key Components:

    MessageHandler: An abstract class for all message handlers.
    DefaultMessageHandler: A handler for displaying the cryptocurrency price in the standard format.
    CompactMessageHandler: A handler for displaying only the cryptocurrency price.
    DisplayAllTickersMessageHandler: A handler for displaying all tickers.
    HiddenMessageHandler: A handler for hidden output.

2.4 main.py

The main file that initializes the entire process: sets up connections, starts the command server, and handles the
display process. It also manages command-line arguments using argparse.
Key Components:

    init_parser(): Configures the command-line arguments.
    main(): The main asynchronous function that initializes all processes:
        Creates a list of connections via WSConnection for each ticker.
        Creates and starts the connection manager.
        Starts the command server via CommandServer.
        Displays the greeting animation.
    greeting(): A greeting animation that flashes a sample for fun.

2.5 config.py

The configuration file that sets the application parameters, including the list of tickers with their URLs for each
ticker, process control parameters, and server settings.

3. Workflow

   Initialization: Upon running the main file main.py, the configuration parameters from config.py are initialized, and
   the necessary WebSocket connections for monitoring cryptocurrency prices are set up.

   WebSocket Server Connections: The ConnectionManager object establishes WebSocket connections for each ticker. These
   connections provide real-time data on cryptocurrency prices.

   Message Handling: Depending on the message handler (e.g., default, compact, or all tickers), the messages from the
   server are processed using one of the classes that inherit from MessageHandler.

   Command Management: When the user interacts with the Polybar (e.g., clicking on a ticker), the command server (
   CommandServer) receives the command and passes it to the ConnectionManager, which executes the corresponding action,
   such as switching connections or changing the message handler.

   Server Start: Three processes are run asynchronously:
   The greeting animation.
   Starting all connections through ConnectionManager.
   Starting the command server through CommandServer.

   Shutdown: When the program finishes, the PID file is removed, and any processes using the specified port are
   terminated to prevent conflicts with future runs.

4. Architectural Decisions

   Asynchronous Model: The use of asyncio allows efficient management of multiple connections and tasks, minimizing
   blocking.

   Modularity: The project is divided into separate modules, each with a clear responsibility:
   actions.py: Manages commands and the server.
   utils.py: Provides utility functions for working with processes and PID files.
   message_handlers.py: Separates message handlers for different formats.
   main.py: Contains the main logic to start and coordinate between components.

   Multitasking Support: The application is designed to perform all tasks asynchronously, including establishing
   connections and processing user commands.

   Flexibility: New tickers or configuration parameters can be easily added through config.py without modifying the core
   logic of the application.

5. Future Improvements

   Refactor CommandServer: Simplify the code for handling commands and improve testability.
   Feature Expansion: Add new types of message handlers for more customization options.
   UI Modification: Provide an option to use a graphical interface for displaying data (currently, the project is
   tailored for Polybar).