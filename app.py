import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import os
from io import BytesIO
import base64


def generate_cert(user):
    font = ImageFont.truetype('LibreBaskerville-Italic.ttf',60)
    img = Image.open('cert/cert.png')
    W, H = img.size
    H = 630
    draw = ImageDraw.Draw(img)
    msg = user
    # figure out the right positioning
    w, h = draw.textsize(msg, font=font)
    draw.text(((W-w)/2,(H-h)/2), msg, fill=(235, 165, 34), font=font)
    img.save("DS3_Certificate.png")
    # st.image(img)
    # st.markdown(get_image_download_link(img, 'DS3_Certificate.png','Download your certificate'), unsafe_allow_html=True)


def clean_folder(file_extension):
	directory = os.getcwd()

	files_in_directory = os.listdir(directory)
	filtered_files = [file for file in files_in_directory if file.endswith(file_extension)]
	for file in filtered_files:
		path_to_file = os.path.join(directory, file)
		os.remove(path_to_file)

def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download your certificate</a>'
    return href

def get_image_download_link(img,filename,text):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href =  f'<a href="data:file/txt;base64,{img_str}" download="{filename}">{text}</a>'
    return href


def main():
	st.image("logo/lab.png")

	st.title('Data Science Summer School 2021 Certificate')

	st.write("""
			This app will check if you are a participant of the Data Science Summer School, organized by the Hertie School Data Science Lab, and generate a certificate with your name on it. 
			Please kindly input your name in the field below, click Enter and download the generated certificate. Thank you and have a splendid summer!

			""")
	user = st.text_input("What is your name?")
	if len(user) != 0: 
		user = user.title()
		df = pd.read_csv('all.csv')
		df["name"] = df["name"].str.title()

		check = df['name'].str.contains(user).sum()
		if check > 0: 
			generate_cert(user)
			# st.markdown(get_image_download_link(result, DS3_Certificate.png,'Download your certificate'), unsafe_allow_html=True)
			st.markdown(get_binary_file_downloader_html('DS3_Certificate.png', 'PNG'), unsafe_allow_html=True)
			st.image('DS3_Certificate.png', width=700)
			clean_folder(".png")
		else: 
			st.write("Your name does not appear to be in our participant database. Please contact us at Datasciencelab@hertie-school.org to sort out the issue. Thank you!")
	else: 
			st.write("Please input your name in the above field. Thank you!")


if __name__ == "__main__":
    main()
