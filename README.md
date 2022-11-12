# DogWatch
Watch your dog when your not around

# How to set it up (For Advanced Users)

- Build and install the [jetson-inference](https://github.com/dusty-nv/jetson-inference) library.
- Use the model downloader tool (/tools/download-models.sh/) to download the DetectNet-COCO-Dog model
- run the following
```bash
mkdir dogwatch
cd dogwatch
git clone https://github.com/TboOffical/DogWatch.git .
```
- Then to start the app, run
```bash
sudo python3 app.py
```
