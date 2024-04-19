import random
import socket
from datetime import datetime


class Log:
    def __init__(self, level: str = None, logger: str = None, message: str = None):
        self.level = level or 'DEBUG'
        self.logger = logger or 'DefaultLogger'
        self.message = message or 'Default log message'
        self.dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return f'{self.dt} :: {self.level} :: {self.logger} :: {self.message}ENDOFLOG'


# do not change the log_level_pool
log_level_pool = [
    'TRACE',
    'DEBUG',
    'INFO ',
    'WARN ',
    'ERROR',
    'FATAL'
]

# You can add more loggers and messages to the pools
logger_pool = [
    'AuthLogger',
    'PaymentLogger',
    'MainLogger',
    'UserActivityLogger',
    'ErrorLogger'
]

message_pool = [
    'User logged in',
    'Payment processed',
    'An error occurred',
    'User logged out',
    'Data updated',
    'Transaction failed',
    'User registered',
    'Password changed',
    'Session expired',
    'New connection established'
]

host = 'localhost'
port = 12345

if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        logs = ''.join([str(Log(
            level=random.choice(log_level_pool),
            logger=random.choice(logger_pool),
            message=random.choice(message_pool)
        )) for _ in range(100)]).encode()
        s.send(logs)
