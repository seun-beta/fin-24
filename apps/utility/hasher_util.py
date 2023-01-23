import argon2
from argon2 import PasswordHasher

pin_hasher = PasswordHasher(
    time_cost=3,
    memory_cost=64 * 1024,
    parallelism=1,
    hash_len=32,
    salt_len=16,
)


def hash_pin(pin: int) -> str:
    return pin_hasher.hash(pin)


def verify_pin(pin: int, pin_hash_value: str) -> bool:
    try:
        return pin_hasher.verify(pin_hash_value, pin)

    except argon2.exceptions.VerifyMismatchError:
        return False
