# South Park API
![](https://github.com/Jorge-Doncel/API/blob/master/input/south-park-4.jpg)

## Introduction

With this API, you will be able to analyze the sentiment of the conversations of the characters in the series and their similarity respect to others.

You can find all South Park conversations used in this API [here](https://www.kaggle.com/tovarischsukhov/southparklines)

## How does it works?

### Add information to the API

Add a new user: /chat/create/<name>

System will return an error if the character was alredy in the database

```
name="Kahwi"
url = f'http://localhost:3000/chat/create/{name}'
res = requests.get(url)
```

Create a conversation: /chat/create

```
participants= ["Anteto", "Navarro", "Llull"]
dicti={"participants":participants, "chat_name": "Basket" }

url = "http://localhost:3000/chat/create"
res = requests.get(url, params= dicti)
```

Add user to a conversation:/chat/<conversation_id>/adduser

System will return an error if the character was alredy in the conversation
```
conversation_id= "5f0ca16f4c36241d385b895a"
user_name="Gasol"

url = f"http://localhost:3000/chat/{conversation_id}/adduser"
params= f'?user_name={user_name}'
requests.get(url+params)
```

Add message to a conversation: /chat/<conversation_id>/addmessage

```
conversation_id= "5f0ca16f4c36241d385b895a"
user_name="Gasol"
mensaje="I will win the NBA next season"

url = f"http://localhost:3000/chat/{conversation_id}/addmessage"
message={"conversation_id":f'{conversation_id}', "user_name":f'{user_name}' , "message":f'{mensaje}'}
requests.post(url, data=message)

```

Get all messages in a conversation

```
conversation_id= "5f0ca16f4c36241d385b895a"
url = f"http://localhost:3000/chat/{conversation_id}/list"
res = requests.get(url)
```

## Sentiments

Get sentiments by all character and message in an episode: /chat/<conversation_id>/sentiment

```
conversation_id= "5f0ca8de4c36241d385b89ab"
url = f'http://localhost:3000/chat/{conversation_id}/sentiment'
requests.get(url)
```

Get sentiments of specific character by messages in an episode: /chat/<conversation_id>/sentiment

```
conversation_id= "5f0ca8de4c36241d385b89ab"
character= "Cartman"
url = f'http://localhost:3000/chat/{conversation_id}/sentiment/{character}'
requests.get(url)
```
Get sentiments of specific character by messages in an episode:/chat/<conversation_id>/sentiment/<name>
```
conversation_id= "5f0ca8de4c36241d385b89ab"
character= "Cartman"
url = f'http://localhost:3000/chat/{conversation_id}/sentiment/{character}'
requests.get(url)
```
Get total sentiments of a character in an episode: /chat/<conversation_id>/sentiment/<name>/total
```
conversation_id= "5f0ca8de4c36241d385b89ab"
character= "Cartman"
url = f'http://localhost:3000/chat/{conversation_id}/sentiment/{character}/total'
requests.get(url)
```
Get total sentiments of a character in all seasons: /chat/sentiment/<name>
```
character= "Cartman"
url = f'http://localhost:3000/chat/sentiment/{character}'
requests.get(url)
```
Compare 2 character sentiments: /chat/sentiment/<name1>/<name2>
```
character1= "Cartman"
character2= "Stan"
url = f'http://localhost:3000/chat/sentiment/{character1}/{character2}'
requests.get(url)
```

## Recomendations

Find similar characters: /recomendation/<name>

```
character="Cartman"
url = f"http://localhost:3000/recomendation/{character}"
res = requests.get(url)

```

For detailed explanation, check the files.