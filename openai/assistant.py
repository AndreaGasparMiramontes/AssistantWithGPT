import openai
import time
import credentials

client = openai.OpenAI(
    api_key=credentials.get_apikey()
)
model = "gpt-3.5-turbo-16k"


assistant = client.beta.assistants.create(
name="Karen",
instructions="Eres una asistente virtual que adora a su creadora",
model=model
)

thread = client.beta.threads.create()

def petition(text):
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=text
    )

    run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions="El nombre del usuario es Andrea y ella es tu creadora."
    )
    
    while run.status in ['queued', 'in_progress', 'cancelling']:
        time.sleep(1) # Wait for 1 second
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )

    if run.status == 'completed': 
        messages = client.beta.threads.messages.list(
        thread_id=thread.id
        )
        print(messages.data[0].content[0].text.value)
    else:
        print(run.status)

request = "hola"

petition(request)
while(True):
    request = input()
    petition(request)