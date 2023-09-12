import boto3
from PIL import Image
import matplotlib.pyplot as plt
import cv2
import numpy as np

from io import BytesIO
import tempfile

# Create a temporary directory and use it for temporary files
temp_dir = tempfile.mkdtemp()
from ultralytics import YOLO

# AWS S3 bucket and access details
bucket_name = ''
aws_access_key_id = ''
aws_secret_access_key = ''
#aws_session_token = 'your-session-token'  # Optional, if using temporary credentials

# Initialize the S3 client
s3 = boto3.resource('s3',
                  aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key,
                  #aws_session_token=aws_session_token  # Include this line if using session token
                  )
bucket=s3.Bucket('')



def read_s3_image(file_name):
    obj = bucket.Object(file_name)
    response = obj.get()
    file_stream = response['Body']
    img = np.asarray(bytearray(file_stream.read()), dtype=np.uint8)
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    return img
img = read_s3_image('googleimage/hybrid_132_address.png')

def detect(model_pt, image_pt):
    # Load a pretrained YOLOv8n model
    model = YOLO(model_pt)

    #what ever the requirement we want can mention here  save_txt = True....etc
    results = model(image_pt, save=True, save_txt=True) 

    return results
detect("best.pt",img)