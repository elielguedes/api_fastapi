import requests

headers = {
    "Authorization":"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMyIsImV4cCI6MTc2NTE0NDk2MH0.YulJWxE_SssGs_YfkCwiQ70KokrcvqBOjDVC5HxAxrA"
}


requisicao = requests.get("http://127.0.0.1:8000/auth/refresh", headers = headers)
print (requisicao)
print (requisicao.json())