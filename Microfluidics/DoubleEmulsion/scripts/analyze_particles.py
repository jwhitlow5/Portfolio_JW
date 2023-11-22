#!/usr/bin/env python3

""" Double emulsion droplet analysis
@author: jwhitlow5
06/21/2019 """

import numpy as np
import matplotlib.pyplot as plt
import cv2
import argparse
import os 

def analyze_image(image_path):
    img = cv2.imread(image_path)
    gsPost = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gsPost1 = gsPost.copy()

    #Hough transform to extract circular elements
    htransf = cv2.Houghhtransf(gsPost, cv2.HOUGH_GRADIENT, 1, 45, param1=30,
                               param2=12, minRadius=35, maxRadius=90)

    if htransf is not None:
        numrows = len(htransf[0])
        htransf = np.round((htransf[0, :]), 2)
        intensity = []
        radius = []
        #define mask
        mask = np.full((img.shape[0], img.shape[1]), 0, dtype=np.uint8)

        for (x, y, r) in htransf:
            cv2.circle(gsPost1, (x, y), r, (255, 0, 0))
            cv2.circle(mask, (x, y), r, (255, 255, 255), -1)
            radius.append(r)
            intensity.append(cv2.mean(gsPost1, mask=mask)[0])

        return intensity, radius
    else:
        return [], []

def main():
    parser = argparse.ArgumentParser(description="Analyze droplets in images.")
    parser.add_argument("directory", help="Directory containing JPG images")
    args = parser.parse_args()
    
    image_files = [f for f in os.listdir(args.directory) if f.endswith('.jpg')]

    contrasts = []
    rr = []

    for image_file in image_files:
        image_path = os.path.join(args.directory, image_file)
        intensities, r = analyze_image(image_path)
      
        contrasts.extend(intensities)
        rr.extend(r)

    #Plot data and save
    index = np.arange(len(contrasts))
    plt.scatter(index, contrasts, color='g')
    plt.scatter(index, rr, color='r')
    plt.legend(('Pixel intensity', 'radius'), loc='best', shadow=False)
    plt.xlabel("Particle")
    plt.ylabel("Droplet Diameter")

    plt.savefig(os.path.join(args.directory, os.path.basename(image)+ '_plot.png'))

if __name__ == "__main__":
    main()