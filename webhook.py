from dialog_manager import dialog_manager


def webhook(data, context):
    
    user_state_update = data['state']['user']
    session_state = data['state']['session']
    
    response_text = dialog_manager(data, user_state_update, session_state)
    response = {
        'version': data['version'],
        'session': data['session'],
        'response': {'text': response_text, 'end_session': False},
        "user_state_update": user_state_update,
        "session_state": session_state
        }

    return response