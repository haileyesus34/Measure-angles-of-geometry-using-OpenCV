import numpy as np 
import cv2 

alpha = 1.8  # Contrast control (1.0-3.0)
beta = 0.1


def image_preprocess(img):
    blank_img = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)
    contrasted = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

    hsv = cv2.cvtColor(contrasted, cv2.COLOR_BGR2HSV) 

    #img = cv2.erode(hsv, kernel=None, iterations=1)
   # Threshold of blue in HSV space 
    lower_blue = np.array([116, 0, 0]) 
    upper_blue = np.array([150, 255, 255]) 
  
   # preparing the mask to overlay 
    mask = cv2.inRange(hsv, lower_blue, upper_blue) 
      
   # The black region in the mask has the value of 0, 
   # so when multiplied with original image removes all non-blue regions 
    result = cv2.bitwise_and(img, img, mask = mask)
    
    edges = cv2.Canny(result,0, 50)
    dilate = cv2.dilate(edges, kernel=None, iterations=2)
    erode = cv2.erode(dilate, kernel=None, iterations=2)

  # Find contours
    H, W = erode.shape[:2]

   # Find contours
    contours, hierarchy = cv2.findContours(erode.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    boxes = []
  
    for contour in contours:
      x, y, w, h = cv2.boundingRect(contour)
      boxes.append((x,y,w,h))
          
    for box in boxes:
        x, y, w, h = box

        if (w > 10 and w < 25) and (h > 10 and h<30):
          xmin = x
          xmax = x+w-15
          ymin = y
          ymax = y+h-15
          cv2.rectangle(erode.copy(), (xmin, ymin), (xmax, ymax), (0, 0, 0), -1)   

    lines = cv2.HoughLinesP(erode, rho=1, theta=np.pi/180, threshold=50, minLineLength=90, maxLineGap=40)

    if lines is not None:
      for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(blank_img, (x1, y1), (x2, y2), 255, 2)
    
    binary_image = cv2.erode(blank_img, kernel=(5,5), iterations=1)
    
    return erode, binary_image
