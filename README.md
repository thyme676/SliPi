# SliPi
Python 3 hardware accelerated slideshow for the Raspberry Pi using the Pi3d library.

SliPi was designed to provide a robust solution to running a slideshow info display off
of a Raspberry Pi. This project uses the Pi3d library and shaders included in the pi3d demo library.
Together with this python 3 project a series of png or jpg images will continuously display.
Recent versions can also play .mp4 videos using omxplayer.
Screen size, fade time and more are configurable by using config.yaml
(Example included as EXAMPLE_config.yaml).

Copyright © 2019 Mark Williams

Please submit issues!

## Author
Mark Williams

## License

This project is licensed under the GPLv3 - see the LICENSE file for details.

Included shaders in shaders directory are subject to MIT license, see included LICENSE file
in shaders directory for more information. Copyright on these files belongs to its respective
contributors, see LICENSE file in shaders directory for more details.

## Installing
To play videos in the mp4 format omxplayer must be installed.
On ubuntu use apt to install it:

`$ sudo apt install omxplayer`

Otherwise videos will not play.

Another dependency are the dev jpeg libraries

libjpeg8-dev zlib1g-dev
Install these using apt before proceeding. 
`$sudo apt install libjpeg8-dev zlib1g-dev`

Then clone the repo: 

`$ git clone https://github.com/thyme676/SliPi.git`

After cloning repo install the requirements

`$ pip3 install -r requirements.txt`

**If using virtual env**
1. Create virtual environment

`$ virtualenv -p python3 slideshow_env`

2. Activate virtual environment

`$ source slideshow_env/bin/activate`

If successful (slideshow_env) should show before your shell
(slideshow_env) pi@raspberry:~/SliPi $

3. Install the requirements

`$ pip3 install -r requirements.txt`


## Running:
After installing, go inside the SliPi directory

`$ cd SliPi`

Then Rename EXAMPLE_config.yaml to config.yaml

`$ mv EXAMPLE_config.yaml config.yaml`

Make any changes to this file to change settings.

Start the Slideshow

`python3 slideshow.py`

## TODO
Outstanding features are:
- ~~Dynamically reload the slideshow list on filesystem event.~~
- ~Play videos.~
- Attempt to reload the slideshow on GL error.
- Pull slides from multiple directories, in weighted amounts.
