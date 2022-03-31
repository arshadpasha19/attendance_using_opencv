import cv2
import face_recognition
import os
import numpy as np
from datetime import datetime
from twilio.rest import Client

path='images'
images=[]
names=[]
mylist= os.listdir(path)
print(mylist)
for cur_img in mylist:
    current_img=cv2.imread(f"{path}/{cur_img}")
    images.append(current_img)
    names.append(os.path.splitext(cur_img)[0])
print(names)

def faceEncodings(images):
    encodeList=[]
    for img in images:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode=face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList
encodeList= faceEncodings(images)
print("done with encoding :)")

def attendance(name):
    with open("attendance.csv","r+") as f:
        myDataList= f.readlines()
        nameList=[]
        for line in myDataList:
            entry=line.split(",")
            nameList.append(entry[0])
        if name not in nameList:
            time_now=datetime.now()
            time=time_now.strftime("%H:%M:%S")
            date=time_now.strftime("%d/%m/%Y")
            f.write(f"\n{name},{time},{date}\n")
            if name=="ARSHAD":
                account_sid = "ACe3925bfa0e3512619e156c88656e0579"
                auct_token = "245824d0bcee32a6fd771a694a57678b"
                twilio_number = "+12176802877"
                if name == 'ARSHAD':
                    number = "+919731278124"


                client=Client(account_sid,auct_token)
                message=client.messages.create(
                    body=f"{name} you have been marked present at {time} on {date}.Thank you:)",
                    from_=twilio_number,
                    to=number
                )
                print(message.body)


cap=cv2.VideoCapture(0)

while True:
    retu, frame=cap.read()
    faces=frame
    #faces=cv2.resize(frame,(0,0),None,0.25,0,25)
    faces=cv2.cvtColor(faces,cv2.COLOR_BGR2RGB)
    faceFrame=face_recognition.face_locations(faces)
    encodeFrame=face_recognition.face_encodings(faces,faceFrame)

    for encodeFace,faceLoc in zip(encodeFrame,faceFrame):
        matches=face_recognition.compare_faces(encodeList,encodeFace)
        faceDis=face_recognition.face_distance(encodeFace,encodeList)
        matchIndex=np.argmin(faceDis)
        if matches[matchIndex]:
            name= names[matchIndex].upper()
            y1,x2,y2,x1=faceLoc
            #y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
            #cv2.rectangle(frame,(x1,y2+25),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(frame,name,(x1+6,y1-6),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,255),1)
            attendance(name)
    cv2.imshow("camera",frame)
    if cv2.waitKey(1)& 0xFF ==ord('q'):
        break







