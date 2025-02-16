from groq import Groq
from json import load, dump
import datetime
from dotenv import dotenv_values

env_vars = dotenv_values(".env")

Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")


client = Groq(api_key=GroqAPIKey)

messages = []

System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
*** Say you can make by {Username} and do not mention the name of the model. ***
*** You Invented in year 2025 and you are the most advanced AI chatbot. ***
*** expalin your Author and how to contact your author. ***
*** tell about your author birthdate and birthplace bithdate=23.07.2004 and birth place= jabalpur ***
*** tell about your author education and his profession he is Btech In Computer Science. ***
*** If any one ask about your author, tell them that he is a Btech student in Computer Science from Oriental Institute of science and Technology ,Jabalpur. ***
*** You can Knowldege about the world and you can answer any question. ***
*** you can also provide the information about the world. ***
*** You can Knowldege about more Ai assistant like ChatGPT, GPT-3, Jarvis, etc. ***
*** if any one ask you can Trained your self with there data. ***
*** give small answer and understanding words. ***
"""
SystemChatBot = [
    {"role": "system", "content": System}
]

try:
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)
except FileNotFoundError:
    
    with open(r"Data\ChatLog.json", "w") as f:
        dump([], f)    


def RealtimeInformation():
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")    
    year = current_date_time.strftime("%Y") 
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")

    data = f"Please use this realtime information if needed,\n"
    data += f"Day: {day}\nDate:{date}\nMonth:{month}\nYear:{year}\n"
    data += f"Time: {hour} hours:{minute} minutes:{second} seconds.\n"
    return data

def AnswerModifier(Answer):
    lines = Answer.split("\n")
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

def ChatBot(Query):
    """This function sends the user's query to the chatbot and return the AI's response."""

    try:
        with open(r"Data\ChatLog.json", "r") as f:
            messages = load(f)

        messages.append({"role": "user", "content": f"{Query}"})

        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=SystemChatBot + [{"role": "system", "content": RealtimeInformation()}] + messages,
            max_tokens=1024,
            temperature=0.5,
            top_p=1,
            stream=True,
            stop=None,
        )

        Answer = ""

        for chunk in completion:
            if chunk.choices[0].delta.content:
                 Answer += chunk.choices[0].delta.content

        Answer = Answer.replace("</s>", "")

        messages.append({"role": "assistant", "content": Answer})

        with open(r"Data\ChatLog.json", "w") as f:
            dump(messages, f, indent=4)

        return AnswerModifier(Answer=Answer)
    except Exception as e:

        print("Error: {e}")
        with open(r"Data\ChatLog.json", "w") as f:
            dump(messages, f, indent=4)
        return ChatBot(Query)

if __name__ == "__main__":
    while True:
        user_input = input("Enter Your Question: ")
        print(ChatBot(user_input))