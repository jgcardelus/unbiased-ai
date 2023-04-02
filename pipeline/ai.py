import re
import openai
from time import time, sleep
from utils.utils import *

openai.api_key = open_file("./apikey.txt")

def log_response(prompt, response, activity="completion"):
    filename = '%s_%s.txt' % (time(), activity)
    with open('./data/logs/%s' % filename, 'w') as outfile:
        outfile.write('PROMPT:\n\n' + prompt + '\n\n==========\n\nRESPONSE:\n\n' + response)

def ai_completion(prompt, engine='text-davinci-003', temp=0.6, top_p=1.0, tokens=2000, freq_pen=0.25, pres_pen=0.0, stop=['<<END>>']):
    max_retry = 5
    retry = 0
    while True:
        try:
            response = openai.Completion.create(
                engine=engine,
                prompt=prompt,
                temperature=temp,
                max_tokens=tokens,
                top_p=top_p,
                frequency_penalty=freq_pen,
                presence_penalty=pres_pen,
                stop=stop
            )
            text = response['choices'][0]['text'].strip()
            text = re.sub('\s+', ' ', text)
            log_response(prompt, text, "completion")
            return text
        except Exception as error:
            retry += 1
            if retry >= max_retry:
                return "GPT3 error: %s" % error
            print('Error communicating with OpenAI:', error)
            sleep(1)

def ai_completion2(prompt, system, engine="gpt-3.5-turbo"):
    max_retry = 5
    retry = 0
    while True:
        try:
            response = openai.ChatCompletion.create(
                model=engine,
                messages=[
                        {"role": "system", "content": system},
                        {"role": "user", "content": prompt},
                    ]
            )
            text = response['choices'][0]['message']['content']
            text = re.sub('\s+', ' ', text)
            log_response(prompt, text, "completion")
            return text
        except Exception as error:
            retry += 1
            if retry >= max_retry:
                return "GPT3 error: %s" % error
            print('Error communicating with OpenAI:', error)
            sleep(1)

def ai_embeddings(content, engine="text-embedding-ada-002"):
    max_retry = 5
    retry = 0
    while True:
        try:
            content = content.replace("\n", " ")
            result = openai.Embedding.create(input = [content], model=engine)
            embeddings = result['data'][0]['embedding']
            return embeddings
        except Exception as error:
            retry += 1
            if retry >= max_retry:
                return "GPT3 error: %s" % error
            print('Error communicating with OpenAI:', error)
            sleep(1)