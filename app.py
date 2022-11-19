
from flask import Flask, render_template, Response, request, send_file
import jetson.inference
import requests
from datetime import date
from datetime import datetime
import cv2
from playsound import playsound
import jetson.utils
from pushbullet import API
import time as tm
import os as os
import gc
import threading
from jetson_utils import videoSource, videoOutput, logUsage, videoOutput

def app():

    load = False
    live = False
    net = jetson.inference.detectNet("coco-dog")

    app = Flask(__name__)

    class ai (threading.Thread):
        def __init__(self, threadID, name, counter):
            threading.Thread.__init__(self)
            self.threadID = threadID
            self.name = name
            self.counter = counter
        def run(self):
            while True:
                cap = cv2.VideoCapture(0) 
                if cap is None or not cap.isOpened():
                    pass
                else:
                        _, frame = cap.read()
                        cv2.imwrite("isdog.jpg", frame)
                        img = jetson.utils.loadImage("isdog.jpg")
                        start = tm.perf_counter()
                        detections = net.Detect(img, overlay="box,labels,conf")
                        end = tm.perf_counter()
                        file2 = open("stats.dwl", "w") 
                        file2.write(str(end - start))
                        file2.close()
                        print("detected {:d} objects in image".format(len(detections)))
                        for detection in detections:
                            print(detection)
                            output = videoOutput("last.jpg")
                            output.Render(img)
                            f = open("push.dwl", "r")
                            push = f.read()
                            f.close()
                            now = datetime.now()
                            if push == "true":
                                api = API()
                                fa = open("key.dwl", "r")
                                key = fa.read()
                                fa.close()
                                now = datetime.now()
                                api.set_token(key)
                                api.send_note("DogWatch", "Detected a dog at " +  now.strftime("%d/%m/%Y %H:%M"))
                            file1 = open("log.dwl", "a") 
                            file1.write('{"date" : "'+  now.strftime("%d/%m/%Y %H:%M") +'", "Message": "'+ 'Detected a Dog"}split\n')
                            file1.close()
                            tm.sleep(2)
                              
                cap.release()
                gc.collect()

    class VideoCamera(object):
        def __init__(self):
            self.video = cv2.VideoCapture(0)  
        def __del__(self):
            self.video.release()
        def save(self):
            _, image = self.video.read()
            cv2.imwrite("isdog.jpg", image)
        def get_frame(self):
            success, image = self.video.read()
            ret, jpeg = cv2.imencode('.jpg', image)
            return jpeg.tobytes()

    @app.route('/')
    def index():
        return render_template("index.html")
        
    @app.route('/clear')
    def clear():
        try:
            os.unlink("./log.dwl")
        except:
            return "err"
        return "ok"

    @app.route('/quit')
    def quit():
        exit()
        
    @app.route('/get_ntf')
    def getntf():
        f = open("push.dwl", "r")
        return f.read()

    @app.route('/get_stat')
    def get_stat():
        f = open("stats.dwl", "r")
        return f.read()

    @app.route('/honk')
    def honk():
        try:
            playsound("horn.wav")
        except:
            return "fail"
        return "ok"
    
    @app.route('/get_log')
    def getlog():
        try:
            f = open("log.dwl", "r")
            return f.read()
        except:
            return '{"date": "Server-Message", "Message": "No Log Data" }'

    @app.route('/lastpic')
    def lst():
       return send_file("last.jpg")

    @app.route("/set_ntf_true")
    def ntftrue():
        file1 = open("push.dwl", "w") 
        file1.write('true')
        file1.close()
        return ""

    @app.route("/set_key", methods=['GET'])
    def setkey():
        file1 = open("key.dwl", "w") 
        file1.write(request.args.get("key"))
        file1.close()
        return ""

    @app.route("/set_ntf_false")
    def ntffalse():
        file1 = open("push.dwl", "w") 
        file1.write('false')
        file1.close()
        return ""

    def gen(camera):
        while True:
            frame = camera.get_frame()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    @app.route('/video_feed')
    def video_feed():
        return Response(gen(VideoCamera()),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

   
    ait = ai(1, "ai-Thread", 1)
    ait.start()

    app.run(host='0.0.0.0', debug=False)

app()