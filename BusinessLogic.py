import telebot
import sqlite3

# API-TOKEN
bot = telebot.TeleBot('token')

def create_db():
    db_name = 'ProfileUser'
    query_create = '''CREATE TABLE UsersLastEntry (id_us INTEGER, record TEXT NOT NULL)'''

    sql_conn = sqlite3.connect(db_name)
    cursor = sql_conn.cursor()
    cursor.execute(query_create)
    sql_conn.commit()

    cursor.close()
    sql_conn.close()

# Init DB
# create_db()

def add_in_table(message):
    print("add_in_table worked")
    print(message.text)
    if message.text != "/replay":
        sql_conn = sqlite3.connect('ProfileUser')
        cursor = sql_conn.cursor()

        record = message.text
        user_id = 0

        query_check = '''SELECT * FROM UsersLastEntry WHERE id_us=?'''
        query_add = '''INSERT INTO UsersLastEntry (record, id_us) VALUES (?, ?)'''
        query_update = '''UPDATE UsersLastEntry SET record = ? WHERE id_us = ?'''

        info = cursor.execute(query_check, (user_id, ))
        if info.fetchone() is None:
            cursor.execute(query_add, (record, user_id, ))
            sql_conn.commit()
            print("add_rec worked")
            return

        else:
            data = (record, user_id)
            cursor.execute(query_update, data)
            sql_conn.commit()
            print("update_rec worked")
            return

        cursor.close()
        sql_conn.close()
        return
    else:
        record = get_record_table()
        bot.send_message(message.from_user.id, "Это твоё последнее сообщение:" + " " + str(record) + ".")
        return

def get_record_table():
    print("get_record_table worked")
    sql_conn = sqlite3.connect('ProfileUser')
    cursor = sql_conn.cursor()

    user_id = 0

    query_get_rec = '''SELECT record FROM UsersLastEntry WHERE id_us=?'''

    temp = cursor.execute(query_get_rec, (user_id,))
    print(temp)

    record = cursor.fetchall()
    print(record)

    # sql_conn.commit()

    cursor.close()
    sql_conn.close()

    return record

# Главный обработчик текстовых сообщений
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    while message.text != '/replay':
        if message.text == "Привет":
            bot.send_message(message.from_user.id, "Привет," + " " + message.from_user.first_name + " " + "(" + message.from_user.username + ")" + ".")
            return

        else:
            bot.register_next_step_handler(message, add_in_table)
            return

    else:
        record = get_record_table()
        bot.send_message(message.from_user.id, "Это твоё последнее сообщение:" + " " + str(record) + ".")


bot.polling(none_stop=True)
