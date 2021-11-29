import config
import telebot
import sqlite3
import logging

bot = telebot.TeleBot(config.API_TOKEN)
initDB()

def initDB():
    try:
        con = sqlite3.connect(config.SQLITE3_DB_PATH)
    except Exception as e:
        logging.error(config.STRING_ERROR_OPENING_DB.format(e))
    else:
        try:
            con.execute(config.SQL_INIT)
            con.commit()
        except Exception as e:
            logging.error(config.STRING_ERROR_INIT_DB.format(e))
        con.close()

def isFromAdmin(message):
    userID = message.from_user.id
    admin = False
    try:
        con = sqlite3.connect(config.SQLITE3_DB_PATH)
    except:
        pass
    else:
        try:
            users = [row[0] for row in con.execute(config.SQL_IS_ADMIN,[userID]).fetchall()]
        except:
            pass
        else:
            if len(users) > 0 and all(q):
                admin = True
        con.close()
    return admin

@bot.message_handler(commands=config.GET_USERS_METHODS)
def get_users(message):
    if isFromAdmin(message):
        try:
            con = sqlite3.connect(config.SQLITE3_DB_PATH)
        except Exception as e:
            logging.error(config.STRING_ERROR_OPENING_DB.format(e))
            bot.reply_to(message, config.STRING_ERROR_OPENING_DB.format(e))
        else:
            try:
                q = [row for row in con.execute(config.SQL_ALL_USERS).fetchall()]
            except Exception as e:
                logging.error(config.STRING_ERROR_USER_DOESNT_EXIST)
                bot.reply_to(message, config.STRING_ERROR_USER_DOESNT_EXIST)
            else:
                bot.reply_to(message, "\r\n".join([str(row) for row in q]))
    else:
        logging.error(config.STRING_ERROR_NOT_AUTHORIZED)
        bot.reply_to(message, config.STRING_ERROR_NOT_AUTHORIZED)


@bot.message_handler(commands=config.REQUIRES_ADMIN_METHODS)
def modify_user(message):
    if isFromAdmin(message):
        try:
            command = message.text.split()[0]
            username = message.text.split()[1]
        except:
            logging.error(config.STRING_ERROR_NO_ID)
            bot.reply_to(message, config.STRING_ERROR_NO_ID)
        else:
            try:
                con = sqlite3.connect(config.SQLITE3_DB_PATH)
            except Exception as e:
                logging.error(config.STRING_ERROR_OPENING_DB.format(e))
                bot.reply_to(message, config.STRING_ERROR_OPENING_DB.format(e))
            else:
                try:
                    q = con.execute(config.SQL_MATCHING_USERS,[username]).fetchall()
                except Exception as e:
                    logging.error(config.ERROR_MODIFY_USER_DOESNT_EXIST)
                    bot.reply_to(message, config.ERROR_MODIFY_USER_DOESNT_EXIST)
                else:
                    if len(q) == 0:
                        logging.error(config.ERROR_MODIFY_USER_NO_MATCH)
                        bot.reply_to(message, config.ERROR_MODIFY_USER_NO_MATCH)
                    else:
                        try:
                            if command in config.ALLOW_MEHTODS:
                                con.execute(config.SQL_ALLOW_USER,[username])
                            elif command in config.UNALLOW_METHODS:
                                con.execute(config.SQL_UNALLOW_USER,[username])
                            elif command in config.PROMOTE_METHODS:
                                con.execute(config.SQL_PROMOTE_USER,[username])
                            elif command in config.DEMOTE_METHODS:
                                con.execute(config.SQL_DEMOTE_USER,[username])
                            con.commit()
                        except Exception as e:
                            logging.error(config.ERROR_MODIFY_USER_UNABLE.format(e))
                            bot.reply_to(message,config.ERROR_MODIFY_USER_UNABLE.format(e))
                        else:
                            logging.error(config.STRING_MODIFIED_USER)
                            bot.reply_to(message, config.STRING_MODIFIED_USER)
                            for row in q:
                                if command in config.ALLOW_MEHTODS:
                                    bot.send_message(row[0],config.STRING_SUBSCRIBED)
                                elif command in config.UNALLOW_METHODS:
                                    bot.send_message(row[0],config.STRING_UNSUBSCRIBED)
                                elif command in config.PROMOTE_METHODS:
                                    bot.send_message(row[0],config.STRING_PROMOTED)
                                elif command in config.DEMOTE_METHODS:
                                    bot.send_message(row[0],config.STRING_DEMOTED)
                con.close()
    else:
        logging.error(config.STRING_ERROR_NOT_AUTHORIZED)
        bot.reply_to(message, config.STRING_ERROR_NOT_AUTHORIZED)

@bot.message_handler(commands=config.HELP_METHODS)
def help(message):
    try:
        l = [
            "Help Menu:",
            "   /start                  Request Access to Subscription", ]
        if isFromAdmin(message):
            l = l + [
                "   /allow {userID}         Allow User Access to Subsription",
                "   /admin {userID}         Promote User to admin",
                "   /block {userID}         Remove All Access from User", ]
        l = l + ["   /help                   This Menu",]
        bot.reply_to(message,"\r\n".join(l))
    except Exception as e:
        logging.error(config.STRING_ERROR_HELP.format(e))

@bot.message_handler(commands=config.START_METHODS)
def send_welcome(message):
    d = {
        'from_user_id':         message.from_user.id,
        'from_user_firstName':  message.from_user.first_name,
        'from_user_username':   message.from_user.username, }
    print(d)
    try:
        con = sqlite3.connect(config.SQLITE3_DB_PATH)
    except Exception as e:
        logging.error(config.STRING_ERROR_OPENING_DB)
    else:
        try:
            admins = con.execute(config.SQL_ADMIN_USERS).fetchall()
        except Exception as e:
            logging.error(config.STRING_ERROR_NO_ADMINS.format(e))
        try:
            users = con.execute(config.SQL_ALL_USERS).fetchall()
        except Exception as e:
            logging.error(config.STRING_ERROR_NO_USERS.format(e))
        else:
            if len(users) == 0:
                d['noUsers'] = True
        try:
            existingUser = con.execute(config.SQL_MATCHING_USERS,[d['from_user_id']]).fetchall()
        except Exception as e:
            logging.error(config.STRING_ERROR_USER_DOESNT_EXIST)
        else:
            if len(existingUser) == 0:
                try:
                    con.execute(config.SQL_INSERT_ADMIN if d.get('noUsers',False) else config.SQL_INSERT_USER,[
                        d['from_user_id'],
                        d['from_user_firstName'],
                        d['from_user_username'], ])
                    con.commit()
                except Exception as e:
                    e = {
                        'Location':     "AddUser",
                        'Description':  "ERROR Executing SQL",
                        'Error':        str(e), }
                    logging.error("[{Location}] {Description}: {Error}".format(**e))
                else:
                    d['added'] = True
                    logging.error(config.STRING_ADDED_USER)
            else:
                try:
                    con.execute(config.SQL_UPDATE_USER,[
                        d['from_user_firstName'],
                        d['from_user_username'],
                        d['from_user_id'], ])
                    con.commit()        
                except Exception as e:
                    e = {
                        'Location':     "UpdateUser",
                        'Description':  "ERROR Executing SQL",
                        'Error':        str(e), }
                    logging.error("[{Location}] {Description}: {Error}".format(**e))
                else:
                    d['updated'] = True
                    logging.error("Updated User!")
        con.close()
    if d.get('noUsers',False):
        bot.reply_to(message, config.STRING_ADMIN_SUBSCRIBED)
    else:
        if d.get('added',False):
            bot.reply_to(message, config.STRING_WAIT_FOR_AUTH)
            for row in admins:
                bot.send_message(row[0],config.STRING_AUTH_SUGGEST.format(
                    d['from_user_id'],
                    d['from_user_firstName'],
                    d['from_user_username'],
                    d['from_user_id']))
        if d.get('updated',False):
            bot.reply_to(message, config.STRING_UPDATED_SELF)

bot.infinity_polling()
