from send_email import send_email


def initialize_send_mail_if_needed(session_state):
    if "send_mail" not in session_state:
        session_state['send_mail'] = {}


def check_recipient_in_name_mail(recipient, user_state_update):
    return 'name_mail' in user_state_update and recipient.lower() in user_state_update['name_mail']


def check_send_mail_ready(session_state):
    return 'recipient' in session_state['send_mail'] and 'subject' in session_state['send_mail'] and 'body' in session_state['send_mail'] and session_state['send_email'] == 1


def check_email_password(user_state_update):
    return 'email' not in user_state_update or "password" not in user_state_update


def check_keys_in_session_state(session_state, key_1=0, key_2=0):
    if key_1 == 0 or key_2 == 0:
        return key_1 in session_state and session_state[key_1]
    else:
        return key_1 in session_state and key_2 in session_state[key_1]


# Составление письма
def send_mail(data, user_state_update, session_state):
    user_message = data['request']["original_utterance"]

    if check_email_password(user_state_update):
        return "Вы пока что не можете отправлять письма так как вы ещё не привязали почту."

    initialize_send_mail_if_needed(session_state)

    if 'send_email' not in session_state:
        if 'recipient' not in session_state['send_mail']:
            session_state['send_mail']['recipient'] = 1
            return 'Кому вы хотите отправить письмо?'
        
        elif session_state['send_mail']['recipient'] == 1:
            session_state['send_mail']['recipient'] = user_message
            if 'subject' not in session_state['send_mail']:
                session_state['send_mail']['subject'] = 1
                return f'Получатель: {user_message}, на какую тему хотите отправить письмо? Если хотите отправить письмо без темы, просто скажите "без темы"'
            
            elif session_state['send_mail']['subject'] != 1 and 'body' in session_state['send_mail'] and session_state['send_mail']['body'] != 1:
                return f'Получатель: {user_message}, отправить письмо?'
            
            elif session_state['send_mail']['subject'] != 1 and 'body' in session_state['send_mail'] and session_state['send_mail']['body'] == 1:
                return f'Получатель: {user_message}, какой текст нужно передать?'
            
            elif session_state['send_mail']['subject'] == 1:
                return f'Получатель: {user_message}, на какую тему хотите отправить письмо?'
            
            return 'Произошла ошибка при сохранении получателя пиьсма'

        elif session_state['send_mail']['subject'] == 1:

            session_state['send_mail']['subject'] = user_message
            if 'body' not in session_state['send_mail']:
                session_state['send_mail']['body'] = 1
                return f'Тема: {user_message}, что нужно передать?'
            
            elif session_state['send_mail']['body'] != 1:
                return f'Тема: {user_message}, Отправить письмо?'
            
            elif session_state['send_mail']['body'] == 1:
                return f'Тема: {user_message}, какой текст нужно передать?'
            
            return 'Произошла ошибка при сохранении темы пиьсма'
        
        elif session_state['send_mail']['subject'] == 'none':
            session_state['send_mail']['subject'] = ' '
            if 'body' not in session_state['send_mail']:
                session_state['send_mail']['body'] = 1
                session_state['send_mail']['body'] = session_state['send_mail']['body']
                return f'Хорошо, письмо будет без темы, что нужно передать?'
        
            elif session_state['send_mail']['body'] != 1:
                return f'Тема: {user_message}, Отправить письмо?'
        
            return 'Произошла ошибка при сохранении темы пиьсма'
        
        elif session_state['send_mail']['body'] == 1:
            session_state['send_mail']['body'] = user_message
            session_state['send_mail']['send_letter'] = 1
            return f'Текст: {user_message}. \n Если хотите прочесть весь состав письма, скажите прочти письмо. Если нужно что-то изменить скажите изменить получателя тему текст. \n\n' \
                   f'Я могу отправлять ваше письмо?'
        
        elif session_state['send_mail']['send_letter'] == 1:
            if data['request']['command'].lower() in ['прочти', 'прочти письмо', 'прочти что получилось']:
                return f'Получатель: {session_state['send_mail']['recipient']} \n\n' \
                       f'Тема: {session_state['send_mail']['subject']} \n\n' \
                       f'Текст: {session_state['send_mail']['body']} \n\n' \
                       f'Отправить письмо?'

            if data['request']['command'].lower() in ["да", 'отправить письмо', 'да, отправить', 'отправляй', 'угу', 'можно', 'отправить']:
                session_state['send_email'] = 1
            else:
                return "Извините я вас не поняла, перефразируйте пожалуйста."
    
    if check_send_mail_ready(session_state):

        recipient = session_state['send_mail']['recipient']
        subject = session_state['send_mail']['subject']
        body = session_state['send_mail']['body']
        
        if check_recipient_in_name_mail(recipient, user_state_update):
            recipient = user_state_update['name_mail'][recipient.lower()]

        try:
            send_email(recipient, subject, body, user_state_update)
            response_text = f"Письмо успешно отправлено на {recipient}"
        except Exception as e:
            return f"Произошла ошибка при отправке письма: {e}, убедитесь, что введенные данные корректны и попробуйте снова"
        del session_state["send_mail"]
        del session_state["send_email"]
        return response_text

    return "Произошла неизвестная ошибка"
