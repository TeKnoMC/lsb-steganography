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

from PIL import Image, UnidentifiedImageError
from args import Command, Arguments
import sys

END_SIGNAL = bin(int.from_bytes(b"MSGEND", byteorder="big"))[2:]
END_SIGNAL = END_SIGNAL.zfill(((len(END_SIGNAL) // 8) + 1) * 8)

def error(msg):
    print(f"error: {msg}")
    sys.exit()

def readImage(image_filename):
    try:
        return Image.open(image_filename)
    except FileNotFoundError:
        error(f"File not found: {image_filename}")
    except UnidentifiedImageError:
        error(f"{image_filename} is likely not an image")

def extract(image_filename, output_filename):
    # Read LSB data and write to file
    image = readImage(image_filename)

    pixels = image.load()
    reconstructed_bin = []

    for y in range(image.size[1]):
        for x in range(image.size[0]):
            blue_byte = pixels[x, y][2]
            reconstructed_bin.append(str(blue_byte % 2))

    d = ''.join(reconstructed_bin)
    d = d[:d.find(END_SIGNAL)]
    data_bytes = int(d, 2).to_bytes(len(d) // 8, byteorder='big')

    #byte_array = bytes([int(''.join(reconstructed_bin[i:i+8]), 2) for i in range(0, len(reconstructed_bin), 8)])

    with open(output_filename, "wb") as f:
        f.write(data_bytes)

    image.close()

def lsb_inject_data(image, data):
    pixels = image.load()
    for y in range(image.size[1]):
        for x in range(image.size[0]):
            idx = x + y * image.size[0]
            if idx >= len(data):
                return
            else:
                pixels[x, y] = (pixels[x, y][0], pixels[x, y][1], pixels[x, y][2] & 0xfe | int(data[idx]))
            print(f"{data[idx]}: {bin(pixels[x, y][2])}")

def inject(image_filename, output_filename, data_filename):
    # Read data, write to LSB, and write to file
    image = readImage(image_filename)

    try:
        with open(data_filename, "rb") as f:
            data = bin(int.from_bytes(f.read(), byteorder="big"))[2:]
            data = data.zfill(((len(data) // 8) + 1) * 8)
    except FileNotFoundError:
        error(f"File not found: {data_filename}")

    binary_data = data + END_SIGNAL

    if len(binary_data) > image.size[0] * image.size[1]:
        error(f"{data_filename} is too large to be stored inside {image_filename}")

    lsb_inject_data(image, binary_data)

    image.save(output_filename)

    image.close()

if __name__ == "__main__":
    extract_cmd = Command("extract")
    extract_cmd.add_arg("-i", "--image", description="The image file to be used")
    extract_cmd.add_arg("-o", "--output", default="extracted_data", description="The filename to write the extracted file under")

    inject_cmd = Command("inject")
    inject_cmd.add_arg("-i", "--image", description="The image file to be used")
    inject_cmd.add_arg("-o", "--output", default="steg_img.png", description="The filename to write the final image to")
    inject_cmd.add_arg("-d", "--data", description="The data file to be hidden")

    parser = Arguments()
    parser.add_command(extract_cmd)
    parser.add_command(inject_cmd)

    cmd, values = parser.parse_args(sys.argv)

    if cmd == "extract":
        extract(values["-i"], values["-o"])
    elif cmd == "inject":
        inject(values["-i"], values["-o"], values["-d"])