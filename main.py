from imutils import paths 
from ocr_labels import ocr_labels
from image_preprocess import image_preprocess
from draw_geometery import draw_geometery
from utils import display_images_grid
from utils import arc_angle_measurement
import cv2 
import json 
import os
import save_json

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
    #store analyzed images in a list
    analyzed_images.append(cv2.resize(img, (350, 200)))

    file = save_json.save_json(angle, coords, labels, arc_angle_measure, error_note)
    final_data.append(file)

with open('data_list.json', 'w') as json_file:
      json.dump(final_data,  json_file, indent=4)

print("Data has been saved to data_list.json")

plt.figure(figsize=(8, 10))

for i in range(12):
    plt.subplot(4,3, i+1)
    plt.axis('off')
    plt.imshow(cv2.cvtColor(analyzed_images[i], cv2.COLOR_BGR2RGB))
plt.show()

