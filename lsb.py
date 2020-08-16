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
from args import Command, ArgumentsParser
from bitstring import Bits
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
    image = readImage(image_filename)

    pixels = image.load()
    reconstructed_bin = []

    for y in range(image.size[1]):
        for x in range(image.size[0]):
            blue_byte = pixels[x, y][2]
            reconstructed_bin.append(str(blue_byte % 2))

    # Read from bit string up to END_SIGNAL
    d = ''.join(reconstructed_bin)
    d = d[:d.find(END_SIGNAL)]
    data_bytes = Bits(bin=d).tobytes()

    print(f"Read {len(data_bytes)} bytes of data")
    print(f"Writing to file: '{output_filename}'")

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

def inject(image_filename, output_filename, data_filename):
    image = readImage(image_filename)

    try:
        with open(data_filename, "rb") as f:
            data = bin(int.from_bytes(f.read(), byteorder="big"))[2:]
            data = data.zfill(((len(data) // 8) + 1) * 8)
    except FileNotFoundError:
        error(f"File not found: {data_filename}")

    binary_data = data + END_SIGNAL

    if len(binary_data) > image.size[0] * image.size[1]:
        error(f"{data_filename} is too large to be stored inside {image_filename}. Max size is {(image.size[0] * image.size[1]) // 8}")

    lsb_inject_data(image, binary_data)

    print(f"Injected {len(binary_data)//8} bytes of data")
    print(f"Writing to file: '{output_filename}'")

    try:
        image.save(output_filename)
    except ValueError:
        error(f"Could not determine file extension for: '{output_filename}'. Please include a valid image file extension.")
    except OSError as e:
        error(f"{e}. A partial file may have been created.")
    image.close()

    if output_filename[-3:] == "jpg" or output_filename[-3:] == "jpeg":
        print("Please note: writing to a JPEG file can often cause problems due to the lossy compression used.")
        print("If there are problems extracting data from the resulting image, attempt another file format.")

if __name__ == "__main__":
    extract_cmd = Command("extract")
    extract_cmd.add_arg("-i", "--image", description="The image file to be used")
    extract_cmd.add_arg("-o", "--output", default="output.bin", description="The filename to write the extracted file under")

    inject_cmd = Command("inject")
    inject_cmd.add_arg("-i", "--image", description="The image file to be used")
    inject_cmd.add_arg("-o", "--output", default="output.png", description="The filename to write the final image to")
    inject_cmd.add_arg("-d", "--data", description="The data file to be hidden")

    parser = ArgumentsParser()
    parser.add_command(extract_cmd)
    parser.add_command(inject_cmd)

    cmd, values = parser.parse_args(sys.argv)

    if cmd == "extract":
        extract(values["-i"], values["-o"])
    elif cmd == "inject":
        inject(values["-i"], values["-o"], values["-d"])