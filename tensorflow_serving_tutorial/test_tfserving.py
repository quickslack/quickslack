if __name__ == "__main__":
    import requests, json
    data = json.dumps({"examples":[{"x": [5.1, 3.5, 1.4, 0.2]}]})

    headers = {"content-type": "application/json", "postman-token": "f7fb6e3f-26ba-a742-4ab3-03c953cefaf5"}
    json_response = requests.post('http://localhost:8501/v1/models/iris:classify', data=data, headers=headers)

    print(json_response.text)