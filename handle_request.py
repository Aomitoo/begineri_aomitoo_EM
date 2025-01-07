from hello import hello
from clear_user_state import clear_user_state
from bind_mail import bind_mail
from send_mail import send_mail
from instruction import instruction
from name_mail import name_mail
from help import help
from unknown_command import unknown_command


def handle_request(data, user_state_update, session_state):
    user_message = data['request']['command'].lower()

    if user_message == "":
        return hello()
    if user_message == "очистить данные почты":
        return clear_user_state(user_state_update)
    if user_message == 'привязать почту':
        return bind_mail(data, user_state_update, session_state)
    if user_message == 'отправить письмо':
        return send_mail(data, user_state_update, session_state)
    if user_message == 'инструкция по настройке почты':
        return instruction()
    if user_message in ['сохранить почту', 'записать почту', 'запомнить почту']:
        return name_mail(data, user_state_update, session_state, 1)
    if user_message in ["покажи список сохраненных почт","прочти список почт", "покажи список почт", 'какие имена есть', 'какие почты я сохранил', 'какие имена я сохранил', 'покажи сохраненные почты', 'покажи сохраненные имена','покажи сохраненные адреса почт',"прочти список адресов почт", "покажи список адресов почт", 'какие адреса почт я сохранил', "список почт"]:
        return name_mail(data, user_state_update, session_state, 2)
    if user_message in ['удалить почту из сохранённых', 'удалить почту из списка сохранёных почт', 'удалить почту из списка', 'удалить почту']:
        return name_mail(data, user_state_update, session_state, 3)
    if user_message in ['нужна помощь', 'помощь']:
        return help()

    return unknown_command()
