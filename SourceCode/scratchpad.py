import requests
url = 'https://jsonplaceholder.typicode.com/todos/1' 
response = requests.get(url)        # To execute get request 
print(response.status_code)     # To print http response code  
# print(response.text)            # To print formatted JSON response 