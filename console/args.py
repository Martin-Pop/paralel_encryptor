import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description="Parallel AES-GCM encryptor / decryptor"
    )

    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument(
        "-e", "--encrypt",
        action="store_true",
        help="Encrypt input file"
    )
    mode_group.add_argument(
        "-d", "--decrypt",
        action="store_true",
        help="Decrypt input file"
    )

    parser.add_argument(
        "-i", "--input",
        required=True,
        help="Path to input file"
    )

    parser.add_argument(
        "-o", "--output",
        required=True,
        help="Path to output file"
    )

    parser.add_argument(
        "-c", "--chunk-size",
        type=int,
        default=1024 * 1024, #1MB
        help="Chunk size in bytes (default 1MB)"
    )

    parser.add_argument(
        "-k", "--key",
        required=True,
        help="Encryption key"
    )

    parser.add_argument(
        "-w", "--workers",
        type=int,
        default=4,
        help="Number of worker processes (default 4)"
    )

    return parser.parse_args()
