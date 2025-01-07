from clear_session_state import clear_session_state
from send_mail import send_mail
from change_mail import change_mail
from bind_mail import bind_mail
from name_mail import name_mail
from handle_request import handle_request


def is_stop_command(user_message):
    stop_commands = [
        'нет',
        'не отправляй',
        'алиса остановись',
        'остановись',
        'алиса стоп',
        'стоп',
        'алиса назад',
        'назад',
        'алиса перестань',
        'перестань',
        'алиса сначала',
        'сначала'
    ]
    return user_message.lower() in stop_commands


def get_send_mail_status(session_state):
    status = {}
    if 'send_mail' in session_state:
        for key in ['recipient', 'subject', 'body', 'send_letter']:
            if key in session_state['send_mail']:
                status[key] = session_state['send_mail'][key]
    return status


def check_change_mail_status(session_state):
    return 'change_mail' in session_state 


def check_bind_email_status(session_state):
    if 'bind_email' in session_state:
        for key in ['email_input', 'password_input']:
            if key in session_state['bind_email']:
                return True
    return False


def check_send_mail_status(status):
    if 'send_letter' in status:
        return True
    for key in ['recipient', 'subject', 'body']:
        if key in status and status[key] == 1:
            return True
    return False


def check_keys_in_session_state(session_state, key_1=0, key_2=0):
    if key_1 == 0 or key_2 == 0:
        return key_1 in session_state and session_state[key_1]
    else:
        return key_1 in session_state and key_2 in session_state[key_1]
   
    
# Обработчик
def dialog_manager(data, user_state_update, session_state):
    user_message = data['request']['command'].lower()
    
    # Обработка команд остановки
    if is_stop_command(user_message):
        clear_session_state(session_state)
        return 'Ладно, чего изволите?'

    # Обработка отправки письма без темы
    if check_keys_in_session_state(session_state, 'send_mail', 'subject') and session_state['send_mail']['subject'] == 1 and user_message in ['без темы', 'без']:
        session_state['send_mail']['subject'] = 'none'
        return send_mail(data, user_state_update, session_state)

    # Чтение составленного письма
    keys_in_session_state = check_keys_in_session_state(session_state, 'send_mail', 'send_letter')
    if keys_in_session_state and user_message in ['прочитать', 'прочти', 'что получилось']:
        return f'Получатель: {session_state["send_mail"]["recipient"]} \n\n' \
               f'Тема: {session_state["send_mail"]["subject"]} \n\n' \
               f'Текст: {session_state["send_mail"]["body"]}'

    # Обработка изменений параметров письма
    change_mail_status = check_change_mail_status(session_state)
    if change_mail_status:
        change_parametr = 'change_' + session_state['change_mail']
        return change_mail(data, session_state, user_state_update, change_parametr)

    if 'send_mail' in session_state:
        if user_message == 'изменить тему':
            return change_mail(data, session_state, user_state_update, 'thema')
        elif user_message == 'изменить текст':
            return change_mail(data, session_state, user_state_update, 'body')
        elif user_message == 'изменить получателя':
            return change_mail(data, session_state, user_state_update, 'recipient')

    # Обработка привязки электронной почты
    bind_email_status = check_bind_email_status(session_state)
    if bind_email_status:
        return bind_mail(data, user_state_update, session_state)

    # Обработка составления письма
    send_mail_status = get_send_mail_status(session_state)
    current_step = check_send_mail_status(send_mail_status)
    if current_step:
        return send_mail(data, user_state_update, session_state)
    
    # Обработка отправки письма
    if check_keys_in_session_state(session_state, 'send_email'):
        return send_mail(data, user_state_update, session_state)
    
    # Обработка замены почтового ящика именем
    if check_keys_in_session_state(session_state, 'name_mail'):
        return name_mail(data, user_state_update, session_state, 1)
    if 'dell_name_mail' in session_state:
        return name_mail(data, user_state_update, session_state, 3)

    return handle_request(data, user_state_update, session_state)
