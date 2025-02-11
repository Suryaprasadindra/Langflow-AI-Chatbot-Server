import argparse
import json
from argparse import RawTextHelpFormatter
import requests
from typing import Optional
import warnings
try:
    from langflow.load import upload_file
except ImportError:
    warnings.warn("Langflow provides a function to help you upload files to the flow. Please install langflow to use it.")
    upload_file = None

BASE_API_URL = "http://127.0.0.1:7860"
FLOW_ID = "bbd9407a-0100-4cc8-9e10-2c7d2e0276f2"
ENDPOINT = "" # You can set a specific endpoint name in the flow settings

# You can tweak the flow by adding a tweaks dictionary
# e.g {"OpenAI-XXXXX": {"model_name": "gpt-4"}}
TWEAKS = {
  "ChatInput-O9DAr": {},
  "ParseData-t6MMJ": {},
  "Prompt-5RXrM": {},
  "SplitText-M2E8s": {},
  "ChatOutput-ON9dP": {},
  "OpenAIEmbeddings-bzPTk": {},
  "OpenAIEmbeddings-tXQih": {},
  "File-wx38s": {},
  "OpenAIModel-G9jv2": {},
  "Chroma-7B3wH": {},
  "Chroma-M0ziZ": {},
  "AstraDB-YMTBR": {}
}

def run_flow(message: str,
  output_type: str = "chat",
  input_type: str = "chat",
  tweaks: Optional[dict] = None,
  api_key: Optional[str] = None) -> dict:
    """
    Run a flow with a given message and optional tweaks.

    :param message: The message to send to the flow
    :param endpoint: The ID or the endpoint name of the flow
    :param tweaks: Optional tweaks to customize the flow
    :return: The JSON response from the flow
    """
    api_url = f"{BASE_API_URL}/api/v1/run/{FLOW_ID}"

    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }
    headers = None
    if tweaks:
        payload["tweaks"] = tweaks
    if api_key:
        headers = {"x-api-key": api_key}

    try:
        response = requests.post(api_url, json=payload, headers=headers)
    except requests.exceptions.RequestException as e:
        return 500

    return response