import requests

endpoint = "http://localhost:8000/auth/get_token/"


def get_token():
    data = {
    'username':"lordace",
    'password':"lordace",
    
}
    response = requests.post(endpoint,json=data)
    if response.status_code == 200:
        response = response.json()
        print(response.get('token'))
        return response.get('token')
    else:
        print(response.json(),response.status_code)