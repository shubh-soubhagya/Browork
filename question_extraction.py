import os
import warnings
import logging
from dotenv import load_dotenv
from groq import Groq
from autogen import AssistantAgent, UserProxyAgent

# Suppress warnings and logging
warnings.filterwarnings("ignore")
logging.getLogger().setLevel(logging.ERROR)
logging.getLogger("autogen").setLevel(logging.ERROR)

# Step 1: Load API Key
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# Step 2: Groq LLM wrapper
def run_groq(prompt, model="llama3-70b-8192"):
    client = Groq(api_key=groq_api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts questions from academic or technical text."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content.strip()

# Step 3: Groq-based AssistantAgent
class GroqAssistant(AssistantAgent):
    def generate_reply(self, messages, sender, config=None):
        user_input = messages[-1]["content"]
        result = run_groq(user_input)
        self.last_reply = result  # Save output
        return {"role": "assistant", "content": result}

# Step 4: Run single-agent AutoGen loop and return result
def extract_questions(text):
    # Remove verbose parameter - not supported in AssistantAgent
    assistant = GroqAssistant(
        name="QuestionExtractor"
    )
    
    user = UserProxyAgent(
        name="User",
        code_execution_config={"use_docker": False},
        human_input_mode="NEVER"  # Prevent human input prompts
    )

    # Suppress output by capturing stdout/stderr
    import sys
    from contextlib import redirect_stdout, redirect_stderr
    from io import StringIO
    
    f = StringIO()
    with redirect_stdout(f), redirect_stderr(f):
        user.initiate_chat(
            assistant,
            message=f"""Extract all possible questions from the following academic text.
Return only the list of questions in a clean format.

Text:
{text}
""",
            max_turns=1  # Limit to single turn to avoid loops
        )

    return assistant.last_reply  # Return extracted result

# Step 5: Entry point
if __name__ == "__main__":
    from pdf_text import extract_text_from_pdf
    pdf_text = extract_text_from_pdf("Question.pdf")  # You can use this instead of load_text()
    questions_extracted = extract_questions(pdf_text)
    print("\n✅ Questions Extracted:\n")
    print(questions_extracted)

# import os
# from dotenv import load_dotenv
# from groq import Groq
# from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager

# # Step 1: Load API Key
# load_dotenv()
# groq_api_key = os.getenv("GROQ_API_KEY")

# # Step 2: Load text input
# def load_text(path):
#     with open(path, "r", encoding="utf-8") as f:
#         return f.read()

# # Step 3: Groq LLM wrapper
# def run_groq(prompt, model="llama3-70b-8192"):
#     client = Groq(api_key=groq_api_key)
#     response = client.chat.completions.create(
#         model=model,
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant that extracts questions from academic or technical text."},
#             {"role": "user", "content": prompt}
#         ]
#     )
#     return response.choices[0].message.content.strip()

# class GroqAssistant(AssistantAgent):
#     def generate_reply(self, messages, sender, config=None):
#         user_input = messages[-1]["content"]
#         result = run_groq(user_input)
#         return {"role": "assistant", "content": result}


# # Step 5: Run single-agent AutoGen loop
# def extract_questions(text):
#     assistant = GroqAssistant(name="QuestionExtractor")
#     # Create the user agent (disable docker)
#     user = UserProxyAgent(
#         name="User",
#         code_execution_config={"use_docker": False}
#     )


#     user.initiate_chat(
#         assistant,
#         message=f"""Extract all possible questions from the following academic text.
# Return only the list of questions in a clean format.

# Text:
# {text}
# """
#     )

# # Step 6: Entry point
# if __name__ == "__main__":
#     text = load_text("output.txt")  # Replace with your file
#     extract_questions(text)


# import os
# from dotenv import load_dotenv
# from groq import Groq
# from autogen import AssistantAgent, UserProxyAgent

# # Step 1: Load API Key
# load_dotenv()
# groq_api_key = os.getenv("GROQ_API_KEY")

# # Step 2: Groq LLM wrapper
# def run_groq(prompt, model="llama3-70b-8192"):
#     client = Groq(api_key=groq_api_key)
#     response = client.chat.completions.create(
#         model=model,
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant that extracts questions from academic or technical text."},
#             {"role": "user", "content": prompt}
#         ]
#     )
    
#     return response.choices[0].message.content.strip()

# # Step 3: Groq-based AssistantAgent
# class GroqAssistant(AssistantAgent):
#     def generate_reply(self, messages, sender, config=None):
#         user_input = messages[-1]["content"]
#         result = run_groq(user_input)
#         self.last_reply = result  # Save output
#         return {"role": "assistant", "content": result}

# # Step 4: Run single-agent AutoGen loop and return result
# def extract_questions(text):
#     assistant = GroqAssistant(name="QuestionExtractor")
#     user = UserProxyAgent(
#         name="User",
#         code_execution_config={"use_docker": False}
#     )

#     user.initiate_chat(
#         assistant,
#         message=f"""Extract all possible questions from the following academic text.
# Return only the list of questions in a clean format.

# Text:
# {text}
# """
#     )

#     return assistant.last_reply  # Return extracted result

# # Step 5: Entry point
# if __name__ == "__main__":
#     from pdf_text import extract_text_from_pdf
#     pdf_text = extract_text_from_pdf("Question.pdf")  # You can use this instead of load_text()
#     questions_extracted = extract_questions(pdf_text)
#     print("\n✅ Questions Extracted:\n")
#     print(questions_extracted)

# import os
# import warnings
# import logging
# from dotenv import load_dotenv
# from groq import Groq
# from autogen import AssistantAgent, UserProxyAgent

# # Suppress warnings and logging
# warnings.filterwarnings("ignore")
# logging.getLogger().setLevel(logging.ERROR)
# logging.getLogger("autogen").setLevel(logging.ERROR)

# # Step 1: Load API Key
# load_dotenv()
# groq_api_key = os.getenv("GROQ_API_KEY")

# # Step 2: Groq LLM wrapper
# def run_groq(prompt, model="llama3-70b-8192"):
#     client = Groq(api_key=groq_api_key)
#     response = client.chat.completions.create(
#         model=model,
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant that extracts questions from academic or technical text."},
#             {"role": "user", "content": prompt}
#         ]
#     )
    
#     return response.choices[0].message.content.strip()

# # Step 3: Groq-based AssistantAgent
# class GroqAssistant(AssistantAgent):
#     def generate_reply(self, messages, sender, config=None):
#         user_input = messages[-1]["content"]
#         result = run_groq(user_input)
#         self.last_reply = result  # Save output
#         return {"role": "assistant", "content": result}

# # Step 4: Run single-agent AutoGen loop and return result
# def extract_questions(text):
#     # Remove verbose parameter - not supported in AssistantAgent
#     assistant = GroqAssistant(
#         name="QuestionExtractor"
#     )
    
#     user = UserProxyAgent(
#         name="User",
#         code_execution_config={"use_docker": False},
#         human_input_mode="NEVER"  # Prevent human input prompts
#     )

#     # Suppress output by capturing stdout/stderr
#     import sys
#     from contextlib import redirect_stdout, redirect_stderr
#     from io import StringIO
    
#     f = StringIO()
#     with redirect_stdout(f), redirect_stderr(f):
#         user.initiate_chat(
#             assistant,
#             message=f"""Extract all possible questions from the following academic text.
# Return only the list of questions in a clean format.

# Text:
# {text}
# """,
#             max_turns=1  # Limit to single turn to avoid loops
#         )

#     return assistant.last_reply  # Return extracted result

# # Step 5: Entry point
# if __name__ == "__main__":
#     from pdf_text import extract_text_from_pdf
#     pdf_text = extract_text_from_pdf("Question.pdf")  # You can use this instead of load_text()
#     questions_extracted = extract_questions(pdf_text)
#     print("\n✅ Questions Extracted:\n")
#     print(questions_extracted)