import os
import time
from time import sleep
#restard gdrive

print("unmontirati cu drive")
sleep(1)
os.system("fusermount -u gdrive")
sleep(2)
print("montirati cu drive")
os.system("rclone mount rpi-gdrive: gdrive")



    

#[ -d "/home/pi/Desktop/Scenic/gdrive/Test" ] && echo "Directory /path/to/dir exists."