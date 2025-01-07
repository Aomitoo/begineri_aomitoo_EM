def clear_session_state(session_state):
    if 'send_mail' in session_state:
        del session_state['send_mail']
    if 'send_email' in session_state:
        del session_state['send_email']
    if 'name_mail' in session_state:
        del session_state['name_mail']
    if 'bind_email' in session_state:
        del session_state['bind_email']
    
    session_state = {}