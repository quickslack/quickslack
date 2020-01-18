import requests, json, time

if __name__ == "__main__":
    data = [[40,588,284,1100,9473,546,1919,29641,780]]

    headers = {
        "content-type": "application/json",
        "postman-token": "f7fb6e3f-26ba-a742-4ab3-03c953cefaf5"
    }
    # this is a change
    body = {
        "signature_name": "predict",
        "inputs": data
    }
    now = time.time()
    json_response = requests.post(
        'http://tf-serving:8501/v1/models/distilgpt2:predict',
        data=json.dumps(body),
        headers=headers
        )

    print(f'EXEC TIME: {time.time()-now}')
    print(json_response.text)