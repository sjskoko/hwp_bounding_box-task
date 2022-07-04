import streamlit as st
import os
import pandas as pd
import numpy as np
import img2pdf
import pdfplumber
from PIL import Image
from util import *
from caption_extraction import *

st.title('PDF Object Extractor')


#########

uploaded_file = st.file_uploader('Drop the pdf', type='pdf')

# display document


if uploaded_file is not None and st.button('process pdf'):

    with open(os.path.join('pdf_file', uploaded_file.name), 'wb') as f:
        f.write(uploaded_file.getbuffer())
    f.close()

    uploaded_file_name = uploaded_file.name
    # with pdfplumber.open(uploaded_file_name) as pdf:
    #     pages = pdf.pages
    pdf = pdfplumber.open(os.path.join('pdf_file', uploaded_file_name))
    pages = pdf.pages

    # 저장용 pdf 별 object dictionary 생성
    text_dict = {}
    image_dict = {}
    table_dict = {}
    
    # 이미지 모음
    img_list = []

    # 각 page 루프
    for i, page in tqdm(enumerate(pages)):

        # text, image 객체 추출
        text = get_text(page)
        image = get_image(page)
        # tableobject 객체 딕셔너리로 변환
        table_obj = get_table(page)
        table = []
        for tboj in table_obj:
            table.append(table_object_to_dict(tboj))

        # page 별로 저장
        text_dict[i] = text
        image_dict[i] = image
        table_dict[i] = table
        # st.header('This is table summary')
        # st.caption(table)

        
        im = page.to_image(resolution=400)

        if table:
            table_bbox_list = [i.bbox for i in table_obj]
            print(i, 'page Table', table_bbox_list)
            for bbox in bbox_padding(table_bbox_list):
                im.draw_rect(bbox, stroke='red')



        if image:
            page_height = page.height

            img_bbox_list = [(image['x0'], page_height - image['y1'], image['x1'], page_height - image['y0']) for image in image]
            print(i, 'page Image', img_bbox_list)
            for bbox in bbox_padding(img_bbox_list):
                im.draw_rect(bbox, stroke='blue')
        
        img_list.append(im)

    if not os.path.exists(os.path.join('img_file', uploaded_file_name)):
        os.makedirs(os.path.join('img_file', uploaded_file_name))

    my_bar = st.progress(0)
    for i, im in enumerate(img_list):
        im.save(os.path.join('img_file', uploaded_file_name, f'{uploaded_file_name}_{i}.png'), format='PNG')
        my_bar.progress(i+1)




# 아래 실행 안됨
# image 저장 후 다시 끌어와서 변환하도록 변경
    # converted_img_list = [i.convert('RGB') for i in img_list[1:]]
    # img_main = img_list[0].convert('RGB')
    # img_main.save(os.path.join('img_file', uploaded_file_name), save_all=True, append_images=converted_img_list)

    img_file_paths = get_file_paths(folder_path=f'img_file/{uploaded_file_name}')
    converted_imgs = []
    for path in img_file_paths:
        img = Image.open(path)
        img_rgb = img.convert('RGB')
        converted_imgs.append(img_rgb)
    
    img_main = converted_imgs.pop(0)
    img_main.save(os.path.join('output_pdf_file', '(captioned)'+uploaded_file_name), save_all=True, append_images=converted_imgs)


    output_pdf = pdfplumber.open(os.path.join('output_pdf_file', '(captioned)'+uploaded_file_name))

    # options = st.multiselect(
    #     'Choose Object',
    #     ['Table', 'Image'],
    #     ['Table'])

    # if 'Table' in options:
    #     pass
    with open(os.path.join('output_pdf_file', '(captioned)'+uploaded_file_name), 'rb') as output_pdf:
        st.download_button(label="Export_Report",
                            data=output_pdf,
                            file_name=f'processed_{uploaded_file_name}')

    # streamlit run sample_code.py