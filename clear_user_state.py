def clear_user_state(user_state_update):
    user_state_update['email'] = None
    user_state_update['password'] = None

    return 'Авторизационные данные успешно очищены'