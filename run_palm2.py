import vertexai
from vertexai.preview.language_models import ChatModel, InputOutputTextPair

import pandas as pd
import random
from tqdm import tqdm
import time

from generate_moral_machine_scenarios import generate_moral_machine_scenarios

import argparse

vertexai.init(project="YOUR_PROJECT_NAME", location="YOUR_LOCATION")
chat_model = ChatModel.from_pretrained("chat-bison@001")
parameters = {
    "temperature": 0.2,
    "max_output_tokens": 256,
    "top_p": 0.8,
    "top_k": 40
}

#### Parameters #############
parser = argparse.ArgumentParser(description='Run Palm2')
parser.add_argument('--model', default='palm2', type=str)
parser.add_argument('--nb_scenarios', default='3', type=int)
parser.add_argument('--random_seed', default='123', type=int)
args = parser.parse_args()

def palm2_response(system_cont, user_cont):
    try:
        chat = chat_model.start_chat(context="Please respond to binary questions. {}".format(system_cont))
        res = chat.send_message(user_cont, **parameters)
    
    except Exception as e:
        time.sleep(5)
        res = palm2_response(system_cont, user_cont)
    
    return str(res)

random.seed(args.random_seed)
scenario_info_list = []
for i in tqdm(range(args.nb_scenarios)):
    # scenario dimension
    dimension = random.choice(["species", "social_value", "gender", "age", "fitness", "utilitarianism"])
    # Interventionism #########
    is_interventionism = random.choice([True, False])
    # Relationship to vehicle #########
    is_in_car = random.choice([True, False])
    # Concern for law #########
    is_law = random.choice([True, False])
    
    # generate a scenario
    system_content, user_content, scenario_info = generate_moral_machine_scenarios(dimension, is_in_car, is_interventionism, is_law)

    # obtain chatgpt response
    response = palm2_response(system_content, user_content)
    scenario_info['palm2_response'] = response

    scenario_info_list.append(scenario_info)

    if (i+1) % 100 == 0:
        df = pd.DataFrame(scenario_info_list)
        df.to_pickle('results_{}_scenarios_seed{}_{}.pickle'.format(args.nb_scenarios, args.random_seed, args.model))

df = pd.DataFrame(scenario_info_list)
df.to_pickle('results_{}_scenarios_seed{}_{}.pickle'.format(args.nb_scenarios, args.random_seed, args.model))
