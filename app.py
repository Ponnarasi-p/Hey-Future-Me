from flask import Flask, render_template, request
from dotenv import load_dotenv
from openai import OpenAI
import os

# Load environment variables
load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

app = Flask(__name__)

def generate_career_guidance(user_input):
    prompt = f"""
    The user provided the following background:
    "{user_input}"

    Based on this, provide:
    - Best career path(s)
    - Year-wise learning goals (3 years)
    - Internship or project suggestions
    - Job preparation resources
    """
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "You are a career coach helping students choose the right path."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"❌ Error: {str(e)}"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/result", methods=["POST"])
def result():
    user_input = request.form["user_input"]
    output = generate_career_guidance(user_input)
    return render_template("result.html", suggestion=output)

if __name__ == "__main__":
    app.run(debug=True)
