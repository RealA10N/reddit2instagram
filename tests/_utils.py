import pytest


def log_records_below(level: int):
    def decorator(func):
        def wrapper(caplog):
            func()

            for record in caplog.records:
                if record.levelno >= level:
                    pytest.fail(
                        f'Captured a {record.levelname}'
                    )

        return wrapper
    return decorator
