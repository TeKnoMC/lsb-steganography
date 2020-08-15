"""
lsb.py:
  A tool to hide data inside of the LSB in pixel data of an image

Usage:
python lsb.py [command] <arguments>

Available commands:
extract
	-i/--image           The image file to be used
	-o/--output          The filename to write the extracted file under
inject
	-i/--image           The image file to be used
	-o/--output          The filename to write the final image to
	-d/--data            The data file to be hidden
"""

from PIL import Image
from args import Command, Arguments
import sys

def extract(image_filename, output_filename):
    # Read LSB data and write to file
    pass

def inject(image_filename, output_filename, data_filename):
    # Read data, write to LSB, and write to file
    pass

if __name__ == "__main__":
    extract_cmd = Command("extract")
    extract_cmd.add_arg("-i", "--image", description="The image file to be used")
    extract_cmd.add_arg("-o", "--output", default="extracted_data", description="The filename to write the extracted file under")

    inject_cmd = Command("inject")
    inject_cmd.add_arg("-i", "--image", description="The image file to be used")
    inject_cmd.add_arg("-o", "--output", default="steg_img", description="The filename to write the final image to")
    inject_cmd.add_arg("-d", "--data", description="The data file to be hidden")

    parser = Arguments()
    parser.add_command(extract_cmd)
    parser.add_command(inject_cmd)

    cmd, values = parser.parse_args(sys.argv)

    if cmd == "extract":
        print(f"extracting {values}")
    elif cmd == "inject":
        print(f"injecting {values}")