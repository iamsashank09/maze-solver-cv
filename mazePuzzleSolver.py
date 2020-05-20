import streamlit as st
import os
import cv2
import numpy as np
import time
from PIL import Image

def solve(ImgCV, kSize = 21):
    sleepTime = 0.5

    img = ImgCV.copy()

    # meankSize, minkSize, modekSize = findKernel(img)
    # print(meankSize, minkSize, modekSize)
    # kSize = 21

    ret, binaryImage = cv2.threshold(img, 10, 255, cv2.THRESH_BINARY_INV)
    imageLocation.image(binaryImage, use_column_width=True, caption="Binary Image")
    time.sleep(sleepTime)

    print(" While binary ",binaryImage.dtype)

    contours, hierarchy = cv2.findContours(binaryImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    path = np.zeros(binaryImage.shape, np.uint8)

    cv2.drawContours(path, contours, 0, (255,255,255), cv2.FILLED)

    imageLocation.image(path, use_column_width=True, caption='After contour')

    time.sleep(sleepTime)

    kernel = np.ones((kSize,kSize),np.uint8)
    dilated = cv2.dilate(path,kernel,iterations = 1)
    imageLocation.image(dilated, use_column_width=True, caption="Dilated")

    time.sleep(sleepTime)

    kernel = np.ones((int(kSize/2),int(kSize/2)),np.uint8)
    erosion = cv2.erode(dilated,kernel,iterations = 1)

    imageLocation.image(erosion, use_column_width=True, caption="Eroded")

    time.sleep(sleepTime)

    diff = cv2.absdiff(erosion, dilated)

    img = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)

    img[diff==255] = (0,255,0)

    imageLocation.image(img, use_column_width=True, caption="Solved Puzzle")


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

uploadOwn = False
    
imageDict = {}
for i in os.listdir(folder):
    imageDict[str(i[:-4])] = "".join((folder, i))

st.markdown("<h1 style='text-align: center; color: black;'>Maze Puzzle Solver</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: black;'>Solving Maze Puzzles using Morphological Operations - Computer Vision.</p>", unsafe_allow_html=True)

uploadType = st.radio("Type of Maze: ", [ "Try out available mazes", "Upload Custom Maze to Solve"])

if uploadType == "Upload Custom Maze to Solve" : 
    uploadOwn = True 
else: 
    uploadOwn = False 

if not uploadOwn:
    st.markdown("<h3 style='text-align: center; color: black;'>Select a maze from the dropdown and click on solve:</h3>", unsafe_allow_html=True)
    key = st.selectbox("Picture choices", list(imageDict.keys()), 0)
    filenameDropDown = imageDict[key]
    ImgCV = cv2.imread(filenameDropDown, 0)
    fileName = filenameDropDown

if uploadOwn:
    st.markdown(
        '<a href="http://mazegenerator.net/Default.aspx">'
        '<p>Generate and Download custom mazes from MazeGenerator.net [RECTANGULAR MAZES ONLY]</p>'
        '</a>', 
    unsafe_allow_html=True)
    filenameUpload = st.file_uploader("Choose an image...", type="png")
    if filenameUpload is not None:
        ImgPIL = Image.open(filenameUpload)
        ImgCV = cv2.cvtColor(np.uint8(np.array(ImgPIL)), cv2.COLOR_BGR2GRAY)
        fileName = filenameUpload
    else:
        ImgCV = None

btn = st.button("Solve the maze!")

# kSize = st.sidebar.slider(label = "Kernel Size", value = 21)
imageLocation = st.empty()

if ImgCV is not None:
    imageLocation.image(ImgCV, use_column_width=True, caption="Original Maze")

if btn:
    if ImgCV is not None:
        solve(ImgCV)


insert_github_logo()