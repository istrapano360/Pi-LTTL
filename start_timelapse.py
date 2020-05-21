import os
import time
import subprocess
from time import sleep
from picam_preset_1 import *
#start timelapse

if sync_to_gdrive == True or save_to_drive == True:
	subprocess.run("python Timelapse_master_1.py & sim_upload.py", shell = True)
	print("timelapse and upload")	
else:
	os.system("python Timelapse_master_1.py")
	print("timelapse only")