import cv2 
from utils import measure_distance, calculate_angle

def draw_geometery(black_img, erode, img):

    error_note = ''

    contours, _ = cv2.findContours(erode, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv2.contourArea)

    H, W = erode.shape[:2]
           
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        # Filter out small contours
        if (w > 10 and w < 50) and (h > 10 and h<50):
            continue    
        cv2.drawContours(img, [c], -1, (0, 255, 0), 3, -1)

    contours, _ = cv2.findContours(black_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv2.contourArea)

    angle = 0
    cropped_arc = erode
    
    if contours:
        contour = contours[-1]
        points = []

        epsilon = 0.01 * cv2.arcLength(contour, False)
        approx = cv2.approxPolyDP(contour, epsilon, False)

        if len(approx) >= 3:
            for i in range(len(approx)):
                points.append(approx[i][0].tolist())
            
            for i in points: 
                for j in points:
                    d = measure_distance(i, j)
                    if d == 0:
                        continue
                    elif d < 50 and d > 0:
                        points.remove(j)

        if len(points) >=3:
            angle = calculate_angle(points[0], points[1], points[2])
            
            if angle <=90:
              x_center, y_bottom = points[0]
            else: 
              x_center, y_bottom = points[1]
              
            x1 = x_center - 40
            x2 = x_center + 40
            y1 = y_bottom - 50
            y2 = y_bottom + 5

            cropped_arc = erode[y1:y2, x1:x2]

            for point in points:
                cv2.circle(img, tuple(point), 8, (0, 0, 255), -1)
            
            #cv2.line(img, points[0], points[1],  (0, 255, 0), 4)
            #cv2.line(img, points[1], points[2], (0, 255, 0), 4)
        else:
            error_note = "Not enough vertices to calculate an angle."
    else:
        error_note = "No contours found."
    return img, angle, cropped_arc, error_note