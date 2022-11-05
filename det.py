#!/usr/bin/python3

import jetson.inference
import jetson.utils

font = jetson.utils.cudaFont()

image_uri = "pug.jpg"

#network = "./resnet18.onnx"
network = "resnet-18"

img = jetson.utils.loadImage(image_uri)
net = jetson.inference.imageNet(network)

class_i, conf = net.Classify(img)
class_description = net.GetClassDesc(class_i)

print("This image is a "+ class_description + " with " + str(conf) + " Confinidance")

font.OverlayText(img, img.width, img.height, "This image is a "+ class_description + " with " + str(conf) + " Confinidance", 5, 5, font.White, font.Gray40)
output = jetson.utils.videoOutput(image_uri )
output.Render(img)