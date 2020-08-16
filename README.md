# lsb-steganography
A small python command line program to facilitate hiding data in the Least Significant Bit of pixels in an image.

## Installation
It is recommended to use a python virtual environment to install the requirements for this program. The following commands will create a new environment and install the requirements:
```bash
git clone https://github.com/TeKnoMC/lsb-steganography.git && cd lsb-steganography
python -m venv venv; source venv/bin/activate; python -m pip install -r requirements.txt
```

## Usage
```
python lsb.py [command] <arguments>

Available commands:
extract
	-i/--image           The image file to be used
	-o/--output          The filename to write the extracted file under
inject
	-i/--image           The image file to be used
	-o/--output          The filename to write the final image to
	-d/--data            The data file to be hidden
```