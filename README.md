# mmllm

This repository contains data and code used in [*the moral machine experiment on large language models*](https://doi.org/10.1098/rsos.231393).

## Terms of use

MIT licensed. Happy if you cite our papers when utilizing the codes:

Takemoto K (2024) **The Moral Machine Experiment on Large Language Models.** R. Soc. Open Sci. 11, 231393.

## Requirements
* Python 3.11 and PyTorch (v2.1.2; for Llama, Vicuna, Gemma)
```
pip install -r requirements.txt
```
**NOTE:** To run the script `run.py`, an OpenAI API key for ChatGPT (GPT-3.5 and GPT-4) and Anthropic API key for Claude 3 are required. Please obtain your API key by following [OpenAI's instructions](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key) and [Anthropic's instructions](https://support.anthropic.com/en/articles/8114521-how-can-i-access-the-claude-api). For PaLM 2 and Gemini, setup is required. Please refer to [the Google Cloud instructions](https://cloud.google.com/vertex-ai/generative-ai/docs/start/quickstarts/quickstart-multimodal). The API keys and Google Cloud information must be specified in the `chatapi.py` file. The Llama2 model files must be downloaded. Please follow [the instructions provided by Meta](https://github.com/facebookresearch/llama) to download the files. The files should be placed in the same directory for proper execution. For Gemma, authentication is needed. Please refer to [the HuggingFace instructions](https://huggingface.co/docs/huggingface_hub/quick-start#authentication).

* R (ver. 4.3.0)
* see also the headers of `figure1.R` and `figure2.R`

## Usage
### Run the Moral Machine experiments on LLMs
For GPT-3.5 (June 2023 version; gpt-3.5-turbo-0613)
```
python run.py --model gpt-3.5-turbo-0613 --nb_scenarios 50000
```
To specify the model, use the following arguments:
* GPT-3.5:
  * `--model gpt-3.5-turbo-1106` (November 2023 version)
  * `--model gpt-3.5-turbo-0125` (January 2024 version)
* GPT-4:
  * `--model gpt-4-0613` (June 2023 version)
  * `--model gpt-4-1106-preview` (November 2023 version)
  * `--model gpt-4-0125-preview` (January 2024 version)
  * `--model gpt-4-turbo-2024-04-09` (April 2024 version)
* PaLM 2: `--model palm2`
* Gemini-Pro: `--model gemini-pro`
* Claude 3:
  * Haiku: `--model claude-3-haiku-20240307`
  * Sonnet: `--model claude-3-sonnet-20240229`
  * Opus: `--model claude-3-opus-20240229`
* Llama 2: `--model llama-2-7b-chat`
* Vicuna: `--model vicuna-13b-v1.5`
* Gemma:
  * 2B-it `--model gemma-2b-it`
  * 7B-it `--model gemma-7b-it`

NOTE: For GPT-4 and Claude 3 Opus, `--nb_scenarios 10000` was used, considering the API usage cost constraints.
For Llama 2, run as follows:
```
OMP_NUM_THREADS=1 torchrun --nproc_per_node 1 run.py --model llama-2-7b-chat
```

The script `run.py` rely on both `generate_moral_machine_scenarios.py`, which houses the function for generating Moral Machine scenarios, and `config.py`, which provides the configuration settings for `generate_moral_machine_scenarios.py`. All these files should be placed in the same directory for proper execution.

NOTE: The scenarios and responses we obtained are available in the `results` directory.

## Data Analysis (Regenerating the Results)
### Data preprocessing
```
python convert_pickle_csv.py --model gpt-3.5-turbo-0613 --nb_scenarios 50000
```
Use the above arguments to specify the model.

The column names of the CSV files generated after running `convert_pickle_csv.py` are the same as those in [the previous study](https://www.nature.com/articles/s41586-018-0637-6). For details on the column names, please refer to the "File 2: SharedResponse.csv" section in [the supplemental text of this preceding research](https://osf.io/wt6mc?view_only=4bb49492edee4a8eb1758552a362a2cf).

NOTE: All datasets used in this study are available in the `data` directory.

### Conjoint analysis (Figure 1)

```
Rsctipt figure1.R
```

The script `figure1.R` requires `chatbot_MMFunctionsShared.R`, which houses the function for conducting the conjoint analysis. Both files should be placed in the same directory for seamless operation.

### Distance Computation and PCA (Figure 2)

```
Rsctipt figure2.R
```
