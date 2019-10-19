from enum import Enum


#адрес сервера, пароль и логин
BASE_URL = 'http://SOME_URL'
SERVER_LOGIN = 'LOGIN'
SERVER_PASSWORD = 'PASSWORD'

#токен тестовой группы
token = "18c6567b488379071d84018da112ec75d868d8ebff61cc0e592d233d2bed377a2fa95e8dac7711188bba4"
group_id = '186944737'



#состояния бота
class UserState(Enum):
    MAIN = 0
    SAY_HELLO = 1
