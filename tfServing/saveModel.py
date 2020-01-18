
import tensorflow as tf
from tensorflow import keras

import numpy as np
import matplotlib.pyplot as plt
import os, subprocess, requests, tempfile

from tensorflow.keras.applications import resnet50


def tf_save(model_name, version):
	tf.saved_model.simple_save(
		keras.backend.get_session(),
		os.path.join(model_name, str(version)), # tempfile.gettempdir(),
		inputs={'input_image': model.input},
		outputs={t.name:t for t in model.outputs}
	)

	os.environ["MODEL_DIR"] = MODEL_DIR

if __name__ == "__main__":
	model = resnet50.ResNet50()
	tf_save('resnet', '1')

# import json
# data = json.dumps({"signature_name": "serving_default", "instances": test_images[0:3].tolist()})
# print('Data: {} ... {}'.format(data[:50], data[len(data)-52:]))


# headers = {"content-type": "application/json"}
# json_response = requests.post('http://localhost:8501/v1/models/fashion_model:predict', data=data, headers=headers)
# predictions = json.loads(json_response.text)['predictions']