import uuid


def is_valid_UUID(candidate):
    try:
        uuid.UUID(str(candidate))
        return True
    except ValueError:
        return False
