import streamlit as st
import os
import cv2
import numpy as np
import time

def solve(fileImage, kSize = 21):
    sleepTime = 0.5
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

    img = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)

    img[diff==255] = (0,255,0)

    imageLocation.image(img, caption="Solved Puzzle")


def insert_github_logo():
    st.markdown(
        "<br>"
        '<div style="text-align: center;">'
        '<a href="https://github.com/iamsashank09"> '
        '<img src="https://image.flaticon.com/icons/png/128/1051/1051326.png" width=64>'
        " </img>"
        "</a> "
        "<br>"
        '<h> Built by Sashank Kakaraparty </h>'
        "</div>",
        unsafe_allow_html=True,
    )

def hideMenuandFooter():
    hide_menu_footer_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_menu_footer_style, unsafe_allow_html=True)

def applyStyleCSS():
    with open("style.css") as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)


# Background HTML scripts using Markdown
hideMenuandFooter()
applyStyleCSS()

# Path to folder containing images
folder = 'mazes/'
    
imageDict = {}
for i in os.listdir(folder):
    imageDict[str(i[:-4])] = "".join((folder, i))

st.markdown("<h1 style='text-align: center; color: black;'>Maze Puzzle Solver</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: black;'>Solving Maze Puzzles using Morphological Operations - Computer Vision.</p>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: black;'>Select a maze from the dropdown and click on solve:</h3>", unsafe_allow_html=True)

key = st.selectbox("Picture choices", list(imageDict.keys()), 0)

btn = st.button("Solve the maze!")

# kSize = st.sidebar.slider(label = "Kernel Size", value = 21)
imageLocation = st.empty()
imageLocation.image(imageDict[key], caption="Original Maze")

if btn:
    solve(imageDict[key])


insert_github_logo()