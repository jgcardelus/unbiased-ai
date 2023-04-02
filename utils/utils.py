import os

def write_file(filename, data):
    with open(filename, "w") as f:
        f.write(data)

def open_file(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return f.read()
    else:
        raise Exception("File doesn't exist")
    
def load_summaries(names):
    summaries = {}
    for name in names:
        filename = os.path.join("./data/summaries", name+".txt")
        summaries[name] = open_file(filename)
    return summaries

def load_articles(names):
    articles = {}
    for name in names:
        filename = os.path.join("./data/raw", name+".txt")
        articles[name] = open_file(filename)
    return articles
    
def decode(string):
    return string.encode(encoding='ASCII',errors='ignore').decode()

def get_tokens(string):
    return len(string) // 4