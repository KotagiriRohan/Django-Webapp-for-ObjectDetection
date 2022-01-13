import cv2
import numpy as np
import os

def ObjectDetectionModel(imgurl):
    # loading the model
    model = cv2.dnn.readNetFromTensorflow(
        "D:/Django/ObjectDetection/assets/dnn/frozen_inference_graph_coco.pb", "D:/Django/ObjectDetection/assets/dnn/mask_rcnn_inception_v2_coco_2018_01_28.pbtxt")
    # getting all the lable names
    classesFile = "D:/Django/ObjectDetection/assets/coco.names"
    classNames = open(classesFile).read().strip().split('\n')
    # print(classNames)

    # getting input image
    img = cv2.imread(
        imgurl)
    height, width, _ = img.shape
    # blank image
    blank_mask = np.zeros((height, width, 3), np.uint8)
    blank_mask[:] = (0, 0, 0)
    # subtractiong the mean and switching RB values
    preprocess = cv2.dnn.blobFromImage(img, swapRB=True)
    # input the image for detectiong
    model.setInput(preprocess)
    # the bounding box and the mask after the detection process
    boxes, masks = model.forward(["detection_out_final", "detection_masks"])

    #print(boxes.shape, masks.shape)
    # max no of detection
    count = boxes.shape[2]
    # for each detection in the image
    for i in range(count):
        # getting the bounding box of the detection, corrosponding class and its detection score
        box = boxes[0, 0, i]
        classid = int(box[1])
        score = box[2]
        # exclude all the classes less than 80% confidence
        if score < 0.75:
            continue
        # lable name to its corrosponding class number
        classname = (classNames[classid])

        # getting the coordinates of the bounding box
        x = int(box[3]*width)
        y = int(box[4]*height)
        x2 = int(box[5]*width)
        y2 = int(box[6]*height)

        # getting the mask of the object
        roi = blank_mask[y: y2, x: x2]
        roi_height, roi_width, _ = roi.shape

        # resize and threshold the mask
        mask = masks[i, classid]
        mask = cv2.resize(mask, (roi_width, roi_height))
        _, mask = cv2.threshold(mask, 0.5, 255, cv2.THRESH_BINARY)

        # finding the counters and filling then with some random color values
        contours, _ = cv2.findContours(
            np.array(mask, np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        color = np.random.randint(0, 255, 3, dtype='uint8')
        color = [int(c) for c in color]

        for cnt in contours:
            cv2.fillPoly(roi, [cnt], (int(color[0]), int(color[1]), int(color[2])))

        # drawing the bounding rectangle and display the object name
        cv2.rectangle(img, (x, y), (x2, y2), color, 2)
        cv2.putText(img, classname, (x, y-5),
                    cv2.FONT_HERSHEY_SIMPLEX, .5, (255, 255, 255), 1)

    # Display the final result
    mask_img = cv2.addWeighted(img, 1, blank_mask, 0.8, 0)
    #cv2.imshow("Black image", blank_mask)
    #cv2.imshow("Mask image", img)
    #cv2.imshow("Final Image", mask_img)
    os.chdir('D:/Django/ObjectDetection/media/processedimg')
    cv2.imwrite('Mask.jpg', blank_mask)
    cv2.imwrite('Detect.jpg', img)
    cv2.imwrite('Final.jpg',mask_img)
