def instruction():
    response_text = "Настройка почты: \n\n " \
                    "Так как мы отправляем письма через ящик Яндекса, перед тем как начать необходимо проверить настройки." \
                    "Первым делом, необходимо проверить, включен ли в ящике IMAP (без него SMTP работать не будет по соображениям безопасности)" \
                    "Для этого перейдите по сылке https://mail.yandex.ru/?#setup/client , поставьте галочку на IMAP и сохраните изменения. \n\n" \
                    "Мы рекомендуем создать отдельный пароль для почты яндекс чтобы не сообщать сторонним сервисам ваш общий пароль на Яндексе" \
                    "Подробнее об этом по сылке - https://id.yandex.ru/security - пролистайте в самый низ, и нажмите на 'Пароли приложений' \n\n" \
                    "Также, для удобной отправки письма, можно привязать к любой почте ключевое слово по которому я буду понимать на какую почту вы хотите отправить пиьсмо, для этого скажите сохранить почту. "

    return response_text