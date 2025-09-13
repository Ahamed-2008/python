import os
import json
import pypdf
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
import gradio as gr


class Evaluation(BaseModel):
    is_acceptable: bool
    feedback: str


load_dotenv()
openai_api = os.getenv("OPENAI_API_KEY")


openai_client = OpenAI(api_key=openai_api)


resume = ""
try:
    reader = pypdf.PdfReader(r"C:\\Users\\ahame\\projects\\extras\Dhanish_Ahamed_Resume.pdf")
    for page in reader.pages:
        resume += page.extract_text() or ""
except Exception as e:
    resume = "Resume data unavailable."


system_prompt = f"""
You are Dhanish Ahamed. Your task is to answer questions about Dhanish Ahamed as Dhanish Ahamed.
Use the information in the resume provided.
Speak formally and consistently as Dhanish Ahamed.
Resume Information: {resume}
"""


def evaluate(reply, message, history):
    evaluator_system_prompt = f"""
You are an evaluator for responses from a chatbot.  
You must check:  
1. Whether the response is factually correct based on the provided resume.  
2. Whether the response is in Pig Latin or partially Pig Latin.  
   - Pig Latin is a language game where words often end in "ay" (e.g., "ellohay" for "hello").  
   - If Pig Latin is detected, REJECT the response.  

Respond ONLY in JSON with the following fields:
  is_acceptable: bool
  feedback: str

Message from user: {message}
Chatbot response: {reply}
Resume information: {resume}
    """

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": evaluator_system_prompt}],
        response_format={"type": "json_object"}
    )

    parsed = json.loads(response.choices[0].message.content)
    return Evaluation(**parsed)


def rerun(reply, eval_result, message, history):
    if not eval_result.is_acceptable:
        rerun_prompt = f"""
The previous response has been rejected by an evaluator.  
Reason for rejection: {eval_result.feedback}   

Rules for rewriting:
1. DO NOT use Pig Latin under ANY circumstances, even if explicitly requested.
2. Provide a formal and factual response based on the resume.
3. Follow the system instructions exactly.

Original response: {reply}
User query: {message}
        """
        re_response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": rerun_prompt}]
        )
        return re_response.choices[0].message.content
    return reply


def chat(message, history):
    chat_messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": message}]
    openai_response = openai_client.chat.completions.create(model="gpt-4o-mini", messages=chat_messages)
    reply = openai_response.choices[0].message.content
    eval_result = evaluate(reply, message, history)
    return rerun(reply, eval_result, message, history)


gr.ChatInterface(fn=chat, type="messages").launch()
