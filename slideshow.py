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
import random, time, os
import pi3d

#####
# Vars, will be loaded from config in the future.
#####

fps = 30
shader = 'pi3d.Shader("shaders/blend_bump)'
mipmap = 'false'
slides = ['image1.png', 'image.png']
num_slides = slides.__len__()
# Time per slide, in s
delay = 20
# Time to fade, in s
fade_time = 1

# Screen Display size
height = '1920'
width = '1080'
fade_step = 1.0 / (fps * fade_time)


class Slide(object):
    def __int__(self):
        self.texture = None


def tex_load(file_name):
    # Initalize a slide object
    slide = Slide()
    tex = pi3d.Texture(file_name, blend=True, mipmap=mipmap, m_repeat=True)
    slide.tex = tex
    return slide


# Create the display and initalize the canvas
display = pi3d.Display.create(background=(0, 0, 0, 1), frames_per_second=fps)
canvas = pi3d.Canvas()
canvas.set_shader(shader)

# Setup the first slide as background
background_slide = slides[0]

change_time = 0
# change_time = time + delay
i = 0
# Looping Slideshow
while display.loop_running():
    time = time.time()
    if time > change_time:
        # Change slide
        fade = 0
        # Put the old foreground to the back
        foreground_slide = background_slide
        change_time = time + delay
#        slide = tex_load(slides[slide_num])
        # Load Background
        background_slide = tex_load(slides[i])
        # ?? Needed ??
        canvas.set_draw_details(canvas.shader, [sfg.tex, sbg.tex])  # reset two textures
        canvas.set_2d_size(width, height, 0, 0)
        canvas.unif[48:54] = canvas.unif[42:48]  # need to pass shader dimensions for both textures
        canvas.set_2d_size(width, height, 0, 0)
        i += 1

    # Draw Canvas
    canvas.draw()

# Clean up
display.destroy()
