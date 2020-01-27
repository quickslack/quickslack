import requests
import json

if __name__ == '__main__':
    url = 'http://127.0.0.1:5000/predict'
    # url = 'http://model-api:5000/predict'
    # url = 'http://0.0.0.0:5000/predict'
    # url = 'http://ea7a92c7.ngrok.io'
    input_text = 'My favorite flavor of ice cream is'

    val = {'input_text': input_text}
    r_success = requests.post(url, data=json.dumps(val))

    print(f'request responded: {r_success}.')
    if r_success.status_code == 200:
        print(f'the content of the response was {r_success.json()}')
    else:
        print(r_success)