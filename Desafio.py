import pandas as pd
import requests
import json
from IPython.core.error import UsageError
import openai
from functools import update_wrapper

df = pd.read_csv('santander.csv.txt')
user_ids = df['UserID'].tolist()
santander = 'https://sdw-2023-prd.up.railway.app'
openai_api_key = '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'
openai.api_key = openai_api_key

def get_user(id):
  response = requests.get(f'{santander}/users/{id}')
  return response.json() if response.status_code == 200 else None


users = [user for id in user_ids if (user := get_user(id)) is not None]

print(json.dumps(users, indent=2))



def generate_ai_news(user):
  completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system",
       "content": "você é um especialista em marketing de empréstimo bancário"},

      {"role": "user",
       "content": f"Qual é uma maneira de comunicar diz o nome {user['name']} precisa falar limite {user['account']['limit']} está liberando um empréstimo ótimo, não diz o valor do emprestimo com (maximo de 100 caracteres)"
       }
    ]
)

  return completion.choices[0].message.content.strip('\"')

for user in users:
  news = generate_ai_news(user)
  print(news)
  user['news'].append({
      "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/pay.svg",
      "description": news
  })


def update_user(user):
   response = requests.put(f"{santander}/users/{user['id']}",json=user)
   return True if response.status_code == 200 else False

for user in users:

  sucesso = update_user(user)
  print(f"User {user['name']} updated? {sucesso}!")
