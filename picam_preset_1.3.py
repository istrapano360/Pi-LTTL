#camera preset 1
import glob
#import os
#print("Currwnt File Name: " .os.path.basename(__file__))
from picamera import PiCamera

#shutter speeds
s8000 = 0.1221		#ms	1/8000
s6400 = 0.1538		#ms	1/6400
s5000 = 0.1938		#ms	1/5000
s4000 = 0.2441		#ms	1/4000
s3200 = 0.3076		#ms	1/3200
s2500 = 0.3875		#ms	1/2500
s2000 = 0.4883		#ms	1/2000
s1600 = 0.6152		#ms	1/1600
s1250 = 0.7751		#ms	1/1250
s1000 = 0.9766		#ms	1/1000
s800 = 1.230		#ms	1/800
s640 = 1.550		#ms	1/640
s500 = 1.953		#ms	1/500
s400 = 2.461		#ms	1/400
s320 = 3.100		#ms	1/320
s250 = 3.906		#ms	1/250
s200 = 4.922		#ms	1/200
s160 = 6.201		#ms	1/160
s125 = 7.813		#ms	1/125
s100 = 9.843		#ms	1/100
s080 = 12.40		#ms	1/80
s060 = 15.63		#ms	1/60
s050 = 19.69		#ms	1/50
s040 = 24.80		#ms	1/40
s030 = 31.25		#ms	1/30
s025 = 39.37		#ms	1/25
s020 = 49.61		#ms	1/20
s015 = 62.50		#ms	1/15
s013 = 78.75		#ms	1/13
s010 = 99.21		#ms	1/10
s08 = 125.0		#ms	1/8
s06 = 157.5		#ms	1/6
s05 = 198.4		#ms	1/5
s04 = 250.0		#ms	1/4
s03 = 315.0		#ms	1/3
s025 = 396.9		#ms	1/2.5
s02 = 500.0		#ms	1/2
s6 = 630.0		#ms	1/1.6
s3 = 793.7		#ms	1/1.3
s1 = 1000.0		#ms	1

s_13 = 1260.0		#ms	1.3
s_16 = 1587.0		#ms	1.6
s_20 = 2000		#ms	2
s_25 = 2052		#ms	2.5
s_30 = 3175		#ms	3
s_40 = 4000		#ms	4
s_50 = 5004		#ms	5
s_60 = 6000		#ms	6

#############################################################################################
Start_day = 1 								#Starting day 0-Sunday, 6- Saturday
Stop_day = 5								#Stoping  day 0-Sunday, 6- Saturday
Start_time = "11:40"						#Staerting time
Stop_time = "18:40"							#Stoping time
Interval = "2:30"							#interval
Shutter = 0									#0 = auto, s_60
Sync_to_cloud = True 						#True / False emediatly save on gdrive
Save_to_cloud = True 						#True / False save on gdrive after stop_time
#############################################################################################
camera = PiCamera()
camera.shutter_speed = (Shutter * 1000)	#in MICROseconds


def create_pool():
	Pool = "/home/pi/Scenic/Local/" + time.strftime("%y%m_%d")			#Capture folder name, differnt settings better different folders
	try:
		os.path.exists(Pool)
	except:
		pass
	else:
		os.makedirs(Pool)
def counter():
	try: 
		list_of_files = glob.glob('/Local/*') # * means all if need specific format then *.csv  Local ali daanašnjem folderu %d
		latest_file = max(list_of_files, key=os.path.getctime)
		y = int(latest_file.split("-")[1].split(".jpg")[0])
	except:
		i = 0
		i = i + 1
		Counter = (f"{i:05d}")
		Filename = (time.strftime("%y%m_%d") + "/IMG_" + time.strftime("H%M") + "-" + Counter + ".jpg")		##filename formating "2005_23/IMG_1203-0001.jpg"
	else:
		i = y
		i = i + 1
		Counter = (f"{i:05d}")
		Filename = (time.strftime("%y%m_%d") + "/IMG_" + time.strftime("H%M") + "-" + Counter + ".jpg")		##filename formating "2005_23/IMG_1203-0001.jpg"
	finally:
		return Filename

def camera_settings():						#Camera_settings
	camera.brightness = 50 					#(0 to 100)
	camera.sharpness = 0 					#(-100 to 100)
	camera.contrast = -10 					#(-100 to 100)
	camera.saturation = -5 					#(-100 to 100)
	camera.iso = 800 						#(100 to 800)
	camera.exposure_compensation = 0	 	#(-25 to 25)
	camera.exposure_mode = 'auto' 			#(off,auto,night,nightpreview,backlight,spotlight,sports,snow,beach,verylong,fixedfps,antishake,fireworks)
	camera.meter_mode = 'average' 			#(average,spot,backlit,matrix)
	camera.awb_mode = 'auto' 				#(off,auto,sun,cloud,shade,tungsten,fluorescent,incandescent,flash,horizon)
	camera.rotation = 0						#rotation 0-270
	camera.hflip = False					#Horisontal flip
	camera.vflip = False					#Vertical filelip
	#camera.capture_raw = True / False #don't know how it works
	camera.crop = (0.2,0.2,1,1) 			#(0.0 to 1.0)
	camera.resolution = (4056, 3040)		#Resolution

def take_picture():
	camera_settings() visak
	camera.capture(counter())
	sleep(1)
	
	