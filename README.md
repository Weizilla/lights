# lights
[![Build Status](https://travis-ci.org/Weizilla/lights.svg?branch=master)](https://travis-ci.org/Weizilla/lights)

Raspberry PI Nightlight Controller

## Installation
1. Install virtualenv
2. Install local python 3: `virtualenv -p python3 venv`
3. Activate virtualenv: `. venv/bin/activate`
4. Install packages: `pip3 -r requirements.txt`

## To Do
1. Sort UI by next run time
2. Improve UI
  1. Use flexbox and div for everything
  2. History is cut off if screen too short
3. Add stop button to clean up gpio and stop server
4. Fix bug where all history shows up as off state
