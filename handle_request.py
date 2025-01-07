from bind_mail import bind_mail
from clear_email import clear_email
from comands import comands
from hello import hello
from help import help
from name_mail import name_mail
from send_mail import send_mail
from instruction import instruction
from unknown_command import unknown_command



def handle_request(data, user_state_update, session_state):
    intents = data['request']['nlu']['intents']
    user_message = data['request']['command']

    if user_message == "":
        return hello()
    if 'clear_email' in intents:
        return clear_email(user_state_update)
    if 'bind_mail' in intents:
        return bind_mail(data, user_state_update, session_state)
    if 'send_mail' in intents:
        return send_mail(data, user_state_update, session_state)
    if 'instruction' in intents:
        return instruction()
    if 'name_mail' in intents:
        return name_mail(data, user_state_update, session_state, 1)
    if 'list_name_mail' in intents:
        return name_mail(data, user_state_update, session_state, 2)
    if 'delete_name_mail' in intents:
        return name_mail(data, user_state_update, session_state, 3)
    if 'help' in intents:
        return help()
    if 'comands' in intents:
        return comands()

    return unknown_command()