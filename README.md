# mmllm

This repository contains data and code used in the Moral Machine experiment on large language models.

## Terms of use

MIT licensed. Happy if you cite our papers when utilizing the codes:

Takemoto K (2023) The Moral Machine Experiment on Large Language Models.

## Requirements
* Python 3.9
```
pip install -r requirements.txt
```
See also [PaLM 2 for Chat](https://console.cloud.google.com/vertex-ai/publishers/google/model-garden/chat-bison?hl=ja&project=palm2api) and [Llama 2](https://github.com/facebookresearch/llama).
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

## Data Analysis (Regenerating the Results)
Data preprocessing.
```
python convert_pickle_csv.py --model gpt-3.5-turbo-0613 --nb_scenarios 50000
```
To specify the model, use the following arguments:
* GPT-4: `--model gpt-4-0613`
* PaLM 2: `--model palm2`
* Llama 2: `--model llama-2-7b-chat`

Generate Figures 1 and 2
```
Rsctipt figure1.R
Rsctipt figure2.R
```
