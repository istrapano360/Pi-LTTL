# Pi-LTTL
Long term time lapse for Raspberry Pi with HQ camera 1.0

Python 3

*under construction, Scheduler_x.py can be executed manually 

There will be a master scipt to start all in the same time StartTimelapse_1.py

The structure:

 -  Create_folders.py.................... run ones to create file tree (100% Completed)
StartTimelapse_1.py.................. edit for chosing a preset (0% Completed)
  - Scheduler_x.py................... don't edit (100% Completed)
  - Picame_preset-x.py............... edit preset options (90% completed)
  - Sim_upload_x.py.................. don't edit, or only for manualy executing uncomment the presset, or set the desidered time (80% completed)
  - Restart_gdrive.py................ (95% completed)
  Folders:
  - gdrive/.......................................folder mouted remote cloud storage
  - Local/........................................folder where script save the images
  - uploaded/.....................................folder of uploaded files movef from Local/
  
_x are versions of the files  
-x preset index
  
This script is made for using with the pi camsera, however the Scheduler-x.py is calling take_picture() function form Picame_preset_x.py
witch can be also defined with with gphoto2 commands, only make a new Picame_preset_x.py file and don't forget to define in the min 
script StartTimelapse_1.

Modules used:

import pytz

import tzlocal

import datetime

import time

import os

import sys

import socket

import shutil

import subprocess 

from picamera import PiCamera

Before startind with uploading, rclone must be installed and configured. The curren version Sim_upload is made for gdrive use, 
can be edited for any cloud storage, rclone is a powerfull tool. 
For checking if the cloud is mounted the script check if a specific directory on the cloud exsist like a Test folder. Create the Test folder localy in the pool folder, rclone will do the rest. Keep this folder otherwise rclone will delete it from the drive.
Looking for a better solution.
