from typing import Tuple, List, Dict, Any
from constants import model_params
import google.generativeai as genai
import json


class Gemini:
    def __init__(self, api_key: str) -> None:
        genai.configure(api_key=api_key)

    def get_xpath(self, rawHtml, element) -> Dict:
        xpath = model_params["xpath"]
        model = genai.GenerativeModel(
            model_name=xpath["model_name"], generation_config=xpath["generation_config"])
        response = model.generate_content(
            xpath["prompt"](rawHtml, element)).text
        return json.loads(response)
