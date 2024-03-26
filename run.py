import pandas as pd
import random
from tqdm import tqdm

from generate_moral_machine_scenarios import generate_moral_machine_scenarios
from chatapi import ChatBotManager
from chatmodel import ChatModel

import argparse

#### Parameters #############
parser = argparse.ArgumentParser()
parser.add_argument('--model', default='gpt-3.5-turbo-0613', type=str)
parser.add_argument('--nb_scenarios', default='3', type=int)
parser.add_argument('--random_seed', default='123', type=int)
args = parser.parse_args()

# load LLM model (API)
if any(s in args.model for s in ["gpt", "gemini", "claude", "palm"]):
  chat_model = ChatBotManager(model=args.model)
elif any(s in args.model for s in ["llama", "vicuna", "gemma"]):
  chat_model = ChatModel(model=args.model)
else:
  raise ValueError("Unsupported model")

# obtain LLM responses
file_name = 'results_{}_scenarios_seed{}_{}.pickle'.format(args.nb_scenarios, args.random_seed, args.model)
random.seed(args.random_seed)
scenario_info_list = []
for i in tqdm(range(args.nb_scenarios)):
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

  # obtain chatgpt response
  response = chat_model.chat(system_content, user_content)
  scenario_info['chat_response'] = response
  #print(scenario_info)

  scenario_info_list.append(scenario_info)

  if (i+1) % 100 == 0:
    df = pd.DataFrame(scenario_info_list)
    df.to_pickle(file_name)

df = pd.DataFrame(scenario_info_list)
df.to_pickle(file_name)
