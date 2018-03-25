import requests
def sendMessage(message):
    url = "url to your discord webhook"
    content = {"content":message,"username":"Ichimoku Alert", "avatar_url":"https://freelancerme.com/wp-content/uploads/2018/01/4b8.png"}
    requests.post(url,content)
