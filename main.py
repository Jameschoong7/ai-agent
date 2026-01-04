from google import genai
import os 
from dotenv import load_dotenv


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


def main():
    print("Hello from ai-agent!")
    generate_content = client.models.generate_content(model="gemini-2.5-flash",contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.")
    print(generate_content.text)

if __name__ == "__main__":
    main()
