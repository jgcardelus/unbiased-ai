import random
from utils.utils import *
from pipeline.ai import ai_completion2
from pipeline.summarizer import recursively_summarize

def combine(data_a, data_b, title_a, title_b, target_size=500, save=True):
    prompt = open_file("./prompts/combinator.txt")
    prompt = prompt.replace("<<TEXT1>>", data_a)
    prompt = prompt.replace("<<TEXT2>>", data_b)

    combined_data = ai_completion2(
        prompt,
        "Your job is to combine texts without losing information and doing it in a coherent way. You speak Spanish."
    )

    title = "_".join([title_a, title_b])
    if get_tokens(combined_data) > target_size:
        combined_data = recursively_summarize(combined_data, title, target_size, save)

    print("\n\n===============COMBINATION=================\n\n")
    print(combined_data)

    if save:
        filename = os.path.join("./data/combinations", title + ".txt")
        write_file(filename, combined_data)

    return combined_data

def combine_n(target_size=1000, save=True, **kwargs):
    combinations = kwargs
    combinations_keys = list(combinations.keys())

    if len(combinations_keys) == 1:
        return combinations[combinations_keys[0]]
    
    while len(combinations.keys()) > 1:
        new_combinations = {}
        combinations_keys = list(combinations.keys()) 

        if len(combinations_keys) % 2 != 0:
            pairable_keys = combinations_keys[:len(combinations_keys)-1]
            selected_key = random.choice(pairable_keys)
            combinations_keys.append(selected_key)

        for i in range(0,len(combinations_keys),2):
            title_a = combinations_keys[i]
            data_a = combinations[title_a]
            title_b = combinations_keys[i+1]
            data_b = combinations[title_b]

            combination = combine(data_a, data_b, title_a, title_b, target_size=target_size, save=save)
            new_combinations[title_a + "_" + title_b] = combination

        combinations = new_combinations

    combined_data = combinations[list(combinations.keys())[0]]
    if save:
        filename = os.path.join("./data/combinations", "final.txt")
        write_file(filename, combined_data)

    return combined_data