import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, Gemma3ForConditionalGeneration

class ChatModel:
    def __init__(self, model):
        self.model = model

        if "deepseek" in self.model.lower():
            self.tokenizer = AutoTokenizer.from_pretrained(
                "deepseek-ai/{}".format(self.model),
            )

            self.generator = AutoModelForCausalLM.from_pretrained(
                f"deepseek-ai/{self.model}",
                torch_dtype=torch.bfloat16,
                device_map="auto",
            )
        
        elif "qwen" in self.model.lower() or "qwq" in self.model.lower():
            self.tokenizer = AutoTokenizer.from_pretrained(
                "Qwen/{}".format(self.model),
            )

            if "72b" in self.model.lower():
                    self.generator = AutoModelForCausalLM.from_pretrained(
                        f"Qwen/{self.model}",
                        load_in_4bit=True,
                        bnb_4bit_compute_dtype=torch.bfloat16,
                        device_map="auto",
                    )

            else:
                self.generator = AutoModelForCausalLM.from_pretrained(
                    f"Qwen/{self.model}",
                    torch_dtype=torch.bfloat16,
                    device_map="auto",
                )

        elif "llama" in self.model.lower():
            if "llama-3" in self.model.lower():
                self.tokenizer = AutoTokenizer.from_pretrained(
                    f"meta-llama/{self.model}",
                )

                if self.tokenizer.pad_token is None:
                    self.tokenizer.pad_token = self.tokenizer.eos_token

                if "70b" in self.model.lower():
                    self.generator = AutoModelForCausalLM.from_pretrained(
                        f"meta-llama/{self.model}",
                        load_in_4bit=True,
                        bnb_4bit_compute_dtype=torch.bfloat16,
                        device_map="auto",
                    )

                else:
                    self.generator = AutoModelForCausalLM.from_pretrained(
                        f"meta-llama/{self.model}",
                        torch_dtype=torch.bfloat16,
                        device_map="auto",
                    )
            else:
                from llama import Llama
                self.generator = Llama.build(
                    ckpt_dir=f"./{self.model}/",
                    tokenizer_path=f"./{self.model}/tokenizer.model",
                    max_seq_len=512,
                    max_batch_size=1,
                )

        elif "vicuna" in self.model.lower():
            self.tokenizer = AutoTokenizer.from_pretrained(
                "lmsys/{}".format(self.model),
                use_fast=False,
            )
            self.generator = AutoModelForCausalLM.from_pretrained(
                "lmsys/{}".format(self.model),
                torch_dtype=torch.float16,
                device_map="auto",
            )
        elif "gemma" in self.model.lower():
            self.tokenizer = AutoTokenizer.from_pretrained(
                "google/{}".format(self.model),
                use_fast=False,
            )

            if "gemma-3" in self.model.lower():
                self.generator = Gemma3ForConditionalGeneration.from_pretrained(
                    "google/{}".format(self.model),
                    torch_dtype=torch.bfloat16,
                    device_map="auto",
                )
            else:
                self.generator = AutoModelForCausalLM.from_pretrained(
                    "google/{}".format(self.model),
                    torch_dtype=torch.bfloat16,
                    device_map="auto",
                )
                
        elif "mistral" in self.model.lower():
            self.tokenizer = AutoTokenizer.from_pretrained(
                "mistralai/{}".format(self.model),
                use_fast=False,
            )

            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token

            self.generator = AutoModelForCausalLM.from_pretrained(
                "mistralai/{}".format(self.model),
                torch_dtype=torch.float16,
                device_map="auto",
            )
            
        elif "command" in self.model.lower():
            self.tokenizer = AutoTokenizer.from_pretrained(
                "CohereForAI/{}".format(self.model),
            )

            self.generator = AutoModelForCausalLM.from_pretrained(
                "CohereForAI/{}".format(self.model),
                device_map="auto",
            )
        elif "phi-" in self.model.lower():
            self.tokenizer = AutoTokenizer.from_pretrained(
                "microsoft/{}".format(self.model),
            )

            if "moe" in self.model.lower():
                self.generator = AutoModelForCausalLM.from_pretrained(
                    "microsoft/{}".format(self.model),
                    device_map="auto", 
                    torch_dtype="auto", 
                    trust_remote_code=True,
                    load_in_4bit=True,
                    bnb_4bit_compute_dtype=torch.bfloat16,
                )
            else:
                self.generator = AutoModelForCausalLM.from_pretrained(
                    "microsoft/{}".format(self.model),
                    device_map="auto", 
                    torch_dtype="auto", 
                    trust_remote_code=True,
                )
        else:
            raise ValueError("unsupprted model")

    def chat(self, system_prompt, user_prompt):
        if "deepseek" in self.model.lower():
            return self.chat_deepseek(system_prompt, user_prompt)
        elif "qwen" in self.model.lower() or "qwq" in self.model.lower():
            return self.chat_qwen(system_prompt, user_prompt)
        elif "llama" in self.model.lower():
            if "llama-3" in self.model.lower():
                return self.chat_llama_hf(system_prompt, user_prompt)
            else:
                return self.chat_llama(system_prompt, user_prompt)
        elif "vicuna" in self.model.lower():
            return self.chat_vicuna(system_prompt, user_prompt)
        elif "gemma" in self.model.lower():
            return self.chat_gemma(system_prompt, user_prompt)
        elif "mistral" in self.model.lower():
            return self.chat_mistral(system_prompt, user_prompt)
        elif "command" in self.model.lower():
            return self.chat_command(system_prompt, user_prompt)
        elif "phi" in self.model.lower():
            return self.chat_phi(system_prompt, user_prompt)

    def chat_llama(self, system_prompt, user_prompt):
        dialogs = [
            [
                {"role": "system", "content": f"Please respond to binary questions.\n\n{system_prompt}"},
                {"role": "user", "content": user_prompt},
            ],
        ]
        response = self.generator.chat_completion(
            dialogs,  # type: ignore
            max_gen_len=128,
            temperature=0.6,
            top_p=0.9,
        )

        return response[0]['generation']['content']
    
    def chat_llama_hf(self, system_prompt, user_prompt):
        prompt = f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\nPlease respond to binary questions.\n\n{system_prompt}<|eot_id|>\n<|start_header_id|>user<|end_header_id|>\n\n{user_prompt}<|eot_id|>\n<|start_header_id|>assistant<|end_header_id|>"
        
        token_ids = self.tokenizer.encode(prompt, add_special_tokens=False, return_tensors="pt")
        with torch.no_grad():
            output_ids = self.generator.generate(
                token_ids.to(self.generator.device),
                max_new_tokens=256,
                do_sample=True,
                temperature=0.6,
                top_p=0.9,
                pad_token_id=self.tokenizer.pad_token_id,
                bos_token_id=self.tokenizer.bos_token_id,
                eos_token_id=self.tokenizer.convert_tokens_to_ids("<|eot_id|>"),
            )
        response = self.tokenizer.decode(output_ids.tolist()[0][token_ids.size(1):])

        return str(response)

    def chat_deepseek(self, system_prompt, user_prompt):
        prompt = f"<｜begin▁of▁sentence｜>Please respond to binary questions. {system_prompt}<｜User｜>{user_prompt}<｜Assistant｜>"
        
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.generator.device)
        with torch.no_grad():
            output_ids = self.generator.generate(
                input_ids=inputs.input_ids,
                attention_mask=inputs.attention_mask,
                max_new_tokens=2048,
                do_sample=True,
                temperature=0.6,
                top_p=0.9,
                pad_token_id=self.tokenizer.pad_token_id,
                bos_token_id=self.tokenizer.bos_token_id,
                eos_token_id=self.tokenizer.convert_tokens_to_ids("<｜end▁of▁sentence｜>"),
            )
        response = self.tokenizer.decode(output_ids.tolist()[0][inputs.input_ids.size(1):])

        return str(response)

    def chat_qwen(self, system_prompt, user_prompt):
        if "qwen3" in self.model.lower():
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]

            text = self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True,
                enable_thinking=False
                # enable_thinking=True
            )

            model_inputs = self.tokenizer([text], return_tensors="pt").to(self.generator.device)

            # conduct text completion
            generated_ids = self.generator.generate(
                **model_inputs,
                max_new_tokens=32768
            )
            output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist()
            
            # parsing thinking content
            try:
                # rindex finding 151668 (</think>)
                index = len(output_ids) - output_ids[::-1].index(151668)
            except ValueError:
                index = 0

            thinking_content = self.tokenizer.decode(output_ids[:index], skip_special_tokens=True).strip("\n")
            content = self.tokenizer.decode(output_ids[index:], skip_special_tokens=True).strip("\n")

            response = str(thinking_content) + str(content)

        else:
            prompt = f"<|im_start|>system\nPlease respond to binary questions. {system_prompt}<|im_end|>\n\n<|im_start|>user\n{user_prompt}<|im_end|>\n\n<|im_start|>assistant"
            
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.generator.device)
            with torch.no_grad():
                output_ids = self.generator.generate(
                    input_ids=inputs.input_ids,
                    attention_mask=inputs.attention_mask,
                    max_new_tokens=2048,
                    do_sample=True,
                    temperature=0.6,
                    top_p=0.9,
                    pad_token_id=self.tokenizer.pad_token_id,
                    bos_token_id=self.tokenizer.bos_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                )
            response = self.tokenizer.decode(output_ids.tolist()[0][inputs.input_ids.size(1):])

        return str(response)

    def chat_vicuna(self, system_prompt, user_prompt):
        prompt = f"USER: Please respond to binary questions.\n\n{system_prompt}\n\n{user_prompt}\n\nASSISTANT:"
        
        token_ids = self.tokenizer.encode(prompt, add_special_tokens=False, return_tensors="pt")
        with torch.no_grad():
            output_ids = self.generator.generate(
                token_ids.to(self.generator.device),
                max_new_tokens=512,
                do_sample=True,
                temperature=0.7,
                top_p=1.0,
                pad_token_id=self.tokenizer.pad_token_id,
                bos_token_id=self.tokenizer.bos_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
            )
        response = self.tokenizer.decode(output_ids.tolist()[0][token_ids.size(1):])

        return str(response)

    def chat_gemma(self, system_prompt, user_prompt):
        prompt = f"<bos><start_of_turn>user\nPlease respond to binary questions.\n\n{system_prompt}\n\n{user_prompt}<end_of_turn>\n<start_of_turn>model\n"
        
        token_ids = self.tokenizer.encode(prompt, add_special_tokens=False, return_tensors="pt")
        with torch.no_grad():
            output_ids = self.generator.generate(
                token_ids.to(self.generator.device),
                max_new_tokens=512,
                do_sample=True,
                temperature=0.7,
                top_p=1.0,
                pad_token_id=self.tokenizer.pad_token_id,
                bos_token_id=self.tokenizer.bos_token_id,
                eos_token_id=self.tokenizer.convert_tokens_to_ids("<end_of_turn>"),
            )
        response = self.tokenizer.decode(output_ids.tolist()[0][token_ids.size(1):])

        return str(response)

    def chat_mistral(self, system_prompt, user_prompt):
        prompt = f"<s>[INST] Please respond to binary questions.\n\n{system_prompt}\n\n{user_prompt} [/INST]"

        token_ids = self.tokenizer.encode(prompt, add_special_tokens=False, return_tensors="pt")
        with torch.no_grad():
            output_ids = self.generator.generate(
                token_ids.to(self.generator.device),
                max_new_tokens=512,
                do_sample=True,
                temperature=0.7,
                top_p=1.0,
                pad_token_id=self.tokenizer.pad_token_id,
                bos_token_id=self.tokenizer.bos_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
            )
        response = self.tokenizer.decode(output_ids.tolist()[0][token_ids.size(1):])

        return str(response)

    def chat_command(self, system_prompt, user_prompt):
        prompt = f"<BOS_TOKEN><|START_OF_TURN_TOKEN|><|SYSTEM_TOKEN|>Please respond to binary questions.\n\n{system_prompt}<|END_OF_TURN_TOKEN|><|START_OF_TURN_TOKEN|><|USER_TOKEN|>{user_prompt}<|END_OF_TURN_TOKEN|><|START_OF_TURN_TOKEN|><|CHATBOT_TOKEN|>"

        token_ids = self.tokenizer.encode(prompt, add_special_tokens=False, return_tensors="pt")
        with torch.no_grad():
            output_ids = self.generator.generate(
                token_ids.to(self.generator.device),
                max_new_tokens=100,
                do_sample=True,
                temperature=0.3,
                top_p=1.0,
                pad_token_id=self.tokenizer.pad_token_id,
                bos_token_id=self.tokenizer.bos_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
            )
        response = self.tokenizer.decode(output_ids.tolist()[0][token_ids.size(1):])

        return str(response)
        
    def chat_phi(self, system_prompt, user_prompt):
        prompt = f"<|system|>\n{system_prompt}<|end|>\n<|user|>\n{user_prompt}<|end|>\n<|assistant|>"

        token_ids = self.tokenizer.encode(prompt, add_special_tokens=False, return_tensors="pt")
        with torch.no_grad():
            output_ids = self.generator.generate(
                token_ids.to(self.generator.device),
                max_new_tokens=100,
                do_sample=True,
                temperature=0.7,
                top_p=1.0,
                pad_token_id=self.tokenizer.pad_token_id,
                bos_token_id=self.tokenizer.bos_token_id,
                eos_token_id=self.tokenizer.convert_tokens_to_ids("<|end|>"),
            )
        response = self.tokenizer.decode(output_ids.tolist()[0][token_ids.size(1):])

        return str(response)

