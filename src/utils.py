import argparse
import asyncio
import signal
import psutil
import fcntl
import os

import config


def kill_pid_from_file():
    """Kills process by PID from file."""

    if os.path.exists(config.TEMP_PID_PATH):
        with open(config.TEMP_PID_PATH, "r", encoding="utf-8") as file:
            content = file.read().strip()
            if content:
                pid = int(content)
                try:
                    os.kill(pid, signal.SIGTERM)
                except Exception as e:
                    pass


def create_pid_file():
    """Create and lock the PID file."""

    try:
        pid_file_fd = open(config.TEMP_PID_PATH, 'w')
        fcntl.flock(pid_file_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        pid_file_fd.write(str(os.getpid()))
        pid_file_fd.flush()

    except:
        pass


def kill_process_by_port(port):
    """Killing processes running on {{port}}"""

    for proc in psutil.process_iter(["pid", "name", "connections"]):
        try:
            # Проверяем, есть ли соединения у процесса
            if proc.info["connections"] is not None:
                for conn in proc.info["connections"]:
                    if conn.laddr.port == port:
                        pid = proc.info["pid"]
                        print(
                            f"Процесс с PID {pid} использует порт {port}. Убиваем процесс..."
                        )
                        os.kill(pid, 9)
                        return
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    print(f"Процесс, использующий порт {port}, не найден.")


async def greeting(event: asyncio.Event):
    """Greeting message, just for fun"""

    try:
        while not event.is_set():
            print("", flush=True)
            await asyncio.sleep(config.BLINK_KAOMOJI_REPEAT_TIME)
            print(config.BLINK_KAOMOJI, flush=True)
            await asyncio.sleep(config.BLINK_KAOMOJI_REPEAT_TIME)
    except asyncio.CancelledError:
        pass


def init_parser() -> argparse.ArgumentParser:
    """Argparse init"""

    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", help="Enable Debug mode", action="store_true")
    parser.add_argument("--cli", help="Use display for CLI interface (Future)", action="store_true")

    return parser
