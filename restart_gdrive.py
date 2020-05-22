import os
import time
from time import sleep
#restart gdrive

print("I will unmount gdrive")
sleep(1)
os.system("fusermount -u gdrive")
sleep(2)
print("I will mount the gdrive")
os.system("rclone mount rpi-gdrive: gdrive")
