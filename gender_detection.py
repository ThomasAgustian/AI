import cv2
import serial
import numpy as np


def faceBox(face_model,frame):
    frameHeight=frame.shape[0]
    frameWidth=frame.shape[1]
    blob=cv2.dnn.blobFromImage(frame, 1.0, (300,300), [104,117,123], swapRB=False)
    face_model.setInput(blob)
    detection=face_model.forward()
    bboxs=[]
    for i in range(detection.shape[2]):
        confidence=detection[0,0,i,2]
        if confidence>0.7:
            x1=int(detection[0,0,i,3]*frameWidth)
            y1=int(detection[0,0,i,4]*frameHeight)
            x2=int(detection[0,0,i,5]*frameWidth)
            y2=int(detection[0,0,i,6]*frameHeight)
            bboxs.append([x1,y1,x2,y2])
            cv2.rectangle(frame, (x1,y1),(x2,y2),(0,255,0), 1)
    return frame, bboxs


faceProto = "C:/Users/Acer/OneDrive/Documents/kuliah/semester 5/AI/Gender_Detector/opencv_face_detector.pbtxt"
faceModel = "C:/Users/Acer/OneDrive/Documents/kuliah/semester 5/AI/Gender_Detector/opencv_face_detector_uint8.pb"

genderProto = "C:/Users/Acer/OneDrive/Documents/kuliah/semester 5/AI/Gender_Detector/gender_deploy.prototxt"
genderModel = "C:/Users/Acer/OneDrive/Documents/kuliah/semester 5/AI/Gender_Detector/gender_net.caffemodel"

ageProto = "C:/Users/Acer/OneDrive/Documents/kuliah/semester 5/AI/Gender_Detector/age_deploy.prototxt"
ageModel = "C:/Users/Acer/OneDrive/Documents/kuliah/semester 5/AI/Gender_Detector/age_net.caffemodel"


face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
gender_model = cv2.dnn.readNet(genderProto, genderModel)
face_model = cv2.dnn.readNet(faceProto, faceModel)
age_model= cv2.dnn.readNet(ageProto, ageModel)

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
genderList = ['Male', 'Female']

ser = serial.Serial('COM7', 9600) # Sesuaikan dengan port yang digunakan pada komputer Anda

video = cv2.VideoCapture(0)

padding=20

while True:
    ret,frame=video.read()
    frame,bboxs=faceBox(face_model,frame)
    for bbox in bboxs:
        face=frame[bbox[1]:bbox[3], bbox[0]:bbox[2]]
        face = frame[max(0,bbox[1]-padding):min(bbox[3]+padding,frame.shape[0]-1),max(0,bbox[0]-padding):min(bbox[2]+padding, frame.shape[1]-1)]
        blob=cv2.dnn.blobFromImage(face, 1.0, (227,227), MODEL_MEAN_VALUES, swapRB=False)
        gender_model.setInput(blob)
        genderPred=gender_model.forward()
        gender=genderList[genderPred[0].argmax()]

        age_model.setInput(blob)
        agePred=age_model.forward()
        age=ageList[agePred[0].argmax()]

        label="{},{}".format(gender,age)
        cv2.rectangle(frame,(bbox[0], bbox[1]-30), (bbox[2], bbox[1]), (0,255,0),-1) 
        cv2.putText(frame, label, (bbox[0], bbox[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2,cv2.LINE_AA)
        
        if gender == 'Male':
            ser.write(b'M')
        else:
            ser.write(b'F')
        cv2.imshow('Real-Time Gender Detection', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()