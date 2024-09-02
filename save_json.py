import json 

def save_json(angle, coords, labels, arc_angle_measure, error_note):
    angle_data = {}

        # define angle types
    if angle >= 0 and angle <=90:
        angle_type = 'Acute'
    elif angle >=90 and angle <=180:
        angle_type = 'Obtuse'
    else: 
        angle_type = 'Reflex'
    
    if labels == '':
        angle_data['angle_labels'] ='labels not detected' 
    else: 
        my_dict = {}
        for i in range(len(coords)):
          if i>3:
             break
          my_dict[labels[i-1]] = coords[i-1]
        angle_data['angle_labels'] = my_dict

    angle_data['angle_measurement'] = round(angle, 1)
    angle_data['Vertex_label'] =  'vertex not detected' if labels == '' else { labels[1]: coords[1]} 
    angle_data['angle_type'] = angle_type

    ""
    #the reason labels of the second index is the location of the arc is that the labels are sorted in increasing x-coordinate
    # and two lines can only make arc angle at the middle where the second lable found
    ""
    angle_data['angle_identified_with_arc'] = 'True' if labels != "" and  labels[1] == 'N' else  'False'  
    angle_data['arc_angle_measurement'] = round(arc_angle_measure, 1)
    angle_data['confidence'] = 100
    angle_data['error_notes'] = error_note

    return angle_data

# save the details in json format

      