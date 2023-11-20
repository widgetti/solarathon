import solara
import time
from solarathon.components import chat
import typing

class Message(typing.TypedDict):
    user: bool
    name: str
    message: str

messages = solara.reactive([])
name = solara.reactive("User")

@solara.component
def Page():
    def add_message(new_message):
        messages.set([
            *messages.value,
            {"user": True, "name": name.value, "message": new_message,},
        ])

    def bot_response():
        # only respond if the last message was from the user
        if len(messages.value) == 0:
            print("no messages")
            return
        if not messages.value[-1]["user"]:        
            print("I don't reply to myself")
            return
        time.sleep(2)
        messages.set([
            *messages.value,
            {"user": False, "name": "Bot", "message": "Hello, " + name.value + " I cannot help you.",},
        ])
    
    print(messages.value)
    thread_result = solara.use_thread(bot_response, dependencies=[messages.value])
    with solara.Column(style={"height": "100%"}):
        # Note that we make this title component a child of the column, so that it does not interfere
        # with the height 100% flow
        solara.Title("Chat with a bot")
        solara.InputText("username", value=name)
        with chat.ChatBox():
            for item in messages.value:
                with chat.ChatMessage(
                    user=item["user"],
                    name=item["name"],
                ):
                    solara.Markdown(item["message"])
        chat.ChatInput(send_callback=add_message)
        solara.ProgressLinear(thread_result.state == solara.ResultState.RUNNING)
        if thread_result.error:
            solara.Error(str(thread_result.error))
