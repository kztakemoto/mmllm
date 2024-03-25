import time

import vertexai
from vertexai.preview.generative_models import GenerativeModel
from vertexai.preview.language_models import ChatModel

# for ChatGPT
import openai
openai.api_key = "ENTER YOUR OPENAI API KEY"

# for Claude
import anthropic
client = anthropic.Anthropic(
            api_key="ENTER YOUR ANTHROPIC API KEY",
        )

# for PaLM and Gemini
vertexai.init(project="ENTER YOUR PROJECT NAME", location="ENTER YOUR LOCATION")

class ChatBotManager:
    def __init__(self, model, max_attempts=20):
        self.model = model
        self.max_attempts = max_attempts
                
        if "gemini" in self.model.lower():
            self.chat_model = GenerativeModel("gemini-1.0-pro-001")
        elif "palm" in self.model.lower():
            self.chat_model = ChatModel.from_pretrained("chat-bison@001")

    def chat(self, system_prompt, user_prompt):
        if "gpt" in self.model.lower():
            return self.chat_gpt(system_prompt, user_prompt)
        elif "gemini" in self.model.lower():
            return self.chat_gemini(system_prompt, user_prompt)
        elif "palm" in self.model.lower():
            return self.chat_palm(system_prompt, user_prompt)
        elif "claude" in self.model.lower():
            return self.chat_claude(system_prompt, user_prompt)

    def chat_gpt(self, system_prompt, user_prompt):
        attempt = 0
        while attempt < self.max_attempts:
            try:
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages = [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}
                        ],
                )
                response_text = response['choices'][0]['message']['content']
                
                return response_text

            except openai.error.OpenAIError as e:
                time.sleep(5)
                attempt = attempt + 1
        
        return None
    
    def chat_claude(self, system_prompt, user_prompt):
        attempt = 0
        while attempt < self.max_attempts:
            try:
                time.sleep(1)
                response = client.messages.create(
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
