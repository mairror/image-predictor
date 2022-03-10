from typing import List

import numpy as np
from faces_predict.transform_images import transform_pickle_to_tf
from tensorflow.keras.models import load_model
from utils.logging import image_predictor

gender_classes = ["Male", "Female"]


def make_prediction(key: str, pickle_list: List):
    """
    Name: prediction
    Description:
        Predicts the age and the gender given an
    Inputs:
        :pickle_file: type(list) -> dictionary with the s3 object key, bucket and checksum.
    Outputs:
        List(faces) -> list of faces on numpy array saved as type(bytes).
    """

    model_age = load_model("./models/model_age.h5", compile=True)
    model_gender = load_model("./models/model_gender.h5", compile=True)

    image_predictor.info(f"Making prediction on {len(pickle_list)} faces ..")
    for face_binary in pickle_list:
        document = {"key": key, "predictions": []}

        age_tensor, gender_tensor = transform_pickle_to_tf(face_binary)

        age_prediction = str(int(model_age.predict(age_tensor) * 116))

        gender_prediction = gender_classes[
            np.argmax(model_gender.predict(gender_tensor))
        ]

        document["predictions"].append(
            {"age": age_prediction, "gender": gender_prediction}
        )

    return document
