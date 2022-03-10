import pickle

import numpy as np
import tensorflow as tf


def transform_pickle_to_tf(face_binary) -> tf.Tensor:
    """ "
    Name: transform_pickle_to_tf
    Description:
        This function transforms a pickle file to a tensorflow array.
    Inputs:
        :face_binary: type(bytes) -> pickle file.
    Outputs:
        :face_tensor: type(tf.tensor) -> tensorflow array.
    """
    face_nparray = pickle.loads(face_binary)
    face_nparray = np.expand_dims(face_nparray, axis=0)

    if len(face_nparray.shape) == 3:
        face_nparray = tf.convert_to_tensor(
            face_nparray.reshape((*face_nparray.shape, 1))
        )

    if face_nparray.shape[-1] == 1:
        face_nparray = tf.image.grayscale_to_rgb(face_nparray)

    return (
        tf.image.resize(face_nparray, [200, 200], antialias=False) / 255,
        tf.image.resize(face_nparray, [128, 128], antialias=False) / 255,
    )
