import requests

def test_homepage():
    url = "http://35.237.215.227.sslip.io/"
    response = requests.get(url)
    assert response.status_code == 200

def test_github():
    url = "http://35.237.215.227.sslip.io/github"
    response = requests.get(url)
    assert response.status_code == 200

def test_playground():
    url = "http://35.237.215.227.sslip.io/playground"
    response = requests.get(url)
    assert response.status_code == 200

def test_attacks():
    url = "http://35.237.215.227.sslip.io/attacks"
    response = requests.get(url)
    assert response.status_code == 200

def test_upload():
    url = "http://35.237.215.227.sslip.io/upload"
    response = requests.get(url)
    assert response.status_code == 200

def test_members():
    url = "http://35.237.215.227.sslip.io/members"
    response = requests.get(url)
    assert response.status_code == 200

def test_external_upload():
    url = "http://35.237.215.227.sslip.io/upload"
    response = requests.post(url)
    assert response.status_code == 405

def test_upload_end():
    url = "http://34.148.135.143:8000/predict/"
    response = requests.post(url)
    assert response.status_code == 422