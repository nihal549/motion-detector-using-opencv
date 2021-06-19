import cv2
from datetime import datetime
import pandas

video = cv2.VideoCapture(0)
first_frame= None
status_list=[None,None]
times=[]
df = pandas.DataFrame(columns=['start','end'])
while True:
    check,frame= video.read()
    status=0
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray,(21,21),0)#blurr the image for high accuracy in calculation of difference
    if first_frame is None:
        first_frame=gray
        continue # go to start of the loop

    delta_frame= cv2.absdiff(first_frame,gray) #gets difference between intensity of pixels
    thresh_frame=cv2.threshold(delta_frame,20,255,cv2.THRESH_BINARY)[1]
    #helps to smooth the threshold image
    thresh_frame=cv2.dilate(thresh_frame,None,iterations=2)
    
    (cnts,_) = cv2.findContours(thresh_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
  
    for contour in cnts:
        if cv2.contourArea(contour)<10000:
            continue
        status=1

        (x,y,w,h)=cv2.boundingRect(contour)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
    
    status_list.append(status)

    #recording the time
    if status_list[-1]==1 and status_list[-2]==0:
       times.append(datetime.now())

    if status_list[-1]==0 and status_list[-2]==1:
       times.append(datetime.now())   
      

    cv2.imshow('recording',gray)
    cv2.imshow('delta',delta_frame)
    cv2.imshow('rec',thresh_frame)
    cv2.imshow("color",frame)
    key= cv2.waitKey(1)

    if key==ord('q'):
        if status==1:
            times.append(datetime.now())
        break

    
#print(status_list)
#print(times)
for i in range(0,len(times),2):
    df= df.append({'start':times[i],'end':times[i+1]},ignore_index=True)

df.to_csv('Times.csv')
video.release()
cv2.destroyAllWindows