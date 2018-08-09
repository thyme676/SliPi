#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright © 2018 Mark Williams
# slideshow.py

# Pull config vars from slideshow.cfg file
# Search directories
# Initialize the slideshow
# Loop the slideshow
# Check for new slides
# Cleanup

import time, pi3d, sys, watchdog
import ruamel.yaml as yaml


#####
# Default Variables
#####

fps = 30
mipmap = False
slides = []
num_slides = slides.__len__()
delay = 20      # Time per slide, in s
fade_time = 1   # Time to fade, in s
fade_step = 1.0 / (fps * fade_time)

# Screen Display size
width = 1920
height = 1080

# Slideshow directory
slide_directory = "./"


#####
# Read variables from config.yaml,
# First checking if config.yaml exists.
#####
with open("config.yaml", 'r') as stream:
    try:
        configs = yaml.safe_load(stream)
        if configs['fps']:
            fps = configs['fps']
        if configs['mipmap']:
            mipmap = configs['mipmap']
        if configs['delay']:
            delay = configs['delay']
        if configs['fade_time']:
            fade_time = configs['fade_time']
            fade_step = 1.0 / (fps * fade_time)
        if configs['width']:
            width = configs['width']
        if configs['height']:
            height = configs['height']
        if configs['slide_directory']:
            slide_directory = configs['slide_directory']
    except yaml.YAMLError as error:
        print(error)


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
        print('No slide to load')
    slide.texture = pi3d.Texture(file_name, blend=True, mipmap=mipmap, m_repeat=True)
    return slide

# Add .jpg and .png files to the slide list.
def get_slides(slide_list, directory):
    for file in os.listdir(directory):
        if file.endswith(".png") or file.endswith(".jpg"):
           slide_list.append(file)
    if slide_list.__len__() == 0:
        print('No Slides in directory:' + directory)
    return slide_list


# Add all the slides to the list
get_slides(slides, slide_directory)

# Create the display and initialize the canvas
display = pi3d.Display.create(background=(0.0, 0.0, 0.0, 1.0), frames_per_second=fps, tk=False)
shader = pi3d.Shader("shaders/blend_bump")
canvas = pi3d.Canvas()
canvas.set_shader(shader)

# Setup the first slide as background
background_slide = tex_load(slides[0])

# Setup to trigger first slide.
change_time = 0
# change_time = time + delay
i = 0

# Looping Slideshow
while display.loop_running():
    time_ = time.time()
    if time_ > change_time:
        # Change slide
        fade = 0
        # Put the old foreground to the back
        foreground_slide = background_slide
        change_time = time_ + delay
        # Load Background
        background_slide = tex_load(slides[i])
        canvas.set_draw_details(canvas.shader, [foreground_slide.texture, background_slide.texture])  # reset two textures
        canvas.set_2d_size(width, height, 1.0, 1.0)
        canvas.unif[48:54] = canvas.unif[42:48]  # need to pass shader dimensions for both textures
        canvas.set_2d_size(width, height, 1.0, 1.0)
        i += 1

    if fade < 1.0:
        fade += fade_step
        if fade > 1.0:
            fade = 1.0
    canvas.unif[44] = fade

    # Draw Canvas
    canvas.draw()

# Clean up
display.destroy()
