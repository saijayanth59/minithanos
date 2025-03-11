from google import genai
from google.genai import types
from .client import client

def generate(prompt):
    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""Your sole task is to write code. Let's start"""),
            ],
        ),
        types.Content(
            role="model",
            parts=[
                types.Part.from_text(text="""{
  \"code\": \"def hello():\\n    print(\\\"Hello, world!\\\")\\n\\nhello()\\n\"
}"""),
            ],
        ),
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""Write code to generate fibonacci numbers using python and top down dp"""),
            ],
        ),
        types.Content(
            role="model",
            parts=[
                types.Part.from_text(text="""{
  \"code\": \"def fibonacci_top_down(n, memo):\\n    if n <= 1:\\n        return n\\n    if n in memo:\\n        return memo[n]\\n    memo[n] = fibonacci_top_down(n-1, memo) + fibonacci_top_down(n-2, memo)\\n    return memo[n]\\n\\n\\ndef fibonacci(n):\\n    memo = {}\\n    return fibonacci_top_down(n, memo)\\n\\n# Example usage:\\nn = 10\\nprint(fibonacci(n)) # Output: 55\\n\"
}"""),
            ],
        ),
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        top_k=40,
        max_output_tokens=8192,
        response_mime_type="application/json",
        response_schema=genai.types.Schema(
            type = genai.types.Type.OBJECT,
            required = ["code"],
            properties = {
                "code": genai.types.Schema(
                    type = genai.types.Type.STRING,
                ),
            },
        ),
        system_instruction=[
            types.Part.from_text(text="""Output only the code. no formatting. nothing else except the code"""),
        ],
    )

    return client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config,
    )

if __name__ == "__main__":
    generate()