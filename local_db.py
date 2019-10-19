import sqlite3

conn = sqlite3.connect("database")

def set_user_state(user_id, state):
    '''
    Добавляет имя конкурса и id в бд
    :param user_id: id пользователя
    :param state: состояние
    :return:
    '''
    cursor = conn.cursor()
    sql = 'INSERT INTO user_state VALUES (?,?);'
    cursor.execute(sql, (user_id, state))
    cursor.close()
    conn.commit()


def change_user_state(user_id, state):
    '''обновить значения стейта'''
    cursor = conn.cursor()
    sql = 'UPDATE user_state SET user_state = ? WHERE user_id = ?;'
    cursor.execute(sql, (state, user_id))
    cursor.close()
    conn.commit()


def get_user_state(user_id):
    '''узнать состояние пользователя'''
    cursor = conn.cursor()
    sql = 'SELECT * FROM user_state WHERE user_id = ?;'
    cursor.execute(sql, [(user_id)])
    contest = cursor.fetchall()
    cursor.close()
    return contest

