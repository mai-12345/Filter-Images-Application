

import cv2
import numpy as np
import streamlit as st
from PIL import Image

st.title("Image Filters Application")

uploaded_image=st.file_uploader('choase an image ',type=['png','jpg','jpeg','webp'])

def black_white(img):
    gray_image=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    return gray_image

def blur_image(img,ksize=5):
    blur=cv2.GaussianBlur(img,(ksize,ksize),0,0)
    sketch,_=cv2.pencilsketch(blur)
    return sketch

def vintage(img,level):
    height,width=img.shape[:2]
    x_kernel=cv2.getGaussianKernel(width,width/level)
    y_kernel=cv2.getGaussianKernel(height,height/level)
    kernel=y_kernel*x_kernel.T
    mask=kernel/kernel.max()
    image_copy=np.copy(img)
    for i in range(3):
        image_copy[:,: ,i]=image_copy[:,: ,i]*mask
    return image_copy


def HDR(img,level,sigma_s=10,sigma_r=0.1):
    bright=cv2.convertScaleAbs(img,beta=level)
    hd_image=cv2.detailEnhance(bright,sigma_s=sigma_s,sigma_r=sigma_r)
    return hd_image

def style_image(img,sigma_s=10,sigma_r=0.1):
    blur=cv2.GaussianBlur(img,(5,5),0,0)
    style=cv2.stylization(blur,sigma_s=sigma_s,sigma_r=sigma_r)
    return style

def brightness(img,level):
    bright=cv2.convertScaleAbs(img,beta=level)
    return bright


if uploaded_image is not None:
    img=Image.open(uploaded_image)
    img=np.array(img)
    img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    
    orginal_image,output_image=st.columns(2)
    
    with orginal_image:
        st.header("Orignal")
        st.image(img,channels='BGR',use_column_width=True)
        st.header('Filters List')

    options=st.selectbox('select Filters : ',('None','Gray Image','HDR','Style Image','Brightness Image','Vintage'))
    
    output_flag=1
    color='BGR'

    if options=='None':
        output_flag=0
        output=img

    elif options=='Gray Image':
        output=black_white(img)

    

    elif options=='HDR':
        level=st.slider('Brightness',-50,50,10,step=5)
        output=HDR(img,level)

    
    elif options=='Style Image':
        sigma_s=st.slider('sigma_s',0,200,40,step=10)
        # sigma_r=st.slider('sigma_r',0,1,4)
        output=style_image(img,sigma_s)

    elif options=='Brightness Image':
        level=st.slider('Brightness',-50,50,10,step=5)
        output=brightness(img,level)

    elif options=='Vintage':
        level=st.slider('level ',0,5,1,step=1)
        output=vintage(img,level)
    with output_image:
        st.header("output image")
        if color=='BGR':
            output=cv2.cvtColor(output,cv2.COLOR_BGR2RGB)
            st.image(output,use_column_width=True)

        
