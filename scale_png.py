"""This script will scale length and with of a png down by 50%
Check codestyles, etc. 
Count number of files, give information.
"""

from pathlib import Path
from argparse import ArgumentParser
from os import system


def main():
    """Get the path from the argument and shrink all .pngs"""
    parser = ArgumentParser(description="Shrink .pngs by 50%")
    parser.add_argument("--path", help="Location of folder of .pngs to shrink", 
                        default=".")
    parser.add_argument("--scale", help="Scale to shrink (percentage)", 
                        default=50)
    args = parser.parse_args()

    location = Path(args.path)
    # print(location)

    if not location.is_dir():
        print(f"No such folder: {location}")
        raise ValueException
    
    images_folder = location / "images_small"
    images_folder.mkdir(exist_ok=True)

    # print(images_folder)

    for item in location.glob("*.png"):
        command = "convert -resize "
        command += str(args.scale) + "% \""
        command += str(item) + "\" "
        # print(f"{item}")
        new_stem = Path(str(item.stem).replace(" ", "_"))
        smaller_file = item.parents[0] / "images_small" / (new_stem.name + "_small.png")
        # print(f"{smaller_file}")
        command += "\"" + str(smaller_file) + "\""
        system(command)

if __name__ == "__main__":
    main()
