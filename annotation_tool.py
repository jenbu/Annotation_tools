import os
import matplotlib.pyplot as plt

import cv2
import datetime as dt
import numpy as np
from generate_xml import write_xml
from matplotlib.widgets import RectangleSelector
import scandir
import random

#Add desired classes
classes = {
    0: "box_end",
    1: "pin_end",
    2: "pipe_connection"
}

image_folder = 'images03.04.19'
image_path = None
savedir = 'xml_filer03.04.19'
objType = 0

#global constants
img = None
tl_list = []
br_list = []
object_list = []
save = False
running = True
isSaved = False





def line_selec_callback(clk, rls):
    global tl_list
    global br_listb
    global save

    if save:
        print("La til et objekt av typen %s til liste" % classes[int(objType)])
        tl_list.append((int(clk.xdata), int(clk.ydata)))
        br_list.append((int(rls.xdata), int(rls.ydata)))
        object_list.append(int(objType))
        save = False


def onkeypress(event):
    global object_list
    global tl_list
    global br_list
    global img
    global save
    global objType
    global isSaved
    if event.key == 'c':
        objType = objType + 1
        if objType == 2:
            objType = 0
        print("Current type:" + classes[int(objType)])

    if event.key == 'b':
        save = True

    if event.key == 't':
        tl_list = []
        br_list = []
        object_list = []
        print("Resetted")
    if event.key == 'q':
        print(tl_list, br_list, object_list)
        #write_txt_file(tl_list, br_list, object_list)
        if len(object_list) > 0:
            write_xml(image_folder, img, object_list, tl_list, br_list, savedir, 0)
            mirror(image_folder, savedir, img, tl_list, br_list, object_list)
            scale(image_folder, savedir, img, tl_list, br_list, object_list)
            translation(image_folder, savedir, img, tl_list, br_list, object_list)
            print("Skrev til xml")
        tl_list = []
        br_list = []
        object_list = []
        img = None
        plt.close()

    if event.key == 'm':
        plt.close()
        #if not isSaved:
            #write_txt_file(tl_list, br_list, object_list)

        global running
        global annotation_file
        #annotation_file.close()
        running = False


def toggle_selector(event):
    toggle_selector.RS.set_active(True)

def write_txt_file(tl, br, obj):
    tl_arr = np.asarray(tl)
    br_arr = np.asarray(br)
    obj_arr = np.asarray(obj)
    global annotation_file
    #print(obj_arr.shape[0])
    tot_arr = np.empty([obj_arr.shape[0], 5])
    #print(tot_arr)
    #print(tl_arr.shape)
    print("topleft: %s\n bottomright: %s" % (str(tl_arr), str(br_arr)))

    #Gjoer at man faar minste verdier foerst, sjekk denne!
    for g in range(0, tl_arr.shape[0]):
        for h in range(0, 2):
            if tl_arr[g,h] > br_arr[g,h]:
                temp_arr = tl_arr
                #tl_arr[g,h] = br_arr[g,h]

    print("topleft: %s\n bottomright: %s" % (str(tl_arr), str(br_arr)))

    annotation_file.write(str(image_path) + " ")

    k = 0
    for j in range(0, obj_arr.shape[0]):
        for i in range(0, 5):

            if i <= 1:
                tot_arr[j, i] = tl_arr[j, k]
                k += 1
            elif i > 1 and i <= 3:
                tot_arr[j, i] = br_arr[j, k]
                k += 1
            elif i == 4:
                tot_arr[j, i] = obj_arr[j]
                k = 0

            if k == 2:
                k = 0

            if i != 4:
                annotation_file.write(str(int(tot_arr[j, i]))+",")
            else:
                annotation_file.write(str(int(tot_arr[j, i])) + " ")
    annotation_file.write("\n")
    print(tot_arr)

def mirror(image_src, xml_path, image, tl, br, obj):
    image_cv = cv2.imread(image.path)
    image_flipped = cv2.flip(image_cv, 1)
    tl_mirrored = []
    br_mirrored = []

    height, width, depth = image_cv.shape
    print(len(tl))

    for i in range(0,len(tl)):
        tl_mirrored.append((width-br[i][0], tl[i][1]))
        br_mirrored.append((width-tl[i][0], br[i][1]))
        #cv2.rectangle(image_flipped, tl_mirrored[i], br_mirrored[i], (255, 0, 0), 1)

    cv2.imwrite(image_src + "/" + "m" +image.name, image_flipped)

    #Safeguard to prevent xml file writing with a non existent image
    if os.path.isfile(image_src + "/" + "m" +image.name):
        print("writing translated xml_file")
        write_xml(image_src, image, obj, tl_mirrored, br_mirrored, xml_path, 1)


def scale(image_src, xml_path, image, tl, br, obj):
    image_cv = cv2.imread(image.path)
    tl_scaled = []
    br_scaled = []

    #Scaling factors
    fx = random.uniform(0.75, 1.25)
    fy = random.uniform(0.75, 1.25)
    scaled_img = cv2.resize(image_cv, None, fx=fx, fy=fy, interpolation=cv2.INTER_CUBIC)
    print("%f %f" % (fx, fy))

    for i in range(0,len(tl)):
        tl_scaled.append((int(fx*tl[i][0]), int(fy*tl[i][1])))
        br_scaled.append((int(fx*br[i][0]), int(fy*br[i][1])))
        #cv2.rectangle(scaled_img, tl_scaled[i], br_scaled[i], (255, 0, 0), 1)

    write_xml(image_src, image, obj, tl_scaled, br_scaled, xml_path, 2)
    cv2.imwrite(image_src + "/" + "s" + image.name, scaled_img)

def translation(image_src, xml_path, image, tl, br, obj):
    image_cv = cv2.imread(image.path)
    tl_translated = []
    br_translated = []
    height, width, depth = image_cv.shape



    #translation factors

    factor = 0.2

    tx = random.randint(-int(width*factor), int(width*factor))
    ty = random.randint(-int(height*factor), int(height*factor))
    #Translation matrix
    M = np.float32([[1, 0, tx], [0, 1, ty]])

    translated_image = cv2.warpAffine(image_cv, M, (width, height))

    print("%f %f" % (tx, ty))

    for i in range(0,len(tl)):
        if ((tx+tl[i][0]) > width and (tx+br[i][0]) > width) or ((tx+tl[i][0]) < 0 and (tx+br[i][0]) < 0):
            print("bb er utenfor x-omraade")
            continue
        if ((ty+tl[i][1]) > height and (ty+br[i][1]) > height) or ((ty+tl[i][1]) < 0 and (ty+br[i][1]) < 0):
            print("bb er utenfor y-omraade")
            continue



        tl_translated.append(((tx+tl[i][0] if (tx+tl[i][0]) > 0 else 0), (ty+tl[i][1] if (ty+tl[i][1] > 0) else 0)))
        br_translated.append(((tx+br[i][0] if (tx+br[i][0]) < width else width), (ty+br[i][1] if (ty+br[i][1] < height) else height)))
        print("tl_translated", tl_translated)
        print("br_translated", br_translated)
        #cv2.rectangle(translated_image, tl_translated[i], br_translated[i], (255, 0, 0), 1)

    write_xml(image_src, image, obj, tl_translated, br_translated, xml_path, 3)
    cv2.imwrite(image_src + "/" + "t" + image.name, translated_image)


if __name__ == '__main__':



    for n, image_file in enumerate(scandir.scandir(image_folder)):
        image_path = str(image_file.path)

        print(image_file.name)
        if image_file.name[-4:] != '.jpg':
            print("ikke en jpg bilde!")
            continue

        #Check for original pictures
        if image_file.name[0] == "m" or image_file.name[0] == "s" or image_file.name[0] == "t":
            continue

        #Check if xml for the image is already made
        xml_str = savedir + '/' + image_file.name
        xml_str = xml_str[:-4]
        xml_str = xml_str + ".xml"
        #print(xml_str)
        if os.path.isfile(xml_str):
            continue

        fig, ax = plt.subplots(1, figsize=(15,9))

        mngr = plt.get_current_fig_manager()
        image = cv2.imread(image_file.path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        ax.imshow(image)
        img = image_file

        print("Currently chosen class: %s" % classes[objType])

        toggle_selector.RS = RectangleSelector(
            ax, line_selec_callback,
            drawtype='box', useblit=False,
            button =[1], minspanx=5, minspany=5,
            spancoords='pixels', interactive=True
        )

        if not running:
            print("hei")
            break

        bbox = plt.connect('key_press_event', toggle_selector)
        key = plt.connect('key_press_event', onkeypress)
        plt.show()
