#it will unmount and mount the gdrive in specified folder
import os
import time
from time import sleep
#restart gdrive
# "gdrive" is a local folder in current directory, 
#"rpi-gdrive" is a profile create with rclone
#need to be first configured and used any name you want

print("I will unmount gdrive")
sleep(1)
os.system("fusermount -u gdrive")
sleep(2)
print("I will mount the gdrive")
os.system("rclone mount rpi-gdrive: gdrive")
