import face_recognition
import cv2
import glob
import os
import datetime
from pathlib import Path
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import COMMASPACE, formatdate
# This is a super simple (but slow) example of running face recognition on live video from your webcam.
# There's a second example that's a little more complicated but runs faster.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.
def ifExists(name):
    #print(name)
    date = datetime.datetime.now().strftime("%Y%m%d")
    path = Path(str(date))
    if (path.is_file()) is False:
        return True
    #file =
    if name in open(str(date),'r').read():
        #file.close()
        return False
    return True

def sendMail():
        text = 'We have found a member who is not enrolled. Please find the attached picture'
        user_name = "i.esuriya.prad@gmail.com"
        password = r'SAFERAsur$1992'
        img_data = open('unknown.jpg','rb').read()
        msg = MIMEMultipart()
        msg['From'] = 'i.esuriya.prad@gmail.com'
        msg['To'] = COMMASPACE.join('suriya.shankar@hotmail.com')
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = 'Intruder Detected CMPE 220'
        msg.attach(MIMEText(text))
        image = MIMEImage(img_data, name = 'Unknown.jpg')
        msg.attach(image)
        s =  smtplib.SMTP('smtp.gmail.com',587)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(user_name,password)
        s.sendmail('i.esuriya.prad@gmail.com','suriya.shankar@hotmail.com',msg.as_string())
        s.quit()
# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)
image_encoding = []
face_name = []
i=0

for file_name in glob.glob('pictures/*.png'):
    image = face_recognition.load_image_file(file_name)
    base = os.path.basename(file_name)
    face_name.append(os.path.splitext(base)[0])
    image_encoding.append(face_recognition.face_encodings(image)[0])
# Load a sample picture and learn how to recognize it.
#obama_image = face_recognition.load_image_file("suriya.png")
#obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()
    #print(ret)
    # Find all the faces and face enqcodings in the frame of video
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    # Loop through each face in this frame of video
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # See if the face is a match for the known face(s)
        i = 0
        #print(len(image_encoding))
        for encoding in image_encoding:
            match = face_recognition.compare_faces([encoding], face_encoding,0.5)
            #print(face_name[i])
            name = "Unknown"
            #print(len(match))
            if match[0]:
                name = face_name[i]
                if ifExists(name):
                    date = datetime.datetime.now().strftime("%Y%m%d")
                    print(datetime.datetime.now().time())
                    file = open(str(date), "a")
                    file.write(name + " " + str(datetime.datetime.now().time()))
                    file.close()
#	    unknown_frame = frame
            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            if name != "Unknown":
                break
            i = i+1
        if name == "Unknown":
	#    file = Path('/home/deeplearning/Desktop/face_recogntion examples/frame.jpg');
	    
            cv2.imwrite('unknown.jpg',frame)
	   # cv2.imwrite('frame.jpg',frame)
            sendMail()

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()

