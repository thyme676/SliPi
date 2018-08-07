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

import time, pi3d, sys
from ruamel.yaml import YAML


#####
# Default Variables
#####

fps = 30
mipmap = False
slides = ['image1.png', 'image2.png']
num_slides = slides.__len__()
delay = 20      # Time per slide, in s
fade_time = 1   # Time to fade, in s
fade_step = 1.0 / (fps * fade_time)

# Screen Display size
height = 1080
width = 1920


#####
# Read variables from config.yaml,
# First checking if config.yaml exists.
#####
yaml = YAML()
with open("config.yaml", 'r') as stream:
    try:
        configs = yaml.load(stream)
#        print(configs)
        if configs[fps]:
            fps = configs[fps]
        if configs[mipmap]:
            mipmap = configs[mipmap]
        if configs[delay]:
            delay = configs[delay]
        if configs[fade_time]:
            fade_time = configs[fade_time]
            fade_step = 1.0 / (fps * fade_time)
        if configs[width]:
            width = configs[width]
        if configs[height]:
            height = configs[width]
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
    slide.texture = pi3d.Texture(file_name, blend=True, mipmap=mipmap, m_repeat=True)
    return slide


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
