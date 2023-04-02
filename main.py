import os
import json
from utils.utils import *

from pipeline.summarizer import summarize_document
from pipeline.combinator import combine_n
from pipeline.embeddings import embed_document
from pipeline.questions import ask_questions

def summarize_articles(documents=["abc", "elpais", "ser", "elmundo"]):
    for document in documents:
        filename = os.path.join("./data/raw", document+".txt")
        summary = summarize_document(filename, document)
        print("\n\n===============FINAL SUMMARY=================\n\n")
        print(summary)

def combine_article_summaries(documents=["abc", "elpais", "ser", "elmundo"]):
    summaries = load_summaries(documents)
    combined_data = combine_n(**summaries)
    print("\n\n===============FINAL COMBINATION=================\n\n")
    print(combined_data)

def embed_articles(documents=["abc", "elpais", "ser", "elmundo"]):
    article_embeddings = []
    for document in documents:
        filename = os.path.join("./data/raw", document+".txt")
        embedding = embed_document(filename, document)
        article_embeddings.extend(embedding)

    print("\n\n===============EMBEDDINGS DONE=================\n\n")
    
    filename = os.path.join("./data/embeddings", "articles.json")
    write_file(filename, json.dumps(article_embeddings))


if __name__ == "__main__":
    ask_questions()
