import re 
import numpy as np 
import math
import cv2

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

def measure_distance(pt1, pt2):
    return ((pt1[0] - pt2[0])**2+(pt1[1] - pt2[1])**2)**0.5

def remove_items(test_list, item):
    return list(filter((item).__ne__, test_list))

def unique(string):
   unique_ = ""

   for character in string:
     if character not in unique_:
        unique_ += character.upper()
   #print(unique_)
   return unique_.upper()

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

def label_moderator(angle_label):
   if len(angle_label)==0:
      return ''
   str1 = "ONM"
   edits = ''
   reversed = str1[::-1]

   result1 = re.sub(re.escape(angle_label), "", str1)
   result2 = re.sub(re.escape(angle_label), "", reversed)
   
   if len(result1) > len(result2):
     edits = result2
   else: 
     edits = result1
   angle_label = angle_label + edits
   angle_label = unique(angle_label)
   
   
   listb = list(angle_label)
   if listb[1] != 'N':
      listb = remove_items(angle_label, "N")
      listb.insert(1, 'N')
      angle_label = ''.join(listb)

   return angle_label


def display_images_in_grid(images, rows, cols, window_name='Image Grid'):
    # Check if the number of images matches the grid dimensions
    assert len(images) == rows * cols, "Number of images must match rows * cols"

    # Resize images to the smallest image dimensions in the list
    min_height = min(image.shape[0] for image in images)
    min_width = min(image.shape[1] for image in images)
    resized_images = [cv2.resize(image, (min_width, min_height)) for image in images]

    # Combine images into a grid
    grid_images = []
    for i in range(rows):
        row_images = resized_images[i * cols:(i + 1) * cols]
        grid_images.append(np.hstack(row_images))

    # Combine rows to form the full grid
    grid = np.vstack(grid_images)

    return grid

def arc_angle_measurement(cropped_arc):
   angle = 0
   contours, _ = cv2.findContours(cropped_arc, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
   for contour in contours:
    # Fit a minimum enclosing circle to the contour
      if len(contour) >= 10:  # Ensure there are enough points to fit an ellipse or circle
        ellipse = cv2.fitEllipse(contour)
        (center, axes, angle) = ellipse

   return angle
   

   