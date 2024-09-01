import cv2
import pytesseract
from utils import moderator_text, label_moderator



def ocr_labels(image, angle):

   labels = ''
   letter = ''
   angle_label = ''

   # Convert to grayscale
   gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

   thresh = cv2.threshold(gray, 0, 255,
	 cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

   # apply a distance transform which calculates the distance to the
   # closest zero pixel for each pixel in the input image
   dist = cv2.distanceTransform(thresh, cv2.DIST_L2, 5)
   # normalize the distance transform such that the distances lie in
   # the range [0, 1] and then convert the distance transform back to
   # an unsigned 8-bit integer in the range [0, 255]
   dist = cv2.normalize(dist, dist, 0, 1.0, cv2.NORM_MINMAX)
   dist = (dist * 255).astype("uint8")

   # threshold the distance transform using Otsu's method
   dist = cv2.threshold(dist, 0, 255,
	cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
   # clean the image using morphological operations
   kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
   thresh = cv2.morphologyEx(dist, cv2.MORPH_OPEN, kernel)
   thresh = cv2.dilate(thresh, kernel=(4,4), iterations=3)
 
   H, W = image.shape[:2]

   # Find contours
   contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
   boxes = []
   coords = []
   # store the bounding coordinates of each contour
   for contour in contours:
     x, y, w, h = cv2.boundingRect(contour)
     boxes.append((x,y,w,h))
          
   for box in boxes:
        x, y, w, h = box
        # Filter out small contours
        # Extract the ROI (Region of Interest)
        if (w > 10 and w < 50) and (h > 10 and h<50):
          xmin = max(0, x-10)
          xmax = min(W, x+w+10)
          ymin = max(0, y-10)
          ymax = min(H, y+h+10)

          roi = thresh[ymin:ymax, xmin:xmax]
          # use tesseract to detect the angle labels as a single character with a whitelist 'MNOmno'
          letter = pytesseract.image_to_string(roi, config='--psm 10 -c tessedit_char_whitelist=MNOmno')
          # if the letter is not none store the coordinates of that letter in a varialble
          if letter:
            coords.append(box)  
            letter = letter.strip()
            letter = moderator_text(letter)
          
                        
          # Draw bounding box and letter on the image
          cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
          cv2.putText(image, letter, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)
          labels = angle_label + letter
          
   labels = label_moderator(labels)
   cv2.putText(image, f'<{labels:}: {int(angle)} degrees', (80, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6*(W/H)/2, (0, 0, 0), 1)

   return image, labels, coords