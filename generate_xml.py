import os
import cv2
from lxml import etree
import xml.etree.cElementTree as ET

classes = {
    0: "box-end",
    1: "pin-end",
    2: "pipe_connection"
}

def write_xml(folder, img, objects, tl, br, savedir, modified):
    if not os.path.isdir(savedir):
        os.mkdir(savedir)

    obj_list = []
    for n in objects:
        obj_list.append(classes[n])
    image = cv2.imread(img.path)
    height, width, depth = image.shape

    if modified == 0:
        image_name = img.name
    elif modified == 1:
        image_name = "m" + img.name
    elif modified == 2:
        image_name = "s" + img.name
    elif modified == 3:
        image_name = "t" + img.name

    annotation = ET.Element('annotation')
    ET.SubElement(annotation, 'folder').text = folder
    ET.SubElement(annotation, 'filename').text = image_name
    ET.SubElement(annotation, 'segmented').text = '0'
    size = ET.SubElement(annotation, 'size')
    ET.SubElement(size, 'width').text = str(width)
    ET.SubElement(size, 'height').text = str(height)
    ET.SubElement(size, 'depth').text = str(depth)

    for obj, topl, botr in zip(obj_list, tl, br):
        ob = ET.SubElement(annotation, 'object')
        ET.SubElement(ob, 'name').text = obj
        ET.SubElement(ob, 'pose').text = 'Unspecified'
        ET.SubElement(ob, 'truncated').text = '0'
        ET.SubElement(ob, 'difficult').text = '0'
        bbox = ET.SubElement(ob, 'bndbox')
        ET.SubElement(bbox, 'xmin').text = str(topl[0])
        ET.SubElement(bbox, 'ymin').text = str(topl[1])
        ET.SubElement(bbox, 'xmax').text = str(botr[0])
        ET.SubElement(bbox, 'ymax').text = str(botr[1])

    xml_str = ET.tostring(annotation)
    root = etree.fromstring(xml_str)
    xml_str = etree.tostring(root, pretty_print=True)
    save_path = os.path.join(savedir, image_name.replace('jpg', 'xml'))
    with open(save_path, 'wb') as temp_xml:
        temp_xml.write(xml_str)

    return xml_str


if __name__ == "__main__":
    folder = 'images'
    img = [im for im in os.scandir('images') if '000001' in im.name][0]
    objects = 2




