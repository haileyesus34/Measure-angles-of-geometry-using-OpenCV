from imutils import paths 
from ocr_labels import ocr_labels
from image_preprocess import image_preprocess
from draw_geometery import draw_geometery
from utils import display_images_in_grid
from utils import arc_angle_measurement
import cv2 
import json 
import os

import matplotlib.pyplot as plt

# directory for the test images dataset
image_dir = '/Users/hanna m/machinelearning/deep_learning/cv/analyse_geometery/Correct'
# create a vaiable for the analyzed images to be stored
# list of each json data to be stored
# detail about the angle 

analyzed_images = []
final_data = []
angle_data = {}

# An object of list of images 
imagePaths = paths.list_images(image_dir)

for imagePath in imagePaths:
    # dictionay for the angle data detail 
    angle_data = {}
    angle_type = ''
    
    # splitting the image path to extract the filename
    filename = imagePath.split(os.path.sep)[-1]
    output_dir = '/Users/hanna m/machinelearning/deep_learning/cv/analyse_geometery/analyzed_images'
    arc_dir = '/Users/hanna m/machinelearning/deep_learning/cv/analyse_geometery/arc_images'

    # directory where to save the output images
    output_dir = os.path.join(output_dir, filename)
    arc_dir = os.path.join(arc_dir, filename)

    print(output_dir)
    
    # read and preprocess image
    img = cv2.imread(imagePath)
    eroded_image, binary_image = image_preprocess(img)
    # draw the contours and on image lines and over the arc outline
    graph_drawn_img, angle, cropped_arc_img, error_note = draw_geometery(binary_image, eroded_image, img)

    #calculate the arc measure angle
    arc_angle_measure = arc_angle_measurement(cropped_arc_img)
    
    # extract the angle labels 
    img, labels, coords = ocr_labels(graph_drawn_img, angle)
    img = cv2.resize(img, (350, 200))
    
    # 
    if labels == '': 
        label = 'No label'
    
    #store analyzed images in a list
    analyzed_images.append(img)
    
    # define angle types
    if angle >= 0 and angle <=90:
        angle_type = 'Acute'
    elif angle >=90 and angle <=180:
        angle_type = 'Obtuse'
    else: 
        angle_type = 'Reflex'
    

    angle_data['angle_measurement'] = round(angle, 1)
    angle_data['angle_labels'] = labels
    angle_data['Vertex_label'] = label if labels == '' else labels[1]
    angle_data['angle_type'] = angle_type
    angle_data['angle_identified_with_arc'] = 'True'
    angle_data['arc_angle_measurement'] = round(arc_angle_measure, 1)
    angle_data['confidence'] = 100
    angle_data['error_notes'] = error_note

    final_data.append(angle_data)

    
with open('data_list.json', 'w') as json_file:
    json.dump(final_data,  json_file, indent=4)

cv2.imwrite(output_dir, img)
if cropped_arc_img is not None or arc_dir is not None:
   cv2.imwrite(arc_dir, cropped_arc_img)

print("Data has been saved to data_list.json")

