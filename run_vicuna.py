import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

import pandas as pd
import random
from tqdm import tqdm

from generate_moral_machine_scenarios import generate_moral_machine_scenarios

import argparse

#### Parameters #############
parser = argparse.ArgumentParser(description='Run Vicuna')
parser.add_argument('--model', default='vicuna-13b-v1.5', type=str)
parser.add_argument('--nb_scenarios', default='50000', type=int)
parser.add_argument('--random_seed', default='123', type=int)
parser.add_argument('--temp', default='0.7', type=float)
args = parser.parse_args()

model_name = args.model
tokenizer = AutoTokenizer.from_pretrained(
    "lmsys/{}".format(model_name),
    use_fast=False,
)
model = AutoModelForCausalLM.from_pretrained(
    "lmsys/{}".format(model_name),
    load_in_8bit=True,
    torch_dtype=torch.float16,
    device_map="auto",
)

nb_scenarios = args.nb_scenarios
random_seed = args.random_seed

# obtain LLM responses
file_name = 'results_{}_scenarios_seed{}_{}_temp{}.pickle'.format(nb_scenarios, random_seed, model_name, args.temp)
random.seed(random_seed)
scenario_info_list = []
for i in tqdm(range(nb_scenarios)):
    # scenario dimension
    dimension = random.choice(["species", "social_value", "gender", "age", "fitness", "utilitarianism"])
    #dimension = "random"
    # Interventionism #########
    is_interventionism = random.choice([True, False])
    # Relationship to vehicle #########
    is_in_car = random.choice([True, False])
    # Concern for law #########
    is_law = random.choice([True, False])
    
    # generate a scenario
    system_content, user_content, scenario_info = generate_moral_machine_scenarios(dimension, is_in_car, is_interventionism, is_law)

    prompt = "USER: Please respond to binary questions.\n\n{}\n\n{}\n\nASSISTANT:".format(system_content, user_content)

    token_ids = tokenizer.encode(prompt, add_special_tokens=False, return_tensors="pt")
    with torch.no_grad():
        output_ids = model.generate(
            token_ids.to(model.device),
            max_new_tokens=512,
            do_sample=True,
            temperature=args.temp,
            top_p=1.0,
            pad_token_id=tokenizer.pad_token_id,
            bos_token_id=tokenizer.bos_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )
    output = tokenizer.decode(output_ids.tolist()[0][token_ids.size(1):])
    #print(output)

    scenario_info['vicuna_response'] = str(output)

    scenario_info_list.append(scenario_info)

    if (i+1) % 100 == 0:
        df = pd.DataFrame(scenario_info_list)
        df.to_pickle(file_name)

df = pd.DataFrame(scenario_info_list)
df.to_pickle(file_name)

