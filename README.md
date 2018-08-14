# SliPi
Hardware accelerated slideshow for the Raspberry Pi using the Pi3d library.

SliPi was designed to provide a robust solution to running a slideshow info display off
of a Raspberry Pi. This project uses the Pi3d library and shaders included in the pi3d demo library.
Together with this python 3 project a series of slides will continuously display. Screen size,
fade time and more are configurable by using config.yaml (Example included as EXAMPLE_config.yaml).

Copyright © 2018 Mark Williams
Also feel free to submit an issue!

# Author
Mark Williams

# License

This project is licensed under the GPLv3 - see the LICENSE file for details.

Included shaders in shaders directory are subject to MIT license, see included LICENSE file
in shaders directory for more information. Copywrite on these files belongs to its respective
contributors, see LICENSE file in shaders directory for more details.

## Installing
After cloning repo install the requirements with:
`pip3 install -r requirements.txt`

**If using virtual env**
1. Create virtual environment
`virtualenv -p python3 slideshow_env`

2. Activate virtual environment
`source slideshow_env/activate`

3. Install the requirements
`pip3 install -r requirements.txt`


## Running:
After installing, go inside the SliPi directory
`cd SliPi`

Then Rename EXAMPLE_config.yaml to config.yaml
`mv EXAMPLE_config.yaml config.yaml`

Make any changes to this file to change settings.


# TODO
Outstanding features are:
- Dynamically reload the slideshow list on filesystem event.
- Attempt to reload the slideshow on GL error.
- Pull slides from multiple directories, in weighted ammounts.
