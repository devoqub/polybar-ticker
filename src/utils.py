import fcntl
import os
import signal

import config
import psutil


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
