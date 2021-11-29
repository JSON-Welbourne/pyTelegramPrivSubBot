from project.server import app
import telebot
import sqlite3
import logging
from notify_run import Notify

bot = telebot.TeleBot(app.config.get("TELEGRAM_BOT_TOKEN"))
notify = Notify()
    
def isFromAdmin(message):
    userID = message.from_user.id
    admin = False
    try:
        con = sqlite3.connect("/home/flask/abp-db/chatBot.sqlite3")
    except:
        pass
    else:
        try:
            q = [row[0] for row in con.execute("SELECT admin FROM Users WHERE id = ?",[userID]).fetchall()]
        except:
            pass
        else:
            if len(q) > 0 and all(q):
                admin = True
        con.close()
    return admin

@bot.message_handler(commands=['users'])
def get_users(message):
    if isFromAdmin(message):
        try:
            con = sqlite3.connect("/home/flask/abp-db/chatBot.sqlite3")
        except:
            logging.error("Unable to open DB!")
            bot.reply_to(message, "Unable to Open DB!")
        else:
            try:
                q = [row for row in con.execute("SELECT * FROM Users").fetchall()]
            except Exception as e:
                logging.error("Unable to get matching users")
                bot.reply_to(message, "Unable to get Matching Users")
            else:
                bot.reply_to(message, "\r\n".join([str(row) for row in q]))
    else:
        logging.error("Not Authorized to make changes!")
        bot.reply_to(message, "Not Authorized to make changes!")


@bot.message_handler(commands=['admin'])
def admin_user(message):
    if isFromAdmin(message):
        username = message.text.split()[1]
        try:
            con = sqlite3.connect("/home/flask/abp-db/chatBot.sqlite3")
        except:
            logging.error("Unable to open DB!")
            bot.reply_to(message, "Unable to Open DB!")
        else:
            try:
                q = con.execute("SELECT * FROM Users WHERE id = ?",[username]).fetchall()
            except Exception as e:
                logging.error("Unable to get matching users")
                bot.reply_to(message, "Unable to get Matching Users")
            else:
                if len(q) == 0:
                    logging.error("No Matching Users!")
                    bot.reply_to(message, "No Matching Users")
                else:
                    try:
                        con.execute("UPDATE Users SET admin = 1 WHERE id = ?",[username])
                        con.commit()
                    except:
                        logging.error("Unable to Update User")
                        bot.reply_to(message, "Unable to Update User")
                    else:
                        logging.error("Updated User")
                        bot.reply_to(message, "Updated User")
                        for row in q:
                            bot.send_message(row[0],"Subscribed to Notifications!")
            con.close()
    else:
        logging.error("Not Authorized to make changes!")
        bot.reply_to(message, "Not Authorized to make changes!")

@bot.message_handler(commands=['block','unallow','disallow','unadmin','demote','kick'])
def block_user(message):
    if isFromAdmin(message):
        username = message.text.split()[1]
        try:
            con = sqlite3.connect("/home/flask/abp-db/chatBot.sqlite3")
        except:
            logging.error("Unable to open DB!")
            bot.reply_to(message, "Unable to Open DB!")
        else:
            try:
                q = con.execute("SELECT * FROM Users WHERE id = ?",[username]).fetchall()
            except Exception as e:
                logging.error("Unable to get matching users")
                bot.reply_to(message, "Unable to get Matching Users")
            else:
                if len(q) == 0:
                    logging.error("No Matching Users!")
                    bot.reply_to(message, "No Matching Users")
                else:
                    try:
                        con.execute("UPDATE Users SET admin = 0, allowed = 0 WHERE id = ?",[username])
                        con.commit()
                    except:
                        logging.error("Unable to Update User")
                        bot.reply_to(message, "Unable to Update User")
                    else:
                        logging.error("Updated User")
                        bot.reply_to(message, "Updated User")
                        for row in q:
                            bot.send_message(row[0],"Subscribed to Notifications!")
            con.close()
    else:
        logging.error("Not Authorized to make changes!")
        bot.reply_to(message, "Not Authorized to make changes!")

@bot.message_handler(commands=['allow'])
def allow_user(message):
    if isFromAdmin(message):
        username = message.text.split()[1]
        try:
            con = sqlite3.connect("/home/flask/abp-db/chatBot.sqlite3")
        except:
            logging.error("Unable to open DB!")
            bot.reply_to(message, "Unable to Open DB!")
        else:
            try:
                q = con.execute("SELECT * FROM Users WHERE id = ?",[username]).fetchall()
            except Exception as e:
                logging.error("Unable to get matching users")
                bot.reply_to(message, "Unable to get Matching Users")
            else:
                if len(q) == 0:
                    logging.error("No Matching Users!")
                    bot.reply_to(message, "No Matching Users")
                else:
                    try:
                        con.execute("UPDATE Users SET allowed = 1 WHERE id = ?",[username])
                        con.commit()
                    except:
                        logging.error("Unable to Update User")
                        bot.reply_to(message, "Unable to Update User")
                    else:
                        logging.error("Updated User")
                        bot.reply_to(message, "Updated User")
                        for row in q:
                            bot.send_message(row[0],"Subscribed to Notifications!")
            con.close()
    else:
        logging.error("Not Authorized to make changes!")
        bot.reply_to(message, "Not Authorized to make changes!")

@bot.message_handler(commands=['help','?'])
def help(message):
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

@bot.message_handler(commands=['start'])
def send_welcome(message):
    d = {
        'from_user_id':         message.from_user.id,
        'from_user_firstName':  message.from_user.first_name,
        'from_user_username':   message.from_user.username, }
    print(d)
    try:
        con = sqlite3.connect("/home/flask/abp-db/chatBot.sqlite3")
        try:
            admins = con.execute("SELECT * FROM Users WHERE admin = 1").fetchall()
        except Exception as e:
            logging.error("Unable to get admins")
        try:
            q = con.execute("SELECT * FROM Users").fetchall()
        except Exception as e:
            logging.error("Unable to get matching users")
        else:
            if len(q) == 0:
                d['noUsers'] = True
        try:
            q = con.execute("SELECT * FROM Users WHERE id = ?",[d['from_user_id']]).fetchall()
        except Exception as e:
            logging.error("Unable to get matching users")
        else:
            if len(q) == 0:
                try:
                    if d.get('noUsers', False):
                        con.execute("INSERT INTO Users (id,firstName,username,admin,allowed) VALUES (?,?,?,?,?)",[
                            d['from_user_id'],
                            d['from_user_firstName'],
                            d['from_user_username'], 
                            1, 
                            1, ])
                    else:
                        con.execute("INSERT INTO Users (id,firstName,username) VALUES (?,?,?)",[
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
                    logging.error("Added User!")
            else:
                try:
                    con.execute("UPDATE Users SET firstName = ?, username = ? WHERE id = ?",[
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
    except Exception as e:
        logging.error("Unable to connect to DB!")
    else:
        con.close()
    if d.get('noUsers',False):
        bot.reply_to(message, "Subscribed to notifications as Administrator!")
    else:
        if d.get('added',False):
            bot.reply_to(message, "Added to UserList, please wait for an admin to authorize your subscription!")
            notify.send("[ABP.chatBot] Added new User!")
            for row in admins:
                bot.send_message(row[0],"To Authorize {}:{}:{}, type /allow {}".format(
                    d['from_user_id'],
                    d['from_user_firstName'],
                    d['from_user_username'],
                    d['from_user_id']))
        if d.get('updated',False):
            bot.reply_to(message, "Updated user info!")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	pass
    # bot.reply_to(message, message.text)

bot.infinity_polling()
