from send_mail import send_mail


def change_mail(data, session_state, user_state_update, change):
    if change == "thema":
        session_state['change_mail'] = 'thema'
        return 'Хорошо, изменим тему. На какую тему хотите отправить письмо?'
    
    if change == 'body':
        session_state['change_mail'] = 'body'
        return 'Хорошо, изменим текст письма. Скажите, какой текст хотите передать?'
    
    if change == 'recipient':
        session_state['change_mail'] = 'recipient'
        return 'Хорошо изменим получателя письма. Кому хотите отправить письмо?'
    
    user_message = data['request']["original_utterance"]
    
    if change == 'change_thema':
        session_state['send_mail']["subject"] = user_message
        del session_state['change_mail']
        session_state['send_mail']['subject'] = 1
        return send_mail(data, user_state_update, session_state)
    
    if change == 'change_body':
        session_state['send_mail']["body"] = user_message
        del session_state['change_mail']
        session_state['send_mail']['body'] = 1
        return send_mail(data, user_state_update, session_state)
    
    if change == 'change_recipient':
        session_state['send_mail']["recipient"] = user_message
        del session_state['change_mail']
        session_state['send_mail']['recipient'] = 1
        return send_mail(data, user_state_update, session_state)