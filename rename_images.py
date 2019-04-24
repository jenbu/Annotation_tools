import os
import scandir

image_folder = '/home/erlendb/Pictures/Masteroppgave_bilder/KinectNetwork/bilder17_04/'

print(image_folder)
i = 0
for n, image_file in enumerate(scandir.scandir(image_folder)):

    image_name = image_file.name
    print(image_name)
    image_name = image_name[:-4]
    image_name = image_name.replace('.', '_')
    image_name = image_name.replace(':', '_')


    src = image_folder + '/' + image_file.name
    dst = image_folder + '/' + image_name + ".jpg"
    print(dst)


    os.rename(src, dst)
    i = i + 1

