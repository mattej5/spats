import os
from openai import OpenAI
import openai
from flask import Flask, request, jsonify, render_template_string

msg = ' '

def api_call(msg):
    if msg != ' ':
        my_thread_message = client.beta.threads.messages.create(
            thread_id=my_thread.id,
            role="user",
            content=msg
        )

        my_run = client.beta.threads.runs.create(
            thread_id=my_thread.id,
            assistant_id=existing_assistant_id,
            instructions=existing_assistant.instructions
        )
    # Step 5: Periodically retrieve the Run to check on its status to see if it has moved to completed
    while my_run.status in ["queued", "in_progress"]:
        keep_retrieving_run = client.beta.threads.runs.retrieve(
            thread_id=my_thread.id,
            run_id=my_run.id
        )
        print(f"Run status: {keep_retrieving_run.status}")

        if keep_retrieving_run.status == "completed":
            print("\n")

            # Step 6: Retrieve the Messages added by the Assistant to the Thread
            all_messages = client.beta.threads.messages.list(
                thread_id=my_thread.id
            )

            print("------------------------------------------------------------ \n")

            print(f"User: {my_thread_message.content[0].text.value}")
            print(f"Assistant: {all_messages.data[0].content[0].text.value}")
            collected_response = f"Assistant: {all_messages.data[0].content[0].text.value}"
            return collected_response
        
            break
        elif keep_retrieving_run.status == "queued" or keep_retrieving_run.status == "in_progress":
            pass
        else:
            print(f"Run status: {keep_retrieving_run.status}")
            break

    collected_response = "\nYour session with stu has ended. Have a nice day!"
    return collected_response

# Initialize the OpenAI client
OPEN_API_KEY = 'sk-proj-CkiPxLDIFbghr0xN41QbT3BlbkFJaY3ZgqaTVqyfOi1lYize'
client = openai.OpenAI(api_key='sk-proj-CkiPxLDIFbghr0xN41QbT3BlbkFJaY3ZgqaTVqyfOi1lYize')
openai.api_key = os.getenv(OPEN_API_KEY)# stored If not add your key
# Specify the ID of the existing assistant
existing_assistant_id = "asst_SqbWN63U0HtURb9teMwFK6Xs"

# Step 1: Retrieve the Existing Assistant
existing_assistant = client.beta.assistants.retrieve(existing_assistant_id)
# print(f"This is the existing assistant object: {existing_assistant} \n")

# Step 2: Create a Thread
my_thread = client.beta.threads.create()
# print(f"This is the thread object: {my_thread} \n")

# Step 3: Add a Message to a Thread
my_thread_message = client.beta.threads.messages.create(
  thread_id=my_thread.id,
  role="user",
  content="Ask for my name, then ask me if I want to create a four-year plan, create a semester plan, ask about specific professors, or discover more about a major.",
)
# print(f"This is the message object: {my_thread_message} \n")

# Step 4: Run the Assistant
my_run = client.beta.threads.runs.create(
  thread_id=my_thread.id,
  assistant_id=existing_assistant_id,
  instructions=existing_assistant.instructions
)
# print(f"This is the run object: {my_run} \n")

app = Flask(__name__)

@app.route("/")
def index():
    return render_template_string(open('index.html').read())

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    msg = data.get('message')
    response = api_call(msg)
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)


    # while msg != "":
    #     if msg != ' ':
    #         my_thread_message = client.beta.threads.messages.create(
    #             thread_id=my_thread.id,
    #             role="user",
    #             content=msg
    #         )

    #         my_run = client.beta.threads.runs.create(
    #             thread_id=my_thread.id,
    #             assistant_id=existing_assistant_id,
    #             instructions=existing_assistant.instructions
    #         )
    #     # Step 5: Periodically retrieve the Run to check on its status to see if it has moved to completed
    #     while my_run.status in ["queued", "in_progress"]:
    #         keep_retrieving_run = client.beta.threads.runs.retrieve(
    #             thread_id=my_thread.id,
    #             run_id=my_run.id
    #         )
    #         print(f"Run status: {keep_retrieving_run.status}")

    #         if keep_retrieving_run.status == "completed":
    #             print("\n")

    #             # Step 6: Retrieve the Messages added by the Assistant to the Thread
    #             all_messages = client.beta.threads.messages.list(
    #                 thread_id=my_thread.id
    #             )

    #             print("------------------------------------------------------------ \n")

    #             print(f"User: {my_thread_message.content[0].text.value}")
    #             print(f"Assistant: {all_messages.data[0].content[0].text.value}")
    #             collected_response = f"------------------------------------------------------------ \nUser: {my_thread_message.content[0].text.value}\nAssistant: {all_messages.data[0].content[0].text.value}"
    #             return collected_response
            
    #             break
    #         elif keep_retrieving_run.status == "queued" or keep_retrieving_run.status == "in_progress":
    #             pass
    #         else:
    #             print(f"Run status: {keep_retrieving_run.status}")
    #             break

    # collected_response = "\nYour session with stu has ended. Have a nice day!"
    # print("\nYour session with stu has ended. Have a nice day!")