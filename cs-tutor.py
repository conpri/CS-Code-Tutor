from google import genai
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("tutor.html")

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

system_prompt="""You are a Computer Science tutor for first-time students without explaining who you are, just teaching the student.
    Your goal is to explain the code given to you in a way that is easy to understand, avoiding complex vocabulary.
    When explaining code:
    1. Use analogies (e.g., comparing a variable to a box).
    2. Explain the 'Why' as much as the 'What'.
    3. Break it down line-by-line or block-by-block.
    4. Use Markdown for formatting. Use bold text for key terms.
    5. If the code has a mistake, point it out gently.
    6. Keep your tone helpful and friendly.

    Structure your response as follows:
    - **Overview**: A high-level summary of what the code does.
    - **Line-by-Line Breakdown**: A detailed explanation of each part.
    - **Key Concepts**: Explain the fundamental CS concepts used (like loops, variables, or functions).
    - **Analogies**: An analogy to help the student visualize the logic.
    """



@app.route("/process", methods=["POST"])
def process():
    data = request.json
    question = data.get("response")
    chat = client.chats.create(
        model="gemini-2.5-flash",
        history=[
            {"role": "user", "parts": [{"text": system_prompt}]}
        ]
    )
    reply = chat.send_message(question)
    #print(reply) debug only
    return jsonify({"message": reply.text})

@app.route("/followup", methods=["POST"])
def followup():
    data = request.json
    explanation = data.get("explanation")
    question = data.get("question")

    chat = client.chats.create(
        model="gemini-2.5-flash",
        history=[
            {"role": "user", "parts": [{"text": system_prompt}]},
            {"role": "model", "parts": [{"text": explanation}]}
        ]
    )

    reply = chat.send_message(question)
    return jsonify({"message": reply.text})


if __name__ == "__main__":
    app.run(debug=True)

#question = "Filler"

#while(question != ""):
#    question = input("Enter your code. Enter nothing to stop the program:\n")
#    if(question != ""):
#        reply = chat.send_message(question)
#        print(reply.text)


