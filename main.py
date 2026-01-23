from google import genai
import os 
from dotenv import load_dotenv
from prompts import system_prompt
from google.genai import types
import argparse
from call_function import available_functions,call_function


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt",type=str,help="User prompt")
    parser.add_argument("--verbose",action="store_true",help="Enable verbose output")
    args = parser.parse_args()
    messages = [types.Content(role="user",parts=[types.Part(text=args.user_prompt)])]
    generate_content = client.models.generate_content(model="gemini-2.5-flash",contents=messages,config=types.GenerateContentConfig(tools=[available_functions],system_instruction=system_prompt,temperature=0))
    if not generate_content.usage_metadata:
        raise RuntimeError("Gemini API response appears t obe malformed")
    function_calls = generate_content.function_calls
    if args.verbose:
        print("User prompt: ",args.user_prompt)
        print("Prompt tokens: ",generate_content.usage_metadata.prompt_token_count)
        print("Response tokens: ",generate_content.usage_metadata.candidates_token_count)
    
    
    if function_calls is not None:
        
        for function_call in function_calls:
            #print(f"Calling function: {function_call.name}({function_call.args})")
            function_call_result = call_function(function_call)
            if len(function_call_result.parts)<=0:
                raise Exception()
            if function_call_result.parts[0].function_response is None:
                raise Exception ()
            if function_call_result.parts[0].function_response.response is None:
                raise Exception()
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
                
    else:
        print("Response:\n",generate_content.text)


if __name__ == "__main__":
    main()
