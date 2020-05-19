import streamlit as st
import os
import cv2
import numpy as np
import time

def solve(fileImage, kSize = 21):
    sleepTime = 1
    orgimg = cv2.imread(fileImage, 0)
    img = orgimg.copy()

    # meankSize, minkSize, modekSize = findKernel(img)
    # print(meankSize, minkSize, modekSize)
    # kSize = 21

    ret, binaryImage = cv2.threshold(img, 10, 255, cv2.THRESH_BINARY_INV)
    imageLocation.image(binaryImage, caption="Binary Image")
    time.sleep(sleepTime)
    contours, hierarchy = cv2.findContours(binaryImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    path = np.zeros(binaryImage.shape, np.uint8)

    cv2.drawContours(path, contours, 0, (255,255,255), cv2.FILLED)

    imageLocation.image(path, caption='After contour')

    time.sleep(sleepTime)

    kernel = np.ones((kSize,kSize),np.uint8)
    dilated = cv2.dilate(path,kernel,iterations = 1)
    imageLocation.image(dilated, caption="Dilated")

    time.sleep(sleepTime)

    kernel = np.ones((int(kSize/2),int(kSize/2)),np.uint8)
    erosion = cv2.erode(dilated,kernel,iterations = 1)

    imageLocation.image(erosion, caption="Eroded")

    time.sleep(sleepTime)

    diff = cv2.absdiff(erosion, dilated)

    # displayImg([diff],['Difference'])

    img = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)

    img[diff==255] = (0,255,0)

    imageLocation.image(img, caption="Solved Puzzle")


folder = 'mazes/'

imageDict = {}
for i in os.listdir(folder):
    imageDict[str(i[:-4])] = "".join((folder, i))

'''
# Maze Puzzle Solver
Solving Maze Puzzle's using Morphological Operations - Computer Vision.
### Select a maze from the dropdown and click on solve:

'''

key = st.selectbox("Picture choices", list(imageDict.keys()), 0)

btn = st.button("Solve the maze!")

# kSize = st.sidebar.slider(label = "Kernel Size", value = 21)
imageLocation = st.empty()
imageLocation.image(imageDict[key], caption="Original Maze")

if btn:
    solve(imageDict[key])

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)


# st.image(imageDict[key], use_column_width=True, caption=imageDict[key])
# imageLocation.image(imageDict[key], use_column_width=True, caption=imageDict[key])