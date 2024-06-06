import openai
import playsound
import time
import os

from Listen import listen
import credentials
import functions

user = os.getlogin()

client = openai.OpenAI(
    api_key=credentials.get_apikey()
)
model = "gpt-3.5-turbo-16k"

assistant = client.beta.assistants.retrieve(credentials.get_assistantid()) #para no necesitar la creacion de una asistente cada que entro uso un id creado antes por mi en openai

thread = client.beta.threads.create()

def speak(text):
    response = client.audio.speech.create(
    model="tts-1",
    voice="nova",
    input=text,
    )

    response.stream_to_file("output.mp3")

    playsound.playsound("output.mp3")

def handling_function(tools):
   tool_outputs = []
   for tool in tools:
    if tool.function.name == "get_weather":
        tool_outputs.append({
        "tool_call_id": tool.id,
        "output": functions.get_weather()
        })
    elif tool.function.name == "pause":
        tool_outputs.append({
        "tool_call_id": tool.id,
        "output": functions.pause()
        })

    return(tool_outputs)
        

def petition(text):
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=text
    )

    run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions="Tu nombre es karen y el nombre del usuario es " + user
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
        speak(messages.data[0].content[0].text.value)
        print(messages.data[0].content[0].text.value)
    else:
        if run.status == "requires_action":
            tool_outputs = handling_function(run.required_action.submit_tool_outputs.tool_calls)
            # Submit all tool outputs at once after collecting them in a list
            if tool_outputs:
                try:
                    run = client.beta.threads.runs.submit_tool_outputs(
                    thread_id=thread.id,
                    run_id=run.id,
                    tool_outputs=tool_outputs
                    )
                    print("Tool outputs submitted successfully.")
                except Exception as e:
                    print("Failed to submit tool outputs:", e)
            else:
                print("No tool outputs to submit.")

request = "hola podrias presentarte por favor"

petition(request)
while(True):
    request = listen()
    if request != "":
        petition(request)