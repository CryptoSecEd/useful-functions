"""Generate a file with random data
"""

from argparse import ArgumentParser
from pathlib import Path
import os
import sys

BLOCK = 4096


def random_file(filename, size):
    """Generate a file with (size) bytes of random data
    """
    generated = 0
    while generated < size:
        # print(generated, size)
        next_amount = min(BLOCK, size - generated)
        random_bytearray = bytearray(os.urandom(next_amount))
        with open(filename, "ab+") as random_file:
            random_file.write(random_bytearray)
        generated += next_amount
    return True


def main():
    """Get filename and size from user and generate random file"""

    parser = ArgumentParser(description="Generate a file with random data")
    parser.add_argument("--file", help="File to write random data to", 
                        default="rand.dat")
    parser.add_argument("--size", help="Number of bytes to write to file", 
                        default=1024)
    parser.add_argument("--delete", help="Delete file if it already exists", 
                        action="store_true")

    args = parser.parse_args()

    destination = Path(args.file)
    if destination.exists():
        if args.delete:
            print(f"Deleting {destination} ...")
            destination.unlink()
        else:
            print(f"File {destination} already exists")
            sys.exit(1)
    print(f"Writing {args.size} random bytes to {destination}")
    random_file(destination, int(args.size))


if __name__ == "__main__":
    main()
