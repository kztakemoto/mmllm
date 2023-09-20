from typing import Optional

import fire

from llama import Llama

import pandas as pd
import random
from tqdm import tqdm
import time

from generate_moral_machine_scenarios import generate_moral_machine_scenarios

def main(
    ckpt_dir: str,
    tokenizer_path: str = "tokenizer.model",
    temperature: float = 0.6,
    top_p: float = 0.9,
    max_seq_len: int = 512,
    max_batch_size: int = 1,
    max_gen_len: Optional[int] = None,
):
    generator = Llama.build(
        ckpt_dir=ckpt_dir,
        tokenizer_path=tokenizer_path,
        max_seq_len=max_seq_len,
        max_batch_size=max_batch_size,
    )

    nb_scenarios = 50000
    random_seed = 123

    random.seed(random_seed)
    scenario_info_list = []
    for i in tqdm(range(nb_scenarios)):
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

        dialogs = [
            [
                {"role": "system", "content": "Please respond to binary questions.\n\n{}".format(system_content)},
                {"role": "user", "content": "{}".format(user_content)},
            ],
        ]
        results = generator.chat_completion(
            dialogs,  # type: ignore
            max_gen_len=128,
            temperature=temperature,
            top_p=top_p,
        )
        #print(dialogs)
        #print(results[0]['generation']['content'])

        scenario_info['llama2_response'] = results[0]['generation']['content']

        scenario_info_list.append(scenario_info)

        if (i+1) % 100 == 0:
            df = pd.DataFrame(scenario_info_list)
            df.to_pickle('results_{}_scenarios_seed{}_{}.pickle'.format(nb_scenarios, random_seed, ckpt_dir.replace("/", "")))

    df = pd.DataFrame(scenario_info_list)
    df.to_pickle('results_{}_scenarios_seed{}_{}.pickle'.format(nb_scenarios, random_seed, ckpt_dir.replace("/", "")))


if __name__ == "__main__":
    fire.Fire(main)
