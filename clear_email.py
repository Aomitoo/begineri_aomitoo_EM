def clear_email(user_state_update):
    user_state_update['email'] = None
    user_state_update['password'] = None

    return 'Авторизационные данные успешно очищены'