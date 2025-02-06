import time

import vertexai
from vertexai.generative_models import GenerativeModel
from vertexai.preview.language_models import ChatModel
import google.generativeai as genai

import openai
import anthropic

# for PaLM and Gemini
vertexai.init(project="ENTER YOUR PROJECT NAME", location="ENTER YOUR LOCATION")

class ChatBotManager:
    def __init__(self, model, max_attempts=20):
        self.model = model
        self.max_attempts = max_attempts
                
        if "gemini" in self.model.lower():
            if "2.0" in self.model.lower():
                genai.configure(api_key="ENTER YOUR GOOGLE AI STUDIO API KEY")
                self.chat_model = genai.GenerativeModel(model_name = self.model)
            else:
                self.chat_model = GenerativeModel(self.model)
        elif "palm" in self.model.lower():
            self.chat_model = ChatModel.from_pretrained("chat-bison@001")
        elif any(s.lower() in self.model.lower() for s in ["gpt", "o1", "o3"]):
            self.chat_model = openai.OpenAI(api_key="ENTER YOUR OPENAI API KEY")
        elif "claude" in self.model.lower():
            self.chat_model = anthropic.Anthropic(api_key="ENTER YOUR ANTHROPIC API KEY")
        elif "deepseek" in self.model.lower():
            self.chat_model = openai.OpenAI(api_key="ENTER YOUR DEEPSEEK API KEY", base_url="https://api.deepseek.com")

    def chat(self, system_prompt, user_prompt):
        if "gpt" in self.model.lower() or "o3" in self.model.lower():
            return self.chat_gpt(system_prompt, user_prompt)
        elif "o1" in self.model.lower():
            return self.chat_o1(system_prompt, user_prompt)
        elif "gemini" in self.model.lower():
            if "2.0" in self.model.lower():
                return self.chat_gemini2(system_prompt, user_prompt)
            else:
                return self.chat_gemini(system_prompt, user_prompt)
        elif "palm" in self.model.lower():
            return self.chat_palm(system_prompt, user_prompt)
        elif "claude" in self.model.lower():
            return self.chat_claude(system_prompt, user_prompt)
        elif "deepseek" in self.model.lower():
            return self.chat_gpt(system_prompt, user_prompt)

    def chat_gpt(self, system_prompt, user_prompt):
        attempt = 0
        while attempt < self.max_attempts:
            try:
                response = self.chat_model.chat.completions.create(
                    model=self.model,
                    messages = [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}
                        ],
                )
                response_text = response.choices[0].message.content
                
                return response_text

            except Exception as e:
                time.sleep(5)
                attempt = attempt + 1
        
        return None
                
    def chat_o1(self, system_prompt, user_prompt):
        attempt = 0
        while attempt < self.max_attempts:
            try:
                response = self.chat_model.chat.completions.create(
                    model=self.model,
                    messages = [
                            {"role": "user", "content": f"{system_prompt}\n\n{user_prompt}"}
                        ],
                )
                response_text = response.choices[0].message.content
                
                return response_text

            except Exception as e:
                time.sleep(5)
                attempt = attempt + 1
        
        return None
    
    def chat_claude(self, system_prompt, user_prompt):
        attempt = 0
        while attempt < self.max_attempts:
            try:
                time.sleep(1)
                response = self.chat_model.messages.create(
                    model=self.model,
                    max_tokens=1000,
                    temperature=0,
                    system=system_prompt,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": user_prompt
                                }
                            ]
                        }
                    ]
                )
                response_text = response.content[0].text
                
                return response_text

            except Exception as e:
                attempt = attempt + 1
                if "rate_limit_error" in str(e):
                    raise ValueError("rate limit error")
                else:
                    print(str(e))
                    time.sleep(5)
        
        return None
    
    def chat_gemini(self, system_prompt, user_prompt):
        chat = self.chat_model.start_chat()
        attempt = 0
        while attempt < self.max_attempts:
            try:
                prompt = f"{system_prompt}\n\n" + user_prompt 
                if "1.5" in self.model.lower():
                    response = chat.send_message(
                            prompt,
                            generation_config = {
                                "max_output_tokens": 8192,
                                "temperature": 1,
                                "top_p": 0.95,
                            },
                            )
                    time.sleep(15)
                else:
                    response = chat.send_message(
                            prompt,
                            generation_config = {
                                "max_output_tokens": 2048,
                                "temperature": 0.9,
                                "top_p": 1
                            },
                            )

                response_text = response.candidates[0].content.parts[0].text
                
                return response_text

            except vertexai.generative_models._generative_models.ResponseBlockedError as e:
                print(str(e))
                attempt = attempt + 1
            
            except Exception as e:
                print(str(e))
                time.sleep(5)
                attempt = attempt + 1
        
        return None

    def chat_gemini2(self, system_prompt, user_prompt):
        attempt = 0
        while attempt < self.max_attempts:
            try:
                prompt = f"{system_prompt}\n\n" + user_prompt 
                response = self.chat_model.generate_content(
                    prompt,
                )
                time.sleep(6)

                return response.text

            except Exception as e:
                print(str(e))
                time.sleep(5)
                attempt = attempt + 1
        
        return None

    def chat_palm(self, system_prompt, user_prompt):
        chat = self.chat_model.start_chat(context=system_prompt)
        attempt = 0
        while attempt < self.max_attempts:
            try:
                response = chat.send_message(user_prompt, **{
                            "temperature": 0.2,
                            "max_output_tokens": 256,
                            "top_p": 0.8,
                            "top_k": 40,
                })

                response_text = response.text
                
                return response_text

            except vertexai.generative_models._generative_models.ResponseBlockedError as e:
                print(str(e))
                attempt = attempt + 1
            
            except Exception as e:
                print(str(e))
                time.sleep(5)
                attempt = attempt + 1
        
        return None
