# mmllm

This repository contains data and code used in the Moral Machine experiment on large language models.

## Terms of use

This project is MIT licensed. If you use this code in your research, please cite our papers:

+ Takemoto K (2024) **The Moral Machine Experiment on Large Language Models.** R. Soc. Open Sci. 11, 231393. https://doi.org/10.1098/rsos.231393
+ Ahmad MSZ and Takemoto K (2025) **Large-Scale Moral Machine Experiment on Large Language Models.** PLoS One, 20, e0322776. https://doi.org/10.1371/journal.pone.0322776

## Requirements
* Python 3.11 and PyTorch (v2.3.1; for the open-source LLMs such as Llama)
```
pip install -r requirements.txt
```
**NOTE:** To run the script `run.py`, an OpenAI API key for ChatGPT (GPT-3.5 and GPT-4) and Anthropic API key for Claude 3 are required. Please obtain your API key by following [OpenAI's instructions](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key), [Anthropic's instructions](https://support.anthropic.com/en/articles/8114521-how-can-i-access-the-claude-api), [DeepSeek's instructions](https://api-docs.deepseek.com/api/deepseek-api), and [xAI's instructions](https://docs.x.ai/docs/overview). For PaLM 2 and Gemini, setup is required. Please refer to [the Google Cloud instructions](https://cloud.google.com/vertex-ai/generative-ai/docs/start/quickstarts/quickstart-multimodal). The API keys and Google Cloud information must be specified in the `chatapi.py` file. The Llama 2 model files must be downloaded. Please follow the instructions on [Llama2](https://github.com/facebookresearch/llama) provided by Meta to download the files. The files should be placed in the same directory for proper execution.

* R (ver. 4.4.1)
* see also the headers of `figure1.R` and `figure2.R`

## Usage
### Run the Moral Machine experiments on LLMs
For GPT-3.5 (gpt-3.5-turbo-0613; no longer be available on September 13, 2024)
```
python run.py --model gpt-3.5-turbo-0613 --nb_scenarios 50000
```
To specify the model, use the following arguments:
* OpenAI
  * GPT-3.5:
    * `--model gpt-3.5-turbo-0301` (March 2023 version; no longer be available on September 13, 2024)
    * `--model gpt-3.5-turbo-1106` (November 2023 version)
    * `--model gpt-3.5-turbo-0125` (January 2024 version)
  * GPT-4:
    * `--model gpt-4-0314` (March 2023 version)
    * `--model gpt-4-0613` (June 2023 version)
    * `--model gpt-4-1106-preview` (November 2023 version)
    * `--model gpt-4-0125-preview` (January 2024 version)
    * `--model gpt-4-turbo-2024-04-09` (April 2024 version)
  * GPT-4o:
    * `--model gpt-4o-2024-05-13` (May 2024 version)
    * `--model gpt-4o-2024-08-06` (August 2024 version)
    * `--model gpt-4o-2024-11-20` (November 2024 version)
  * GPT-4o-mini: `--model gpt-4o-mini-2024-07-18`
  * GPT-4.1: `--model gpt-4.1-2025-04-14`
  * GPT-4.1-mini: `--model gpt-4.1-mini-2025-04-14`
  * GPT-4.1-nano: `--model gpt-4.1-nano-2025-04-14`
  * GPT-4.5: `--model gpt-4.5-preview-2025-02-27`
  * o1:
    * `--model o1-preview-2024-09-12` (September 2024 version)
    * `--model o1-2024-12-17` (December 2024 version)
  * o1-mini: `--model o1-mini-2024-09-12`
  * o3-mini: `--model o3-mini-2025-01-31`
  * o3: `--model o3-2025-04-16`
  * o4-mini: `--model o4-mini-2025-04-16`
* PaLM 2: `--model palm2`
* Gemini
  * 1.0 Pro: `--model gemini-1.0-pro-001`
  * 1.5 Pro:
    * `--model gemini-1.5-pro-preview-0409` (April 2024 preview version)
    * `--model gemini-1.5-pro-preview-0514` (May 2024 preview version)
    * `--model gemini-1.5-pro-001`
    * `--model gemini-1.5-pro-002`
  * 1.5 Flash:
    * `--model gemini-1.5-flash-preview-0514` (Preview version)
    * `--model gemini-1.5-flash-001`
    * `--model gemini-1.5-flash-002`
  * 2.0 Flash:
    * `--model gemini-2.0-flash-exp`
    * `--model gemini-2.0-flash-001`
  * 2.0 Flash Lite: `--model gemini-2.0-flash-lite-preview-02-05`
  * 2.0 Flash Thinking: `--model gemini-2.0-flash-thinking-exp-01-21`
  * 2.0 Pro: `--model gemini-2.0-pro-exp-02-05`
  * 2.5 Pro:
    * `--model gemini-2.5-pro-exp-03-25` (Experimental version)
    * `--model gemini-2.5-pro-preview-03-25` (Preview version)
  * 2.5 Flash: `--model gemini-2.5-flash-preview-04-17` 
* Claude
  * 3 Haiku: `--model claude-3-haiku-20240307`
  * 3 Sonnet: `--model claude-3-sonnet-20240229`
  * 3 Opus: `--model claude-3-opus-20240229`
  * 3.5 Sonnet (June 2024 version): `--model claude-3-5-sonnet-20240620`
  * 3.5 Sonnet (October 2024 version): `--model claude-3-5-sonnet-20241022`
  * 3.5 Haiku: `--model claude-3-5-haiku-20241022`
  * 3.7 Sonnet: `--model claude-3-7-sonnet-20250219`
  * 3.7 Sonnet with thinking: `--model claude-3-7-sonnet-20250219_thinking`
  * 4 Sonnet: `--model claude-sonnet-4-20250514`
  * 4 Sonnet with thinking: `--model claude-sonnet-4-20250514_thinking`
  * 4 Opus: `--model claude-opus-4-20250514`
  * 4 Opus with thinking: `--model claude-opus-4-20250514_thinking`
* Llama
  * 2 7B Chat: `--model llama-2-7b-chat`
  * 3 8B Instruct: `--model Meta-Llama-3-8B-Instruct`
  * 3 70B Instruct: `--model Meta-Llama-3-70B-Instruct`
  * 3.1 8B Instruct: `--model Meta-Llama-3.1-8B-Instruct`
  * 3.1 70B Instruct: `--model Meta-Llama-3.1-70B-Instruct`
  * 3.2 1B Instruct: `--model Llama-3.2-1B-Instruct`
  * 3.2 3B Instruct: `--model Llama-3.2-3B-Instruct`
  * 3.3 70B Instruct: `--model Llama-3.3-70B-Instruct`
* Vicuna
  * 7B: `--model vicuna-7b-v1.5`
  * 13B: `--model vicuna-13b-v1.5` 
* Mistral: `--model Mistral-7B-Instruct-v0.2`
* Mistral-NeMo: `--model Mistral-Nemo-Instruct-2407`
* Gemma
  * 2B-it: `--model gemma-2b-it`
  * 7B-it: `--model gemma-7b-it`
  * 1.1-2B-it: `--model gemma-1.1-2b-it`
  * 1.1-7B-it: `--model gemma-1.1-7b-it`
  * 2-2b-it: `--model gemma-2-2b-it`
  * 2-9B-it: `--model gemma-2-9b-it`
  * 2-27B-it: `--model gemma-2-27b-it`
  * DataGemma RIG 27B: `--model datagemma-rig-27b-it`
  * 3-1B-it: `--model gemma-3-1b-it`
  * 3-4B-it: `--model gemma-3-4b-it`
  * 3-12B-it: `--model gemma-3-12b-it`
  * 3-27B-it: `--model gemma-3-27b-it`
* Command R+: `--model c4ai-command-r-plus-4bit`
* Phi
  *  3.5 MoE-instruct: `--model Phi-3.5-MoE-instruct`
  *  3.5 mini-instruct: `--model Phi-3.5-mini-instruct`
  *  4: `--model phi-4`
  *  4 mini-instruct: `--model Phi-4-mini-instruct`
* Qwen
  * 2.5 0.5B: `--model Qwen2.5-0.5B-Instruct`
  * 2.5 1.5B: `--model Qwen2.5-1.5B-Instruct`
  * 2.5 3B: `--model Qwen2.5-3B-Instruct`
  * 2.5 7B: `--model Qwen2.5-7B-Instruct`
  * 2.5 14B: `--model Qwen2.5-14B-Instruct`
  * 2.5 32B: `--model Qwen2.5-32B-Instruct`
  * 2.5 72B: `--model Qwen2.5-72B-Instruct`
  * 3 0.6B: `--model Qwen3-0.6B`
  * 3 1.7B: `--model Qwen3-1.7B`
  * 3 4B: `--model Qwen3-4B`
  * 3 8B: `--model Qwen3-8B`
  * 3 14B: `--model Qwen3-14B`
  * 3 32B: `--model Qwen3-32B`
* QwQ 32B: `--model QwQ-32B`
* Deepseek
  * V3: `--model deepseek-chat` (December 2024 and March 2025 versions)
  * R1: `--model deepseek-reasoner` (January 2025 and May 2025 versions)
  * R1-Llama-8B: `--model DeepSeek-R1-Distill-Llama-8B`
  * R1-Llama-70B: `--model DeepSeek-R1-Distill-Llama-70B`
  * R1-Qwen-1.5B: `--model DeepSeek-R1-Distill-Qwen-1.5B`
  * R1-Qwen-7B: `--model DeepSeek-R1-Distill-Qwen-7B`
  * R1-Qwen-14B: `--model DeepSeek-R1-Distill-Qwen-14B`
  * R1-Qwen-32B: `--model DeepSeek-R1-Distill-Qwen-32B`
* Grok
  * 2: `--model grok-2-1212`
  * 3: `--model grok-3-beta`
  * 3-fast: `--model grok-3-fast-beta`
  * 3-mini: `--model grok-3-mini-beta`
  * 3-mini-fast: `--model grok-3-mini-fast-beta`

NOTE: For Llama 2, run as follows:
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

### Conjoint analysis
Figure 1 in [Takemoto (2024)](https://doi.org/10.1098/rsos.231393)
```
Rsctipt figure1.R
```

The script `figure1.R` requires `chatbot_MMFunctionsShared.R`, which houses the function for conducting the conjoint analysis. Both files should be placed in the same directory for seamless operation.

### Distance Computation and PCA
Figure 2 in [Takemoto (2024)](https://doi.org/10.1098/rsos.231393)
```
Rsctipt figure2.R
```
