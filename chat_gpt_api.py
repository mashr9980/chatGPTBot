import openai
import os

class ChatGPTBotAPI:
    def __init__(self, api_key, prompts_file_path):
        self.api_key = api_key
        self.prompts_file_path = prompts_file_path
        self.load_prompts_from_file()

    def initialize_gpt3(self):
        openai.api_key = self.api_key

    def load_prompts_from_file(self):
        self.prompts = []
        if os.path.exists(self.prompts_file_path):
            with open(self.prompts_file_path, "r") as file:
                for line in file:
                    prompt_response = line.strip().split("|")
                    if len(prompt_response) == 2:
                        prompt, response = prompt_response
                        self.prompts.append({"prompt": prompt, "response": response})

    def save_prompts_to_file(self):
        with open(self.prompts_file_path, "w") as file:
            for prompt in self.prompts:
                file.write(f"Question: {prompt['prompt']} | Response: {prompt['response']}\n")

    def create_prompt(self, prompt):
        response = self.get_response_for_prompt(prompt)
        self.prompts.append({"prompt": prompt, "response": response})
        self.save_prompts_to_file()
        return len(self.prompts) - 1  

    def read_prompt(self, prompt_index):
        if prompt_index < 0 or prompt_index >= len(self.prompts):
            return {"error": "Invalid prompt index."}

        return self.prompts[prompt_index]

    def update_prompt(self, prompt_index, new_prompt):
        if prompt_index < 0 or prompt_index >= len(self.prompts):
            return {"error": "Invalid prompt index."}

        response = self.get_response_for_prompt(new_prompt)
        self.prompts[prompt_index] = {"prompt": new_prompt, "response": response}
        self.save_prompts_to_file()
        return {"result": "Prompt updated successfully."}

    def delete_prompt(self, prompt_index):
        if prompt_index < 0 or prompt_index >= len(self.prompts):
            return {"error": "Invalid prompt index."}

        del self.prompts[prompt_index]
        self.save_prompts_to_file()
        return {"result": "Prompt deleted successfully."}

    def get_response_for_prompt(self, prompt):
        response = openai.Completion.create(
            engine="text-davinci-001",  
            prompt=prompt,
            max_tokens=250,  
        )
        return response.choices[0].text.strip()
