# mmllm

This repository contains data and code used in [*the moral machine experiment on large language models*](https://doi.org/10.1098/rsos.231393).

## Terms of use

MIT licensed. Happy if you cite our papers when utilizing the codes:

Takemoto K (2024) **The Moral Machine Experiment on Large Language Models.** R. Soc. Open Sci. 11, 231393.

## Requirements
* Python 3.9
```
pip install -r requirements.txt
```
**NOTE:** The script `run_chatgpt.py` requires an OpenAI API key. Please obtain your API key by following [OpenAI's instructions](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key). To run the script `run_palm2.py`, setup is required. Please refer to the "Setup the PaLM 2 for chat (Python)" section in [the Google Cloud instructions](https://console.cloud.google.com/vertex-ai/publishers/google/model-garden/chat-bison). Before running `run_llama2.py`, the Llama2 model files must be downloaded. Please follow [the instructions provided by Meta](https://github.com/facebookresearch/llama) to download the files.

* R (ver. 4.3.0)
* see also the headers of `figure1.R` and `figure2.R`

## Usage
### Run the Moral Machine experiments on LLMs
For GPT-3.5,
```
python run_chatgpt.py --nb_scenarios 50000
```

For GPT-4,
```
python run_chatgpt.py --model gpt-4-0613 --nb_scenarios 10000
```

For PaLM 2,
```
python run_palm2.py --nb_scenarios 50000
```

For Llama 2,
```
OMP_NUM_THREADS=1 torchrun --nproc_per_node 1 run_llama2.py --ckpt_dir llama-2-7b-chat/
```

The scripts `run_chatgpt.py`, `run_palm2.py`, and `run_llama2.py` rely on both `generate_moral_machine_scenarios.py`, which houses the function for generating Moral Machine scenarios, and `config.py`, which provides the configuration settings for `generate_moral_machine_scenarios.py`. All these files should be placed in the same directory for proper execution.

## Data Analysis (Regenerating the Results)
### Data preprocessing
```
python convert_pickle_csv.py --model gpt-3.5-turbo-0613 --nb_scenarios 50000
```
To specify the model, use the following arguments:
* GPT-4: `--model gpt-4-0613`
* PaLM 2: `--model palm2`
* Llama 2: `--model llama-2-7b-chat`

The column names of the CSV files generated after running `convert_pickle_csv.py` are the same as those in [the previous study](https://www.nature.com/articles/s41586-018-0637-6). For details on the column names, please refer to the "File 2: SharedResponse.csv" section in [the supplemental text of this preceding research](https://osf.io/wt6mc?view_only=4bb49492edee4a8eb1758552a362a2cf).

### Conjoint analysis (Figure 1)

```
Rsctipt figure1.R
```

The script `figure1.R` requires `chatbot_MMFunctionsShared.R`, which houses the function for conducting the conjoint analysis. Both files should be placed in the same directory for seamless operation.

### Distance Computation and PCA (Figure 2)

```
Rsctipt figure2.R
```
