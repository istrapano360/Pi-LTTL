#first run create folderrs
import os
paths = ["Local/", "gdrive/", "uploaded/"]
for folder in paths:
	if not os.path.exists(folder):
		os.makedirs(folder)
		print("Folder are created")
	else:
		print("Folders already exist")