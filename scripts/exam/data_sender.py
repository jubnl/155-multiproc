import random
import socket
from datetime import datetime


class Log:
    def __init__(self, level: str = None, logger: str = None, message: str = None):
        self.level = level or 'DEBUG'
        self.logger = logger or 'DefaultLogger'
        self.message = message or 'Default log message'

    def __str__(self):
        return f'{datetime.now().strftime("%d-%m-%Y %H:%M:%S")} :: {self.level} :: {self.logger} :: {self.message}ENDOFLOG'


log_level_pool = [
    'TRACE',
    'DEBUG',
    'INFO ',
    'WARN ',
    'ERROR',
    'FATAL'
]

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

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    for _ in range(50):
        log = Log(
            level=random.choice(log_level_pool),
            logger=random.choice(logger_pool),
            message=random.choice(message_pool)
        )
        s.send(str(log).encode())
