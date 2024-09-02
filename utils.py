import re 
import numpy as np 
import math
import cv2

# calcualte the angle between two lines
def calculate_angle(point1, point2, point3):
    """
    Calculate the angle between the line from point1 to point2 and from point2 to point3.
    """
    vector1 = np.array(point1) - np.array(point2)
    vector2 = np.array(point3) - np.array(point2)

    dot_product = np.dot(vector1, vector2)
    magnitude1 = np.linalg.norm(vector1)
    magnitude2 = np.linalg.norm(vector2)

    angle = math.acos(dot_product / (magnitude1 * magnitude2))
    return np.degrees(angle)

# calcualtes the intersection over unit 
def iou(boxA, boxB):
    # Determine the (x, y)-coordinates of the intersection rectangle
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    # Compute the area of intersection rectangle
    interArea = max(0, xB - xA) * max(0, yB - yA)

    # Compute the area of both the prediction and ground-truth rectangles
    boxAArea = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
    boxBArea = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])

    # Compute the intersection over union by taking the intersection area
    # and dividing it by the sum of prediction + ground-truth areas - the intersection area
    iou = interArea / float(boxAArea + boxBArea - interArea)

    # Return the intersection over union value
    return iou

# measure the distance between two points
def measure_distance(pt1, pt2):
    return ((pt1[0] - pt2[0])**2+(pt1[1] - pt2[1])**2)**0.5

# remove duplicate characters from a string
def remove_items(test_list, item):
    return list(filter((item).__ne__, test_list))

# collect unique characters 
def unique(string):
   unique_ = ""

   for character in string:
     if character not in unique_:
        unique_ += character.upper()
   #print(unique_)
   return unique_.upper()

# save unique characters from a list
def moderator_text(text):
    moderated =  ''
    for char in text: 
      if text.count(char) > 1:
         moderated = text.replace(char, '', text.count(char)-1)
      elif char.islower() and len(text)>1:
         moderated = text.replace(char, '')
      else: 
         moderated = (moderated + char)
    return moderated

# if OCR detects only two letters add the letter that is left
def label_moderator(angle_label):
   str1 = "ONM"
   edits = ''
   reversed = str1[::-1]
   
   #search for the undetected label
   result1 = re.sub(re.escape(angle_label), "", str1)
   result2 = re.sub(re.escape(angle_label), "", reversed)
   
   if len(result1) > len(result2):
     edits = result2
   else: 
     edits = result1
   
   # add the undetected label
   angle_label = angle_label + edits
   angle_label = unique(angle_label)
   
   
   listb = list(angle_label)
   if listb[1] != 'N':
      listb = remove_items(angle_label, "N")
      listb.insert(1, 'N')
      angle_label = ''.join(listb)

   return angle_label


def display_images_grid(images, grid_size=(5, 5), window_name='Image Grid'):
    # Ensure images are the same size
    resized_images = [cv2.resize(img, (200, 200)) for img in images]  # Resize all images to 200x200
    # Create the grid
    rows = []
    for i in range(0, len(resized_images), grid_size[1]):
        row = np.hstack(resized_images[i:i + grid_size[1]])
        rows.append(row)
    grid_image = np.vstack(rows)
    return grid_image

def arc_angle_measurement(cropped_arc):
   angle = 0
   contours, _ = cv2.findContours(cropped_arc, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
   for contour in contours:
    # Fit a minimum enclosing circle to the contour
      if len(contour) >= 5:  # Ensure there are enough points to fit an ellipse or circle
        ellipse = cv2.fitEllipse(contour)
        (center, axes, angle) = ellipse

   return angle
   

   