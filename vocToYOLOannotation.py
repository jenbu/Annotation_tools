import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
import scandir


classes = ["box-end", "pin-end"]
folder_labels = "labels17_04/"
train_txt_name = "train17_04.txt"
xml_path = "xml_filer03.04.19"

def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(year, image_id):
    in_file = open('/s.xml')
    out_file = open('labels/yolo_annotation.txt', 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write("abc")#str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

train_file = open(train_txt_name, "a")

for n, xml_file in enumerate(scandir.scandir(xml_path)):
    print(xml_file.name)
    in_file = open(xml_file.path)
    xml_name = xml_file.name
    xml_name = xml_name[:-4]

    out_file = open(folder_labels + xml_name + ".txt", 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    picture_name = root.find('filename')
    train_file.write("data/obj/" + picture_name.text + '\n')

    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text

        if cls not in classes or int(difficult) == 1:
            print("could not find class")
            continue

        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

train_file.close()




