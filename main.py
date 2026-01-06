from google import genai
import os 
from dotenv import load_dotenv
import argparse


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt",type=str,help="User prompt")
    args = parser.parse_args()
    generate_content = client.models.generate_content(model="gemini-2.5-flash",contents=args.user_prompt)
    if not generate_content.usage_metadata:
        raise RuntimeError("Gemini API response appears t obe malformed")
    print("Prompt tokens: ",generate_content.usage_metadata.prompt_token_count)
    print("Response tokens: ",generate_content.usage_metadata.candidates_token_count)
    print("Response:\n",generate_content.text)

if __name__ == "__main__":
    main()
