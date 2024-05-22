from tensorflow.keras.applications.inception_v3 import preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow import keras
from core import settings
from glob import glob
import pandas as pd
import numpy as np
import cv2
import os


skin_disease_model = keras.models.load_model('skincare/ai_models/EfficientNetB3-skin-disease.h5')
skin_type_model = keras.models.load_model('skincare/ai_models/skin_type_recognition.h5')
burn_model = keras.models.load_model('skincare/ai_models/skin_burn.hdf5')


def predict_skin_type(image_path):
    csv_path = os.path.join(settings.BASE_DIR, "skincare/ai_models/skin_type_class_dict.csv")
    class_df = pd.read_csv(csv_path)
    img_height = int(class_df['Height'].iloc[0])
    img_width = int(class_df['Width'].iloc[0])
    img_size = (img_width, img_height)
    scale = class_df['Scale Factor'].iloc[0]
   
    try:
        s = int(scale)
        s2 = 1
        s1 = 0
    except:
        split = scale.split('-')
        s1 = float(split[1])
        s2 = float(split[0].split('*')[1])
    
    img = cv2.imread(image_path)
    img = cv2.resize(img, img_size)
    img = img * s2 - s1
    img = np.expand_dims(img, axis=0)
    preds = skin_type_model.predict(img)
    predicted_class = np.argmax(preds, axis=1)
    class_labels = {
        0: 'Oily Skin',
        1: 'Dry Skin'
    }
    class_name = class_labels[predicted_class[0]]
    return class_name


def predict_skin_disease(image_path):
    # Read in the CSV file
    csv_path = os.path.join(settings.BASE_DIR, "skincare/ai_models/skin_diseases_class_dict.csv")
    class_df = pd.read_csv(csv_path)
    img_height = int(class_df['height'].iloc[0])
    img_width = int(class_df['width'].iloc[0])
    img_size = (img_width, img_height)
    scale = class_df['scale by'].iloc[0]
    try:
        s = int(scale)
        s2 = 1
        s1 = 0
    except:
        split = scale.split('-')
        s1 = float(split[1])
        s2 = float(split[0].split('*')[1])

    # Load and preprocess the image
    img = cv2.imread(image_path)
    img = cv2.resize(img, img_size)
    img = img * s2 - s1
    img = np.expand_dims(img, axis=0)

    # Make a prediction
    preds = skin_disease_model.predict(img)
    predicted_class = np.argmax(preds, axis=1)

    # Load the class labels
    class_labels = {0: 'Eczema',
                    1: 'Melanoma',
                    2: 'Atopic Dermatitis',
                    3: 'Basal Cell Carcinoma',
                    4: 'Melanocytic Nevi',
                    5: 'Benign Keratosis',
                    6: 'Psoriasis pictures Lichen Planus and related diseases',
                    7: 'Seborrheic Keratoses and other Benign Tumors',
                    8: 'Tinea Ringworm Candidiasis and other Fungal Infections',
                    9: 'Warts Molluscum and other Viral Infections'}

    # Return the predicted disease name
    class_name = class_labels[predicted_class[0]]
    return class_name


def predict_skin_burn(image_path):
    img = image.load_img(image_path, target_size=(224, 224))
    x = image.img_to_array(img)
    tensor = np.expand_dims(x, axis=0)
    tensor = preprocess_input(tensor)

    predictions = burn_model.predict(tensor)
    y_hat = np.argmax(predictions)
    dog_names = [item[20:-1] for item in sorted(glob("dogImages/train/*/"))]
    return dog_names[y_hat] 

