#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Copyright © 2018 Mark Williams
# licensed under GPLv3, see LICENSE for details
# slipi

# Pull config vars from slideshow.cfg file
# Search directories
# Initialize the slideshow
# Loop the slideshow
# Check for new slides
# Cleanup

import time, pi3d, os, stat, sys, re
import ruamel.yaml as yaml
import subprocess
import logging
import logging.handlers
import datetime
import math
import argparse 

MY_PID = os.getpid()
BIN_NAME = os.path.basename(sys.argv[0])


LOGGER = logging.getLogger(BIN_NAME)
syslog_handler = logging.handlers.SysLogHandler(address='/dev/log', facility="daemon")
syslog_handler.setLevel(logging.DEBUG)
syslog_handler.ident = '{}[{}]: '.format(BIN_NAME, MY_PID)
stderr_handler = logging.StreamHandler()
stderr_handler.setLevel(logging.DEBUG)
stderr_handler.ident = '{}[{}]: ]'.format(BIN_NAME, MY_PID)

LOGGER.addHandler(syslog_handler)
#LOGGER.addHandler(stderr_handler)

LOGGER.setLevel(logging.DEBUG)

# Script dir
script_dir = os.path.dirname(os.path.realpath(__file__))
# Config location
config_dir = os.path.dirname(os.path.realpath(__file__))+ "/config.yaml"
# Black image location
black_img = os.path("/var/tmp/slideshow/black.png")

#####
# Default Variables
#####

DEFAULT_CONFIG = {
    'fps': 30,
    'mipmap': False,
    'delay': 20,      # Time per slide, in seconds
    'fade_time': 1,   # Time to fade, in s
    'check_delay': 900, # Time before renewing slide list, in s (900s is 15 min)
    # Screen Display size
    'width': 1920,
    'height': 1080,
    # Shader
    'order': 'sorted',
    'synced': True,
    'shader': 'blend_smooth',
    'shader_directory': './shaders',
    'image_ext_regexp': '\.(png|jpe?g|gif|bmp)$',
    'video_ext_regexp': '\.(mp4|mpeg4|mkv)$',

    # Slideshow directory
    'slide_directory': './'
}

#####
# Read variables from config.yaml,
# First checking if config.yaml exists.
#####

# If called with --config filelocation it will use
# filelocation as the location of config.yaml

parser = argparse.ArgumentParser()
parser.add_argument("--config", help="Specify config.yaml location. \nEx: --config /home/pi/config.yaml",
                                     action="store")
args = parser.parse_args()

if args.config is not None:
        config_dir = args.config

with open(config_dir, 'r') as stream:
    try:
        user_config = yaml.safe_load(stream)
        CONFIG = {**DEFAULT_CONFIG, **user_config}
    except yaml.YAMLError as error:
        print(error)

# Compile regex
CONFIG['image_ext_regexp'] = re.compile(CONFIG['image_ext_regexp'], re.IGNORECASE)
CONFIG['video_ext_regexp'] = re.compile(CONFIG['video_ext_regexp'], re.IGNORECASE)

CONFIG['fade_step'] = 1.0 / (CONFIG['fps'] * CONFIG['fade_time'])

slides = []

# Slide class
class Slide(object):
    def __int__(self):
        self.texture = None

#############
# Functions
#############

# Load Slides from file_name.
def tex_load(file_name):
    # Initialize a slide object
    slide = Slide()
    if file_name is None:
        slide.texture = pi3d.Texture(black_img, blend=True, mipmap=CONFIG['mipmap'], m_repeat=True)

    try:
        slide.texture = pi3d.Texture(file_name, blend=True, mipmap=CONFIG['mipmap'], m_repeat=True)
    except Exception as e:
        LOGGER.error("There was a problem loading slide, {}: {}".format(file_name, e))
        slide.texture = pi3d.Texture(black_img, blend=True, mipmap=CONFIG['mipmap'], m_repeat=True)
    return slide

# Add .jpg and .png files to the slide list.
def get_slides(config):
    directory = config['slide_directory']
    emergency_directory = config['emergency_slide_directory']
    slide_list = []
    emergency_list = []
    try:
        for slide_file in os.listdir(emergency_directory):
            if CONFIG['image_ext_regexp'].search(slide_file) or CONFIG['video_ext_regexp'].search(slide_file):
                emergency_list.append(os.path.join(emergency_directory, slide_file))
    except FileNotFoundError:
        LOGGER.debug("Emergency slide directory doesn't exist")
        emergency_list = []
    for slide_file in os.listdir(directory):
        if CONFIG['image_ext_regexp'].search(slide_file) or CONFIG['video_ext_regexp'].search(slide_file):
           slide_list.append(os.path.join(directory, slide_file))
    if slide_list.__len__() == 0:
        LOGGER.error('No Slides in directory: {}'.format(directory))
    if CONFIG['order'] == 'sorted':
        slide_list = sorted(slide_list)

    if len(emergency_list) > 0:
        slide_list = emergency_list
    LOGGER.debug("Slide list: {}\n".format(", ".join(slide_list)))
    return slide_list

# Initialize the slide list
slides = get_slides(CONFIG)

# Create the display and initialize the canvas
display = pi3d.Display.create(background=(0.0, 0.0, 0.0, 1.0), frames_per_second=CONFIG['fps'], tk=False)
shader = pi3d.Shader(os.path.join(CONFIG['shader_directory'], CONFIG['shader']))
canvas = pi3d.Canvas()
canvas.set_shader(shader)

canvas.set_2d_size(CONFIG['width'], CONFIG['height'], 0, 0)
canvas.unif[48:54] = canvas.unif[42:48]  # need to pass shader dimensions for both textures

for aslide in slides:
   if CONFIG['image_ext_regexp'].search(aslide):
       # Setup the first slide as background
       prev_slide = tex_load(black_img)
       current_slide = tex_load(black_img)
       next_slide = tex_load(black_img)
       canvas.set_draw_details(canvas.shader, [prev_slide.texture, current_slide.texture])  # reset two textures
       break

first_slide = True
i = -1

def get_next_slide_start_time(config):
    global first_slide
    now = datetime.datetime.now().timestamp()
    delay = config['delay']

    if config['synced']:
        #slide_deck_length = len(slides) * config['delay']
        next_slide_time = delay * (now // delay) + delay
        return next_slide_time
    else:
        if first_slide:
            first_slide = False
            return now
        else:
            return now + delay

def next_slide_index(slides, config, next_slide_start_time, last_slide_index):
    now = datetime.datetime.now().timestamp()
    if config['synced']:
        slide_deck_length = len(slides) * config['delay']
        slide_deck_start_time = slide_deck_length * (now // slide_deck_length)
        slide_deck_elapsed_time = next_slide_start_time - slide_deck_start_time
        slide_index = math.floor(slide_deck_elapsed_time // float(config['delay']) - 1)
    else:
        slide_index = (last_slide_index + 1) % len(slides)

    return slide_index

def transition_image(new_image, config, slide_start_time):
    global prev_slide, current_slide, next_slide
    LOGGER.debug("Showing: {}".format(new_image))
    prev_slide = current_slide
    current_slide = next_slide

    transition_time = CONFIG['fade_time']

    transition_step = 1.0 / (CONFIG['fps'] * transition_time)

    transition_value = 0.0

    canvas.set_draw_details(canvas.shader, [prev_slide.texture, current_slide.texture])

    canvas.unif[44] = transition_value

    canvas.draw()

    while(display.loop_running() and transition_value < 1):
        transition_value += transition_step
        if transition_value > 1:
            transition_value = 1
        canvas.unif[44] = transition_value
        #canvas.unif[44] = 0.5
        canvas.draw()
    canvas.draw()

def play_video(video_file):
    global prev_slide, current_slide, next_slide
    LOGGER.debug("Playing: {}".format(video_file))
    prev_slide = tex_load(black_img)
    current_slide = tex_load(black_img)
    next_slide = tex_load(black_img)
    canvas.set_draw_details(canvas.shader, [prev_slide.texture, current_slide.texture])  # reset two textures
    omxplayer_command = ['omxplayer', '--blank', '--aspect-mode', 'stretch', video_file]
    return subprocess.Popen(omxplayer_command)

def advance_slide():
    global slides, next_slide_file, next_slide, next_slide_start_time, i

    slides = get_slides(CONFIG)
    next_slide_start_time = get_next_slide_start_time(CONFIG)
    LOGGER.debug("Next slide will start at, {}".format(next_slide_start_time))

    if len(slides) > 0:
        i = next_slide_index(slides, CONFIG, next_slide_start_time, i)
        next_slide_file = slides[i]
        LOGGER.debug("Next slide: {}".format(next_slide_file))
        if CONFIG['image_ext_regexp'].search(next_slide_file):
            next_slide = tex_load(next_slide_file)
    else:
        LOGGER.debug("Slide directory empty, not advancing")

advance_slide()

while display.loop_running():
    # Draw Canvas
    now = datetime.datetime.now().timestamp()

    if now >= next_slide_start_time:
        slide_start_time = next_slide_start_time
        current_slide_file = next_slide_file
        # Render the next slide
        if CONFIG['image_ext_regexp'].search(current_slide_file):
            LOGGER.debug("New slide is an image, {}".format(current_slide_file))
            transition_image(current_slide_file, CONFIG, slide_start_time)
            advance_slide()
        elif CONFIG['video_ext_regexp'].search(current_slide_file):
            LOGGER.debug("New slide is a video, {}".format(current_slide_file))
            video_proc = play_video(current_slide_file)
            advance_slide()
            video_result = video_proc.wait()
        else:
            LOGGER.debug("New slide is something unknown...")
            advance_slide()
    else:
        canvas.draw()

# Clean up
display.destroy()
