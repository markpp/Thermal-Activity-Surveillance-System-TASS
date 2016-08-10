import os, sys
path = sys.argv[1]
for filename in os.listdir(path):
	num = os.path.splitext(filename)[0]
	num = num.zfill(6)
	new_filename = "frame_" + num + ".png"
	print filename
	os.rename(os.path.join(path, filename), os.path.join(path, new_filename))
	