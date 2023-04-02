import os
import textwrap

from time import time
from utils.utils import *
from pipeline.ai import ai_completion, ai_completion2

def summarize(text, wrap=2000, doc_id=None, height=0, log=False, path="./data/logs"):
    text_chunks = textwrap.wrap(text, wrap)
    summarized_chunks = list()

    for text_chunk in text_chunks:
        prompt = open_file("./prompts/summarize2.txt").replace("<<TEXT>>", text_chunk)
        prompt = decode(prompt)
        summarized_chunk = ai_completion2(prompt, "You are an unbiased summarizer", engine="gpt-3.5-turbo")
        summarized_chunks.append(summarized_chunk)
    summary = "\n\n".join(summarized_chunks)

    if log:
        filename = ""
        if doc_id is not None:
            filename += doc_id + "_"
        filename += "%s-" % time()
        filename += str(height)
        filename += ".txt"
        complete_path = os.path.join(path, filename)
        write_file(complete_path, summary)

    return summary

def recursively_summarize(data, title, target_size=500, save=True):
    summary = data

    height = 0
    while get_tokens(summary) > target_size and height < 10:
        summary = summarize(summary, doc_id=title, height=height, log=True)
        print("\n\n===============SUMMARY=================\n\n")
        print(summary)
        height += 1

    if save:
        filename = os.path.join("./data/summaries", title + ".txt")
        write_file(filename, summary)
    
    return summary

def summarize_document(document_path, document_title, target_size=500, save=True):
    document = open_file(document_path)
    summary = recursively_summarize(document, document_title, target_size, save)

    return summary