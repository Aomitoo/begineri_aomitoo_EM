def name_mail(data, user_state_update, session_state, d):
    user_message = data['request']['command'].lower()
    if 'name_mail' not in user_state_update:
        user_state_update['name_mail'] = {}
    if 'name_mail' not in session_state:
        session_state['name_mail'] = {}

    if d == 1 and not(session_state['name_mail']):
        response_text = 'Введите,пожалуйста, адрес почты который хотите сохранить'
        session_state['name_mail']['safe_mail'] = 1
        return response_text
    elif 'safe_mail' in session_state['name_mail'] and session_state['name_mail']['safe_mail'] == 1:
        session_state['name_mail']['safe_mail'] = data['request']["original_utterance"].lower()
        response_text = 'Под каким именем хотите сохранить почту?'
        session_state["name_mail"]['safe_name'] = 1
        return response_text
    elif 'safe_name' in session_state['name_mail'] and session_state['name_mail']['safe_name'] == 1:
        session_state['name_mail']['safe_name'] = data['request']["original_utterance"].lower()
        response_text = f'Адресс почты: {session_state["name_mail"]["safe_mail"]} \n\n' \
                        f'Имя: {session_state["name_mail"]["safe_name"]} \n\n' \
                        f'Сохраняю?'
        session_state['name_mail']['ready'] = 1
        return response_text
    elif 'ready' in session_state['name_mail'] and session_state['name_mail']['ready'] == 1:
        if user_message in ['да', 'сохраняй', 'да сохраняй', 'да, сохраняй']:
            user_state_update['name_mail'][session_state['name_mail']['safe_name']] = session_state['name_mail']['safe_mail']
            response_text = 'Почта успешно сохранена, хотите что нибудь еще?'
            del session_state['name_mail']
            return response_text
        else:
            response_text = 'Чтобы корректно обработать ваш запрос, уточните что хотите изменить "адрес почты" или "имя"?'
            session_state['name_mail']['ready'] = 2
            return response_text
    elif 'ready' in session_state['name_mail'] and session_state['name_mail']['ready'] == 2:
        if user_message == 'адрес почты':
            response_text = 'Введите,пожалуйста, адрес почты который хотите сохранить'
            session_state['name_mail']['ready'] = 2.1
            return response_text
        elif user_message == 'имя':
            response_text = 'Введите,пожалуйста, имя которое хотите привязать к почте'
            session_state['name_mail']['ready'] = 2.2
            return response_text
        else:
            return 'Я вас не поняла, скажите пожалуйста, вы хотите изменить адрес почты или имя? \n' \
                   'Если не хотите ничего сохранять то просто скажите "Алиса стоп"'

    elif 'ready' in session_state['name_mail'] and session_state['name_mail']['ready'] == 2.1:
        session_state['name_mail']['safe_mail'] = data['request']["original_utterance"].lower()
        response_text = f'Адресс почты: {session_state["name_mail"]["safe_mail"]} \n\n' \
                        f'Имя: {session_state["name_mail"]["safe_name"]} \n\n' \
                        f'Сохраняю?'
        session_state['name_mail']['ready'] = 1
        return response_text
    elif 'ready' in session_state['name_mail'] and session_state['name_mail']['ready'] == 2.2:
        session_state['name_mail']['safe_name'] = data['request']["original_utterance"].lower()
        response_text = f'Адресс почты: {session_state["name_mail"]["safe_mail"]} \n\n' \
                        f'Имя: {session_state["name_mail"]["safe_name"]} \n\n' \
                        f'Сохраняю?'
        session_state['name_mail']['ready'] = 1
        return response_text
    elif d == 2:
        if 'name_mail' in user_state_update and user_state_update['name_mail']:
            response_text = ''
            for key in user_state_update['name_mail']:
                p = user_state_update['name_mail'][key]
                response_text += f'{key} : {p} \n\n'
            response_text = response_text + '\n\n Если хотите что-то изменить скажите: удалить почту из списка'
            return response_text
        else: return 'У вас не сохраненно ни одной почты'
    elif d == 3 and 'dell_name_mail' not in session_state:
        if 'name_mail' in user_state_update and user_state_update['name_mail']:
            response_text = 'Назовите имя почты, которую хотите удалить'
            session_state['dell_name_mail'] = 1
            return response_text
        else: return 'У вас не сохраненно ни одной почты'
    elif d == 3 and 'dell_name_mail' in session_state:
        if user_message in user_state_update['name_mail'] :
            del user_state_update['name_mail'][user_message]
            response_text = 'Заданный элемент успешно удалён из списка сохранённых почт'
            del session_state['dell_name_mail']
            return response_text
        else: return "Нет сохранённой почты с таким именем"
    else: return 'При сохранении почты произошла ошибка'
