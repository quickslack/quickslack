import tensorflow as tf

def tfserving_save(export_dir):
    input_keys_placeholder = tf.placeholder(
        tf.int32,
        shape=[None, 1],
        name="input_keys"
    )
    
    output_keys = tf.identity(
        input_keys_placeholder,
        name="output_keys"
    )

    with tf.Session() as session:
        tf.saved_model.simple_save(
            session,
            export_dir,
            inputs={"keys": input_keys_placeholder},
            outputs={"keys": output_keys}
        )

def tfserve(tf_endpoint, input_data):
    input_data = {
        "model_name": "default",
        "model_version": 1,
        "data": {
            "keys": [[11.0], [2.0]],
            "features": [
                [1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1]
            ]
        }
    }

    with requests.post(tf_endpoint, json=input_data) as response:
        pass
