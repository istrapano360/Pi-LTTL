#cloud upload script under construction
import pytz
import tzlocal
import datetime
import time
import os
import sys
import shutil
import socket
import subprocess
from time import sleep
"""
TO BE DONE import from the main file "Start_timelapse.py" a variable that define witch variables will be imported
from specified preset
from Start_timelapse import Preset  #Preset = Picam-preset_1
from Preset import Start_day, Stop_day, Sync_to_cloud, Save_to_cloud, Stop_time, Start_time, sync, upload, restart_cloud
"""

#########  -  uncomment for manually run  -  #################
#from picam_preset_1 import start_day, stop_day, Sync_to_cloud, Save_to_cloud, stop_time, start_time, sync, upload, restart_cloud
Start_day = 0			#only import from preset
Stop_day = 6			#only import from preset
Sync_to_cloud = False	#only import from preset
Save_to_cloud = True	#only import from preset
Start_time = "8:00"		#only import from preset
Stop_time = "18:00"		#only import from preset

#############  -  Custom time  -  only for 2. option ########
#sch_time()					#auto
Time_upload = "18:00"		#manually
Time_upload_str = (sum(x * int(t) for x, t in zip([3600, 60, 1], Time_upload.split(":"))))
#############################################################

x = datetime.datetime.utcnow()															#UTC time 
Local_timezone = tzlocal.get_localzone()												#Time Zone 
Moment_utc = x.replace(tzinfo=pytz.utc).astimezone(Local_timezone) 						#UTC Time Zone
Moment =(Moment_utc.strftime("%X"))														#time now in hh:mm:ss
Start_str = (sum(x * int(t) for x, t in zip([3600, 60, 1], Start_time.split(":"))))		#string time start now in seconds
Stop_str = (sum(x * int(t) for x, t in zip([3600, 60, 1], Stop_time.split(":"))))		#string time stop now in seconds
Time_now_str = (sum(x * int(t) for x, t in zip([3600, 60, 1], Moment.split(":"))))		#string time now in seconds
Day_now = Moment_utc.strftime("%w")														#day of the week 0-6 in the time zone
cloud_path = "/home/pi/Desktop/Timelapse/gdrive"										#location of gdrive
destination = "uploaded/"																#moved uploaded files 
checkfile = "logfile.txt"																#log file from rclone check
local = "Local/"

#--------------------------------- Day -------------------------------------------------
def today():											#F Return today day int
	return Day_now
	print("today is today")#---------------------------

#-------------------------------- Clock ------------------------------------------------
def clock(): 											#F Return time in second string
	return Time_now_str
	print("now is current time ")#---------------------------

#-------------------------------scheduler  ---------------------------------------------
def sch_start_time(): 									#Operating_T True/ False
	global Operating_T, Time_now_str, Start_time_str, Stop_time_str
	if Start_time <= Stop_time:
		clock()
		if Time_now_str >= Start_time_str and Time_now_str < Stop_time_str:
			Operating_T = True
		else:
			Operating_T = False	
	elif Start_time > Stop_time:
		clock()
		if not Time_now_str > Start_time_str or Time_now_str < Stop_time_str:
			Operating_T = True
		else:
			Operating_T = False
	return Operating_T
	
def sch_start_day(): 									#Operating_D True/ False
        global Operating_D, Time_now_str, Start_day, Stop_day
	if Start_day <= Stop_day:
                today()
		if Day_now >= Start_day and Day_now <= Stop_day:
			Operating_D = True
		else:
			Operating_D = False
	elif Start_day > Stop_day:
		today()
		if not Day_now >= Start_day or Day_now <= Stop_day:
                	if Day_now > Start_day:
				Operating_D = True
			else:
				Operating_D = False
	return Operating_D

#----------------------------  Ping google  --------------------------------------------
def raspberry_online():									#V Raspberry_online True/ False
	print(" check if is online ")
	global Raspberry_online, Cloud_online
	try:
		socket.create_connection(('Google.com', 80)) # ####################################  google or default server gateway
	except OSError:
		Raspberry_online = False
		return Raspberry_online
		Cloud_online == False
		return Cloud_online
		print("Offline")#---------------------------
	else:
		Raspberry_online = True
		return Raspberry_online
		print("Online")#---------------------------
	finally:
		pass

#------------------------- check cloud online ------------------------------------------ #####
def cloud_check():										#V Cloud_online True/ False
	print(" check if the gdrive is mounted ")
	global Cloud_online
	try:
		os.path.ismount(cloud_path)
	except:
		Cloud_online = False
		return Cloud_online
		print("Not mounted")#---------------------------
	else:
		Cloud_online = True
		return Cloud_online
		print("Mounted")#---------------------------
	finally:
		pass
"""
----------------------------------- Late upload ---------------------------------------
ther is a problem, if a time lapse ends in 23:50 and the next day is a non working day
the upload will have only 10 minutes to run and it will not be completed, the upload
will coninue next working day again after 23:50, but will have two days of files to
upload. To overcome this probelm the next stsment will ignore the Shedule_day to make
it work one more day this is for fail safe safety
"""

##ovaj dio nije gotov upload_check() ####################################################################################

late_upload() #upload_check()
upload_check() 
sync_to_cloud() #upload_check()
save_to_cloud() #upload_check()
restart_cloud() #odvojiti procese

################################
def late_upload(): 							#V Operating_D True/False   Stop_str > 82800
	global Cloud_online
	print("Not a working day, if fail will continue next working day")
	if Error_upload == True and Cloud_online == True and New_day == False and Raspberry_online == True:
		print("Uploading in a non working day...")
		upload()
		upload_check()
		raspberry_online()
	elif Error_upload == False:
		print("Succes upload, new upload schedule next scheduled day!")
		New_day == True
	elif Cloud_online == False or Raspberry_online == False:
		print("Cheking internet and restarting cloud")
		restart_cloud()
		cloud_check()
		raspberry_online()
		sleep(120)
	pass

#-------------------------- check uploaded data -----------------------------------------
def upload_check():
	print(" check if all files are uploaded ")
	global Error_upload 
	os.system("rclone check 'Local' 'gdrive' --one-way  -vv -P --combined logfile.txt")
	destination = "uploaded/"
	checkfile = "logfile.txt"
	search = "=" # move from the folder successfuly uplouded files

	list_of_files = []
	lines = []
	folders = []
	uniq_folder_list = []
	shutil_l = []
	shutil_f = []
	
	for line in open(checkfile, "r"):
		if search in line:
			list_of_files = line.split("/")[1]
			lines.append(list_of_files.rstrip())
			list_of_folders = line.split(" ")[1].split("/")[0]
			folders.append(list_of_folders.rstrip())
	[uniq_folder_list.append(n) for n in folders if n not in uniq_folder_list] 
	for new_folder in uniq_folder_list:
		if not os.path.exists(destination + new_folder):
			os.makedirs(destination + new_folder)
	for l, f in zip(lines, folders):
		l1 = (local + f + "/" + l)
		f1 = (destination + f)
		shutil_l.append(l1.rstrip())
		shutil_f.append(f1.rstrip())
	for src, dest in zip(shutil_l, shutil_f):
		shutil.move(src,dest)

	os.system("rclone check 'Local' 'gdrive' --one-way  -vv -P --combined logfile.txt")
	with open(checkfile, 'r') as read_obj:
		one_char = read_obj.read(1)
		if not one_char:
			Error_upload = False
			return Error_upload
			print("all files are online")
		else:
			Error_upload = True
			return Error_upload
			print("Not uploaded ")
			
#----------------------- upload after taking picture ------------------------------------
def	sync_to_cloud(): #Cloud_online == True ## New_day == False ## Raspberry_online == True
		if Operating_T == True and Operating_D == True and Cloud_online == True and New_day == False and Raspberry_online == True:  #working time is not over 
			sch_time()
			sch_day()
			try:
				sync() #no  --checksum, faster upload, if is done before stop time just wait 2 min and resart
			except:
				print("Disconnected!!")
			pass
			upload_check()
			raspberry_online()
			cloud_check()
			sleep(1)
			if Operating_T == False and New_day == False and Raspberry_online == True: 	 #working time is over no new picture will be taken
				if Cloud_online == True and New_day == False and Raspberry_online == True:
					upload_check()
					reupload()
				pass
			pass
		elif Cloud_online == False and Raspberry_online == True:
			restart_cloud()
			sleep(5)
		pass

##----------------------- upload after timelapse stopped ----------------------------------- #####
def	save_to_cloud(): # Upload to cloud after working day is over and stops before time lapse starts
	upload_check()
	if Operating_T == True and Operating_D == True and Cloud_online == True and New_day == False and Raspberry_online == True:
		sch_time()
		sch_day()
		try:
			upload() ##########################In case of lost connection break
		except:
			print("Disconnected!!")
		pass
		upload_check()
		raspberry_online()
		reupload()
	pass

##----------------------- upload after timelapse stopped ----------------------------------- #####
def reupload():							#reupload after checking if data on cloud is not completed
	if Error_upload == True and Cloud_online == True and New_day == False and Raspberry_online == True:
		print("Upload all and repeat!")
		seelp(2)
		try:
			upload() ##########################In case of lost connection break
		except:
			print("Disconnected!!")
		pass
		upload_check()
		raspberry_online()
		cloud_check()
	elif Error_upload == False and New_day == False and Raspberry_online == True:
		print("Succes upload, new upload schedule tomorrow!")
		New_day == True
	elif Cloud_online == False and Raspberry_online == True:
		restart_drive()
		upload_check()
		cloud_check()
		sleep(120)
	pass

################# will be defined in picam_reset_1  ######################
def sync():
	print("rclone Sync function")#-------------------------------------
	os.system("rclone --ignore-existing sync 'Local' gdrive -P -vv --dry-run") # -P -vv -dry-run
	sleep(300)

def upload():
	print("rclone Upload function")#-------------------------------------
	os.system("rclone --checksum --ignore-existing sync 'Local' gdrive -P -vv --dry-run") # -P -vv -dry-run

def restart_cloud(): ## subprocces and check for other procces and kill it
	try:
		Raspberry_online == True
	except:
		print("Not online")
	else:
		#os.system("fusermount -u gdrive")
		sleep(1)
		#os.system("rclone mount rpi-gdrive: gdrive")
		sleep(1)
		cloud_check()
	finally:
		pass

# ############################  - Main loop  -  ##########################

Error_upload = True
New_day = True
Operating_D = False
Operating_T = False
Sync_to_cloud = False
Save_to_cloud = False
Check = True
while True:
#	restart_cloud()
	raspberry_online()
	sch_day()
	New_day = False
	if Operating_D == True and New_day == False and Raspberry_online == True:
		sch_day()
		sch_time()
		
		if Sync_to_cloud == True and Save_to_cloud == False and New_day == False and Raspberry_online == True:
			sync_to_cloud() #syncronise every 2 min with the cloud
		
		elif Sync_to_cloud == False and Save_to_cloud == True and New_day == False and Raspberry_online == True:
			save_to_cloud() #upload after working our all files until starting time
		
		elif Raspberry_online == False:
			raspberry_online() # raspberry not online
			sleep(300)
		elif Sync_to_cloud == True and Save_to_cloud == True:
			print("Chose Sync or Save")
			break
		elif Sync_to_cloud == False and Save_to_cloud == False:
			print("Sync or Save not working")
			break
		else:
			print("done for today")
			Check = True
			Return Check
	elif Operating_D == False and Error_upload == True and Stop_str > 82800: #23:00 in seconds
		late_upload()
		sch_day()
		sch_time()
		Check = True
		Return Check
	elif Operating_D == False and Check == True:
		print("Upload will continue next scheduled day")
		sch_day()
		Check = False
		Return Check
		sleep(600)
pass
