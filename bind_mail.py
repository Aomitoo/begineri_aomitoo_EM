from clear_user_state import clear_user_state
import smtplib


def bind_mail(data, user_state_update, session_state):
        if 'email' not in user_state_update and 'bind_email' not in session_state:
            response_text = "Данную процедуру рекомендуем сделать с использованием клавиатуры для более корректного ввода данных, после привязки почты процедуру повторять не нужно. \n\n" \
                            "\n\n" \
                            "Напишите свой email, напомню что почта должна быть только с доменом @yandex.ru, остальные почты пока что не поддерживаются для привязки."
            session_state['bind_email'] = {}
            session_state['bind_email']['email_input'] = 1
        elif 'password' not in user_state_update and 'bind_email' in session_state and 'password_input' not in session_state['bind_email'] :
            session_state['bind_email']['email_input'] = None
            user_state_update['email'] = data['request']["original_utterance"]
            response_text = "Адресс получен, ведите пароль от почты"
            session_state['bind_email']['password_input'] = 1
        else:
            if 'email' in user_state_update and 'password' in user_state_update and user_state_update['email'] and user_state_update['password']:
                return f'Аккаунт уже привязан: email: {user_state_update["email"]},' \
                       f'если имеются какие-то проблемы с данными почты, скажите "Очистить данные почты",' \
                       f'а после заново привяжите почту'
            session_state['bind_email']['password_input'] = None
            user_state_update['password'] = data['request']["original_utterance"]
            email = user_state_update['email']
            password = user_state_update['password']

            if len(email) < 9 or '@yandex.ru' not in email or len(password) < 5:
                clear_user_state()
                return 'Данные некорректны, попробуйте снова привязать почту, удостоверившись, что все данные введены правильно и не содержат ошибок.'
            try:
                with smtplib.SMTP('smtp.yandex.ru', 587) as server:
                    server.ehlo()
                    server.starttls()  # Включаем защищенное соединение TLS
                    server.login(email, password)
                    server.quit()
                    response_text = 'Ваша почта успешно привязана! Теперь вы можете отправлять письма на другие почты, для этого просто скажите Отправить письмо'
                    return response_text
            except Exception as e:
                response_text = f"Произошла ошибка при привязке акканута: {e}. \n\n" \
                                f"'Данные скорее всего некорректны, попробуйте снова привязать почту, удостоверившись, что все данные введены правильно и не содержат ошибок.'"

                return response_text
        return response_text