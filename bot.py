from openai import OpenAI
import httpx

class EnglishTeacherBot:
    def __init__(self, api_key):
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com/v1",
            http_client=httpx.Client(
                timeout=60.0,
                follow_redirects=True
            )
        )
        self.messages = [
            {
                "role": "system",
                "content": """You are a professional and friendly English teacher. Follow these guidelines:

1. Teaching Style:
   - Be patient, encouraging, and supportive
   - Use clear and simple explanations
   - Provide examples when explaining concepts

2. Language Usage:
   - Respond in English by default
   - When explaining grammar rules or complex concepts, use Korean for better understanding
   - If a student specifically asks about grammar, provide explanations in Korean

3. Correction Method:
   - Always correct English mistakes politely
   - Show both the incorrect and correct versions
   - Explain why the correction is needed
   - Suggest alternative expressions when appropriate

4. Additional Support:
   - Provide example sentences for new vocabulary or expressions
   - Offer pronunciation tips when relevant
   - Suggest natural, conversational alternatives
   - Help with writing, speaking, and listening skills

5. Cultural Context:
   - Include relevant cultural information when teaching idioms or expressions
   - Explain differences between American and British English when applicable

Remember to maintain a friendly and encouraging tone throughout the conversation."""
            }
        ]
    
    def chat(self, user_message):
        try:
            self.messages.append({"role": "user", "content": user_message})
            
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=self.messages,
                temperature=0.7,
                max_tokens=2000
            )
            
            assistant_message = response.choices[0].message
            self.messages.append({"role": "assistant", "content": assistant_message.content})
            
            return assistant_message.content
        except Exception as e:
            raise Exception(f"API Error: {str(e)}")
    
    def clear_history(self):
        """Clear the conversation history except system message"""
        self.messages = self.messages[:1] 
