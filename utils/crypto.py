import hashlib

def derive_key_from_string(password):
    """
    Creates a derived key from a password.
    :param password: password to derive key from
    :return: key derived from password
    """
    # UTF-8 -> bytes -> SHA256 -> 32 B key
    return hashlib.sha256(password.encode("utf-8")).digest()