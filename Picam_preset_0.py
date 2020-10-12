#camera preset 1
#print("Currwnt File Name: " .os.path.basename(__file__))
import glob
import os
import time
import picamera
from picamera import PiCamera
from time import sleep
import Shutter_speeds
from Shutter_speeds import*

#############################################################################################
Start_day = 0 								#Starting day 0-Sunday, 6- Saturday
Stop_day = 6								#Stoping  day 0-Sunday, 6- Saturday
Start_time = "13:00"						#Staerting time
Stop_time = "18:58"							#Stoping time
Interval = "0:10"							#interval
Shutter = 0								#0 = auto, s_60
Sync_to_cloud = True 						#True / False emediatly save on gdrive
Save_to_cloud = True 						#True / False save on gdrive after stop_time
#############################################################################################
camera = PiCamera()

#-------------------------------------naming--------------------------------------------------
def pic_name():																												#reset the counter or continue counting from the last file
	if os.path.isdir('Local/' + time.strftime('%y_%m_%d') + '/') == True:
		try:
			list_of_files = glob.glob('Local/*'+ time.strftime("%y_%m_%d") + '/*')
			latest_file = max(list_of_files, key=os.path.getctime)
			y = int(latest_file.split("-")[1].split(".jpg")[0])
			i = y
			i = i + 1
			Counter = (f"{i:05d}")
			Filename = ("Local/" + time.strftime("%y_%m_%d") + "/IMG_" + time.strftime("%H%M") + "-" + Counter + ".jpg")		##filename formating "20_05_23/IMG_1203-0001.jpg"	
		except:
			i = 0
			i = i + 1
			Counter = f'{i:05d}'
			Filename = ("Local/" + time.strftime("%y_%m_%d") + "/IMG_" + time.strftime("%H%M") + "-" + Counter + ".jpg")		##filename formating "20_05_23/IMG_1203-0001.jpg"
	return Filename
#-------------------------------camera settings-----------------------------------------------
def camera_settings():
	camera.shutter_speed = int(Shutter)*1000	#in MICROseconds
	camera.brightness = 50 						#(0 to 100)
	camera.sharpness = 0 						#(-100 to 100)
	camera.contrast = -10 						#(-100 to 100)
	camera.saturation = -5 						#(-100 to 100)
	camera.iso = 800 							#(100 to 800)
	camera.exposure_compensation = 0	 		#(-25 to 25)
	camera.exposure_mode = 'auto' 				#(off,auto,night,nightpreview,backlight,spotlight,sports,snow,beach,verylong,fixedfps,antishake,fireworks)
	camera.meter_mode = 'average' 				#(average,spot,backlit,matrix)
	camera.awb_mode = 'auto' 					#(off,auto,sun,cloud,shade,tungsten,fluorescent,incandescent,flash,horizon)
	camera.rotation = 0							#rotation 0-270
	camera.hflip = True							#Horisontal flip
	camera.vflip = True							#Vertical filelip
	camera.crop = (0.2,0.2,1,1) 				#(0.0 to 1.0)
	camera.resolution = (4056, 3040)			#Resolution
#---------------------------------take picture------------------------------------------------
def take_picture():
	camera_settings()
	sleep(1)
	camera.capture(pic_name())
