from flask import Flask, request
import smtplib
from email.mime.text import MIMEText
from email.header import Header


app = Flask(__name__)



@app.route('/webhook', methods=['POST'])
def webhook():
    global user_state_update, data, session_state

    data = request.get_json()
    user_state_update = data['state']['user']
    session_state = data['state']['session']


    response_text = dialog_manager(session_state,)


    response = {'version': data['version'],
                'session': data['session'],
                'response': {'text' : response_text, 'end_session': False},
                "user_state_update": user_state_update,
                "session_state": session_state}

    return response

def dialog_manager(session_state):
    user_message = data['request']['command'].lower()
    if user_message in ['нет', 'не отправляй', 'алиса остановись', 'остановись', 'алиса стоп', 'стоп', 'алиса назад', 'назад', 'алиса перестань', 'перестань', 'алиса сначала', 'сначала']:
        return clear_session_state()

    if 'send_mail' in session_state and 'subject' in session_state['send_mail'] and session_state['send_mail']['subject'] == 1 and user_message in ['без темы', 'без']:
        session_state['send_mail']['subject'] = 'none'
        return send_mail()


    if 'send_mail' in  session_state and 'send_letter' in session_state['send_mail'] and ('прочитать' in user_message or 'прочти' in user_message or 'что получилось' in user_message):
        return f'Получатель: {session_state["send_mail"]["recipient"]} \n\n' \
               f'Тема: {session_state["send_mail"]["subject"]} \n\n' \
               f'Текст: {session_state["send_mail"]["body"]}'

    if 'change_mail' in session_state:
        if session_state['change_mail'] == 'thema':
            return change_mail('change_thema')
        if session_state['change_mail'] == 'body':
            return change_mail('change_body')
        if session_state['change_mail'] == 'recipient':
            return change_mail('change_recipient')
        
    if 'send_mail' in session_state:
        if user_message == 'изменить тему':
            return change_mail('thema')
        elif user_message == 'изменить текст':
            return change_mail('body')
        elif user_message == 'изменить получателя':
             return change_mail('recipient')

    if 'bind_email' in session_state:
        if 'email_input' in session_state['bind_email'] and session_state['bind_email']['email_input'] == 1:
            return bind_mail()
        if 'password_input' in session_state['bind_email'] and session_state['bind_email']['password_input'] == 1:
           return bind_mail()

    if 'send_mail' in session_state:
        if 'recipient' in session_state['send_mail'] and session_state['send_mail']['recipient'] == 1:
           return send_mail()
        if 'subject' in session_state['send_mail'] and session_state['send_mail']['subject'] == 1:
           return send_mail()
        if 'body' in session_state['send_mail'] and session_state['send_mail']['body'] == 1:
           return send_mail()
        if 'send_letter' in session_state['send_mail']:
            return send_mail()

    if 'send_email' in session_state and session_state['send_email']:
        return send_mail()
    if 'name_mail' in session_state and session_state['name_mail']:
        return name_mail(1)
    if 'dell_name_mail' in session_state:
        return name_mail(3)


    return handle_request(data)


def handle_request(request_data):
    user_message = request_data['request']['command'].lower()

    if user_message == "":
        return hello()
    if user_message == "очистить данные почты":
        return clear_user_state()
    if user_message == 'привязать почту':
        return bind_mail()
    if user_message == 'отправить письмо':
        return send_mail()
    if user_message == 'инструкция по настройке почты':
        return instruction()
    if user_message in ['сохранить почту', 'записать почту', 'запомнить почту']:
        return name_mail(1)
    if user_message in ["покажи список сохраненных почт","прочти список почт", "покажи список почт", 'какие имена есть', 'какие почты я сохранил', 'какие имена я сохранил', 'покажи сохраненные почты', 'покажи сохраненные имена','покажи сохраненные адреса почт',"прочти список адресов почт", "покажи список адресов почт", 'какие адреса почт я сохранил']:
        return name_mail(2)
    if user_message in ['удалить почту из сохранённых', 'удалить почту из списка сохранёных почт', 'удалить почту из списка', 'удалить почту']:
        return name_mail(3)
    if user_message in ['нужна помощь', 'помощь']:
        return help()

    return unknown_command()

def hello():
    response_text = "Приветствую! Я Голосовой почтальон, помогаю отправлять письма от вашей Яндекс Почты. \n\n " \
    "Чтобы начать работу сначала скажите 'инструкция по настройке почты', пройдите предложенную процедуру, после настройки скажите Привязать почту, если вы это уже сделали скажите Отправить письмо"
    return response_text

def stop():
    response_text = "Ладно, чего изволите?"
    session_state = {}
    return response_text

def help():
    return 'Чтобы пользоваться данным навыком нужно обязательно привязать почту. Перед привязкой почты необходимо выполнить настройку почту, подробнее о настройке почты в инструкции по настройке почты. \n\n' \
           '\n\n' \
           'Для того чтобы привязать почту, скажите привязать почту, а после следуйте моим указаниям \n\n' \
           'Далее уже можно отправлять письмо, просто скажите мне отправить письмо. На какждом этапе составления письма можно мне сказать изменить получателя или тему или текст. \n\n' \
           'После вам предложат отправить письмо на адрес получателя. В этот момент можно будет полностью прочесть сожержание письма, сказав мне прочесть или прочти что получилось. \n\n' \
           'Замечания: \n Если я услышу от вас единым сообщением слова нет, стоп, остановись, мне ничего не останется кроме как отменить текующую процедуру.' \
           '\n Чтобы не вписывать вручную адрес получателя во время составления письма можно заменить его на ключевое слово, для этого скажите мне сохранить или записать почту' \
           '\n Чтобы прочесть список сохранённых почт, скажите покажи сохранённые почты'

def instruction():
    response_text = "Настройка почты: \n\n " \
                    "Так как мы отправляем письма через ящик Яндекса, перед тем как начать необходимо проверить настройки." \
                    "Первым делом, необходимо проверить, включен ли в ящике IMAP (без него SMTP работать не будет по соображениям безопасности)" \
                    "Для этого перейдите по сылке https://mail.yandex.ru/?#setup/client , поставьте галочку на IMAP и сохраните изменения. \n\n" \
                    "Мы рекомендуем создать отдельный пароль для почты яндекс чтобы не сообщать сторонним сервисам ваш общий пароль на Яндексе" \
                    "Подробнее об этом по сылке - https://id.yandex.ru/security - пролистайте в самый низ, и нажмите на 'Пароли приложений' \n\n" \
                    "Также, для удобной отправки письма, можно привязать к любой почте ключевое слово по которому я буду понимать на какую почту вы хотите отправить пиьсмо, для этого скажите сохранить почту. "

    return response_text

def clear_user_state():
    user_state_update['email'] = None
    user_state_update['password'] = None

    return 'Авторизационные данные успешно очищены'

def clear_session_state():
    if 'send_mail' in session_state:
        del session_state['send_mail']
    if 'send_email' in session_state:
        del session_state['send_email']
    if 'name_mail' in session_state:
        del session_state['name_mail']
    return stop()

def bind_mail():
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




def send_mail():

    if 'email' not in user_state_update or "password" not in user_state_update:
        return "Вы пока что не можете отправлять письма так как вы ещё не привязали почту."

    if "send_mail" not in session_state:
        session_state['send_mail'] = {}

    if 'send_email' not in session_state:
        if 'recipient' not in session_state['send_mail']:
            response_text = 'Кому вы хотите отправить письмо?'
            session_state['send_mail']['recipient'] = 1
            return response_text
        elif session_state['send_mail']['recipient'] == 1:
            session_state['send_mail']['recipient'] = data['request']["original_utterance"]
            if 'subject' not in session_state['send_mail']:
                response_text = f'Получатель: {data["request"]["original_utterance"]}, на какую тему хотите отправить письмо? Если хотите отправить письмо без темы, просто скажите "без темы"'
                session_state['send_mail']['subject'] = 1
                return response_text
            elif session_state['send_mail']['subject'] != 1 and 'body' in session_state['send_mail'] and session_state['send_mail']['body'] != 1:
                response_text = f'Получатель: {data["request"]["original_utterance"]}, отправить письмо?'
                return response_text
            elif session_state['send_mail']['subject'] != 1 and 'body' in session_state['send_mail'] and session_state['send_mail']['body'] == 1:
                return f'Получатель: {data["request"]["original_utterance"]}, какой текст нужно передать? '
            elif session_state['send_mail']['subject'] == 1:
                return f'Получатель: {data["request"]["original_utterance"]}, на какую тему хотите отправить письмо?'
            return 'Произошла ошибка при сохранении получателя пиьсма'

        elif session_state['send_mail']['subject'] == 1:
            session_state['send_mail']['subject'] = data['request']["original_utterance"]
            if 'body' not in session_state['send_mail']:
                response_text = f'Тема: {data["request"]["original_utterance"]}, что нужно передать?'
                session_state['send_mail']['body'] = 1
                return response_text
            elif session_state['send_mail']['body'] != 1:
                response_text = f'Тема: {data["request"]["original_utterance"]}, Отправить письмо?'
                return response_text
            elif session_state['send_mail']['body'] == 1:
                response_text = f'Тема: {data["request"]["original_utterance"]}, какой текст нужно передать?'
                return response_text
            return 'Произошла ошибка при сохранении темы пиьсма'
        elif session_state['send_mail']['subject'] == 'none':
            session_state['send_mail']['subject'] = ' '
            if 'body' not in session_state['send_mail']:
                response_text = f'Хорошо, письмо будет без темы, что нужно передать?'
                session_state['send_mail']['body'] = 1
                return response_text
            elif session_state['send_mail']['body'] != 1:
                response_text = f'Тема: {data["request"]["original_utterance"]}, Отправить письмо?'
                return response_text
            return 'Произошла ошибка при сохранении темы пиьсма'


        elif session_state['send_mail']['body'] == 1:
            session_state['send_mail']['body'] = data['request']["original_utterance"]
            response_text = f'Текст: {data["request"]["original_utterance"]}. \n Если хотите прочесть весь состав письма, скажите прочти письмо. Если нужно что-то изменить скажите изменить получателя тему текст. \n\n' \
                            f'Я могу отправлять ваше письмо?'
            session_state['send_mail']['send_letter'] = 1
            return response_text
        elif session_state['send_mail']['send_letter'] == 1:
            if data['request']['command'].lower() in ["да", 'отправить письмо', 'да, отправить', 'отправляй', 'угу', 'можно', 'отправить']:
                session_state['send_email'] = 1
            else:
                return "Извините я вас не поняла, перефразируйте пожалуйста."





    if 'recipient' in session_state['send_mail'] and 'subject' in session_state['send_mail'] and 'body' in session_state['send_mail'] and session_state['send_email'] == 1:
        recipient = session_state['send_mail']['recipient']
        subject = session_state['send_mail']['subject']
        body = session_state['send_mail']['body']

        if 'name_mail' in user_state_update and recipient.lower() in user_state_update['name_mail']:
            recipient = user_state_update['name_mail'][recipient.lower()]
        else: 
            return f"Неизвестный получатель. {change_mail('recipient')}"

        try:
            send_email(recipient, subject, body)
            response_text = f"Письмо успешно отправлено на {recipient}"
        except Exception as e:
            return f'Произошла ошибка при отправке письма: {e}, убедитесь, что введенные данные корректны и попробуйте снова'

        return response_text

    return 'Произошла неизвестная ошибка'



def send_email(to, subject, body):
    msg = MIMEText(body.encode('utf-8'), _charset='UTF-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = user_state_update['email']
    msg['To'] = to

    mailserver = smtplib.SMTP('smtp.yandex.ru', 587)
    mailserver.ehlo()
    mailserver.starttls()  # Включаем защищенное соединение TLS
    mailserver.login(user_state_update['email'], user_state_update['password'])
    mailserver.sendmail(user_state_update['email'], [to], msg.as_string())
    mailserver.quit()

    return True

def change_mail(change):

    if change == "thema":
       response_text = 'Хорошо, изменим тему. На какую тему хотите отправить письмо?'
       session_state['change_mail'] = 'thema'
       return response_text
    if change == 'body':
        response_text = 'Хорошо, изменим текст письма. Скажите, какой текст хотите передать?'
        session_state['change_mail'] = 'body'
        return response_text
    if change == 'recipient':
        response_text = 'Хорошо изменим получателя письма. Кому хотите отправить письмо?'
        session_state['change_mail'] = 'recipient'
        return response_text

    if change == 'change_thema':
        session_state['send_mail']["subject"] = data['request']["original_utterance"]
        del session_state['change_mail']
        session_state['send_mail']['subject'] = 1
        return send_mail()
    if change == 'change_body':
        session_state['send_mail']["body"] = data['request']["original_utterance"]
        del session_state['change_mail']
        session_state['send_mail']['body'] = 1
        return send_mail()
    if change == 'change_recipient':
        session_state['send_mail']["recipient"] = data['request']["original_utterance"]
        del session_state['change_mail']
        session_state['send_mail']['recipient'] = 1
        return send_mail()

def name_mail(d):
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



def unknown_command():
    response_text = "Я не понял вашу команду. Если хотите узнать подробнее о командах скажите помощь."
    return response_text


if __name__ == '__main__':
    app.run('0.0.0.0', port = 5000 ,debug=True)