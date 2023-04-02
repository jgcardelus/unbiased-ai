import json
from utils.utils import *
from pipeline.ai import ai_completion2
from pipeline.embeddings import search_index
from pipeline.summarizer import recursively_summarize

def ask_question(query, data):
    passages = search_index(query, data, 5)

    answers = list()
    for passage in passages:
        prompt = open_file("./prompts/searcher.txt")
        prompt = prompt.replace("<<CONTEXT>>", passage["content"])
        prompt = prompt.replace("<<QUERY>>", query)
        print("\n\n===============ANSWERING QUESTION=================\n\n")
        print("\n\n---------------" + passage["source"] + "-----------------\n\n")
        answer = ai_completion2(
            prompt, 
            "You respond using only the provided context to questions. You are honest and detailed in your responses. You speak spanish."
        )
        print(answer)
        answers.append(answer)

    answers_combined = "\n\n".join(answers)
    answers_summarized = recursively_summarize(answers_combined, "answers-sumarized", save=False)

    print("\n\n===============FINAL ANSWER=================\n\n")
    print(answers_summarized)

def ask_questions():
    data = json.loads(open_file("./data/embeddings/articles.json"))
    while True:
        query = input("Dame una pregunta: ")
        ask_question(query, data)