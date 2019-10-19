import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.longpoll import VkLongPoll
from vk_api.utils import get_random_id
from vk_api import VkUpload
import config
import example_request
import local_db
import requests
from datetime import datetime

vk_session = vk_api.VkApi(token=config.token)
vk = vk_session.get_api()


class MyVkLongPoll(VkBotLongPoll):
    def listen(self):
        while True:
            try:
                for event in self.check():
                    yield event
            except Exception as e:
                continue


bot = MyVkLongPoll(vk_session, config.group_id)

'''/start'''
def handle_first_message(message):

    user_id = message.from_id
    text = "Привет! Я демонстрационный бот."
    vk.messages.send(peer_id=user_id, random_id=get_random_id(), message=text)
    local_db.set_user_state(user_id, config.UserState.MAIN.value)
    open_main_menu(message)
    return


def tell_story(message):
     user_id = message.from_id
     vk.messages.send(peer_id=user_id, random_id=get_random_id(), message="some story")
     open_main_menu(message)
     return


def say_hi(message):
    user_id = message.from_id
    vk.messages.send(peer_id=user_id, random_id=get_random_id(), message="Введите свое имя")
    local_db.change_user_state(user_id, config.UserState.SAY_HELLO.value);
    return


def handle_say_hay(message):
    user_id = message.from_id
    text = "Здравствуйте, " + message.text
    vk.messages.send(peer_id=user_id, random_id=get_random_id(), message=text)
    local_db.change_user_state(user_id, config.UserState.MAIN.value);
    open_main_menu
    return


'''Главное меню и обработка действий пользователя'''
def handle_message(message):
    """ Основная функция обработки сообщений """
    #узнать пользователя
    user_id = message.from_id
    #узнать его состояние
    #функция возвращает и id и cтатус
    user_state = local_db.get_user_state(user_id)
    text = message.text

    #new!! it works
    if user_state is None:
        handle_first_message(message)#стартовое состояние
    elif text == back_to_menu_message:
        try:
            open_main_menu(message)#вовзвращение в меню
        except:
            open_main_menu(message)#вовзвращение в меню
    else:
        func = find_state(user_state)
        func(message)


def main():
    """ Это функция, в которой мы получаем сообщеньки и отправляем на обработку """
  
    for event in bot.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            handle_message(event.obj)
            


def open_main_menu(message, text="Выберите из перечисленного:"):
    user_id = message.from_id
    keys = list(main_menu_commands.keys())
    

    keyboard = create_keyboard(*keys)
    vk.messages.send(peer_id=user_id, random_id=get_random_id(), message=text, keyboard=keyboard)
    local_db.change_user_state(user_id, config.UserState.MAIN.value)


def handle_main_menu_command(message):
    """ Обработать команду из главного меню """
    user_id = message.from_id
    text = message.text

    if text in main_menu_commands.keys():
        func_to_call = main_menu_commands[text]
        func_to_call(message)

    else:
        send_error_message(message)
        return


'''Отправка ошибки'''
def send_error_message(message, last_func=open_main_menu, text="Не могу понять ваш запрос.."):

    user_id = message.from_id
    vk.messages.send(peer_id=user_id, random_id=get_random_id(), message=text, reply_to=message.id)
    local_db.change_user_state(user_id, config.UserState.MAIN.value)
    last_func(message)


def create_keyboard(*buttons_text):
    """
    Создать клавиатуру
    :param buttons_text: переменное количество строк для кнопок
    :return: объект клавиатуры
    4х10 - максимум клавиатуры
    """

    k = VkKeyboard(one_time=True)
    had_exit = exit_bot_command in buttons_text
    had_back_to_menu = back_to_menu_message in buttons_text


    for button_text in buttons_text:
        if isinstance(button_text, str) and button_text != exit_bot_command and button_text != back_to_menu_message:
            color = VkKeyboardColor.PRIMARY
            k.add_button(label=button_text, color=color)
            k.add_line()

    if had_exit:
        k.add_button(label=exit_bot_command, color=VkKeyboardColor.NEGATIVE)
    if had_back_to_menu:
        k.add_button(label=back_to_menu_message, color=VkKeyboardColor.NEGATIVE)

    return k.get_keyboard()


def find_state(state):
    all_states = {
        config.UserState.MAIN.value: open_main_menu,
        config.UserState.SAY_HELLO.value: handle_say_hay    
    }
    if state in all_states:
        return all_states[state]
    else:
        return None


last_contest_for_user = {}
back_to_menu_message = "Вернуться в меню"
exit_bot_command = "Завершить работу с ботом"
main_menu_commands = {"Рассказать историю": tell_story,
                      "Сказать привет": say_hi }





if __name__ == '__main__':
    main()
