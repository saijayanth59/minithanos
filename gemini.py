import google.generativeai as genai

genai.configure(api_key="AIzaSyA7SbKNMH1FWqgu232oTEAzjg_yisa4bWw")

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-2.0-flash",
  generation_config=generation_config,
  system_instruction="Generate short responses. Don't use emojis.",
)
