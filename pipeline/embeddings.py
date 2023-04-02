import os
import json
import textwrap
import numpy as np

from utils.utils import *
from pipeline.ai import ai_embeddings

def embed(text, source=None, wrap=2000):
    text_chunks = textwrap.wrap(text, wrap)
    embeddings = []

    for text_chunk in text_chunks:
        embedding = ai_embeddings(decode(text_chunk))
        info = {"content": text_chunk, "vector": embedding, "source": source}
        embeddings.append(info)

    return embeddings

def embed_document(document_path, document_title, save=False):
    print("\n\n===============EMBEDDING=================\n\n")
    print(document_title)
    document = open_file(document_path)
    embeddings = embed(document, source=document_title)

    if save:
        filename = os.path.join("./data/embeddings", document_title + ".json")
        write_file(filename, json.dumps(embeddings))

    return embeddings

def similarity(v1, v2):
    return np.dot(v1, v2)

def search_index(text, data, count=20):
    embeddings = embed(text, "user")
    vector = embeddings[0]["vector"]

    scores = list()
    for chunk in data:
        challenge_vector = chunk["vector"]
        score = similarity(vector, challenge_vector)
        scores.append({
            "content": chunk["content"],
            "score": score,
            "source": chunk["source"]
        })
    
    ordered = sorted(scores, key=lambda d: d['score'], reverse=True)
    return ordered[:count]