from functools import reduce
# from modules import extra_networks
# from modules import prompt_parser
import math

def get_prompt_lengths_on_ui(prompt):
    chunk_length = 75
    r = len(prompt.strip('!,. ').replace(' ', ',').replace('.', ',').replace('!', ',').replace(',,', ',').replace(',,', ',').replace(',,', ',').replace(',,', ',').split(','))
    return r, math.ceil(max(r, 1) / chunk_length) * chunk_length

def get_token_counter(text, steps):

    prompt_schedules = [[[steps, text]]]


    flat_prompts = reduce(lambda list1, list2: list1 + list2, prompt_schedules)
    prompts = [prompt_text for step, prompt_text in flat_prompts]

    token_count, max_length = max([get_prompt_lengths_on_ui(prompt) for prompt in prompts],key=lambda args: args[0])


    

    return {"token_count": token_count, "max_length": max_length}
