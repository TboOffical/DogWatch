# DogWatch
Do you have a naughty dog, Dose your pet destroy your house, room or office. Well then
dog watch is the perfect solution for you. DogWatch uses Computer Vision to spot dogs before
you get a chance to. Once a dog is found, dog watch can alert you on you phone via PushBullet. 
DogWatch will also save a picture of the detection and put a entry on the DogLog so you can
see all the times a dog was detected. Have fun!

<img  width="50%" src="https://i.imgur.com/YOEoJph.png">

# How to set it up (For Advanced Users)

- Build and install the [jetson-inference](https://github.com/dusty-nv/jetson-inference) library.
- <img width="50%" src="https://i.imgur.com/wfV3S4U.png">
- Use the model downloader tool (/tools/download-models.sh/) to download the DetectNet-COCO-Dog model
- Run the following
```bash
mkdir dogwatch
cd dogwatch
git clone https://github.com/TboOffical/DogWatch.git .
```
- Then to start the app, run
```bash
sudo python3 app.py
```


