"""This script will scale length and with of a jpg down by 50%
For png files see scale_png.py
Check codestyles, etc. 
Count number of files, give information.
"""

from pathlib import Path
from argparse import ArgumentParser
from os import system

import platform


def main():
    """Get the path from the argument and shrink all jpgs"""
    parser = ArgumentParser(description="Shrink .jpgs by factor (default 50%)")
    parser.add_argument("--path", help="Location of folder of .jpgs to shrink", 
                        default=".")
    parser.add_argument("--scale", help="Scale to shrink (percentage)", 
                        default="50")
    args = parser.parse_args()

    if platform.system() != "Linux":
        print("This script requires the use of the Linux command 'convert'")
        print(f"Unfortantely, it is not yet supported on {platform.system()}")
        exit(-1)

    location = Path(args.path)
    # print(location)

    if not location.is_dir():
        print(f"No such folder: {location}")
        raise ValueException
    
    images_folder = location / "images_small"
    images_folder.mkdir(exist_ok=True)

    print(f"Shrinking images in {location} and saving them to {images_folder}")

    for item in location.glob("*.jpg"):
        command = "convert -resize "
        command += str(args.scale) + "% \""
        command += str(item) + "\" "
        # print(f"{item}")
        new_stem = Path(str(item.stem).replace(" ", "_"))
        smaller_file = item.parents[0] / "images_small" / (new_stem.name + "_small.jpg")
        # print(f"{smaller_file}")
        command += "\"" + str(smaller_file) + "\""
        # print(command)
        system(command)

if __name__ == "__main__":
    main()
