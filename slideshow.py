#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright © 2018 Mark Williams
# slideshow.py

# Pull config vars from slideshow.cfg file
# Search directories
# Initialize the slideshow
# Loop the slideshow
# Check for new slides
# Cleanup

from __future__ import absolute_import, division, print_function, unicode_literals
import time
import pi3d
#import demo # If pi3d isn't installed

#####
# Vars, will be loaded from config in the future.
#####

fps = 30
shader = pi3d.Shader("shaders/blend_bump")
mipmap = False
slides = ['image1.png', 'image2.png']
num_slides = slides.__len__()
# Time per slide, in s
delay = 20
# Time to fade, in s
fade_time = 1
fade_step = 1.0 / (fps * fade_time)

# Screen Display size
height = 1920
width = 1080
tk_windows = False

class Slide(object):
    def __int__(self):
        self.texture = None


def tex_load(file_name):
    # Initialize a slide object
    slide = Slide()
    slide.texture = pi3d.Texture(file_name, blend=True, mipmap=mipmap, m_repeat=True)
    return slide


# Create the display and initalize the canvas
display = pi3d.Display.create(background=(0.0, 0.0, 0.0, 1.0), frames_per_second=fps, tk=tk_windows)
canvas = pi3d.Canvas()
canvas.set_shader(shader)

# Setup the first slide as background
background_slide = tex_load(slides[0])


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
#        slide = tex_load(slides[slide_num])
        # Load Background
        background_slide = tex_load(slides[i])
        # ?? Needed ??
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
