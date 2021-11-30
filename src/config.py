# Important Stuff, change before running
SQLITE3_DB_PATH = "./chatBot.sqlite3" # SQLITE3 Database Path
API_TOKEN = 'YOUR-API-TOKEN-HERE' # API Token from @BotFather
API_URL = f"https://api.telegram.org/bot{API_TOKEN}" # You might change this if you are running your own server
# Methods
ALLOW_MEHTODS =     ['allow',]
UNALLOW_METHODS =   ['unallow','disallow','kick','block',]
PROMOTE_METHODS =   ['admin','promote',]
DEMOTE_METHODS =    ['unadmin','demote',]
GET_USERS_METHODS = ['users',]
HELP_METHODS =      ['?','h','help']
START_METHODS =     ['start',]
REQUIRES_ADMIN_METHODS = (
    ALLOW_MEHTODS + 
    UNALLOW_METHODS + 
    PROMOTE_METHODS + 
    DEMOTE_METHODS)
# SQL Commands
SQL_INIT =                          """CREATE TABLE IF NOT EXISTS Users (
                                            id INTEGER NOT NULL UNIQUE PRIMARY KEY, 
                                            firstName TEXT, 
                                            username TEXT, 
                                            admin BOOLEAN, 
                                            allowed BOOLEAN) WITHOUT ROWID;"""
SQL_ADMIN_USERS =                   "SELECT * FROM Users WHERE admin = 1"
SQL_ALL_USERS =                     "SELECT * FROM Users"
SQL_IS_ADMIN =                      "SELECT admin FROM Users WHERE id = ?"
SQL_MATCHING_USERS =                "SELECT * FROM Users WHERE id = ?"
SQL_ALLOW_USER =                    "UPDATE Users SET allowed = 1 WHERE id = ?"
SQL_UNALLOW_USER =                  "UPDATE Users SET allowed = 0, admin = 0 WHERE id = ?"
SQL_PROMOTE_USER =                  "UPDATE Users SET admin = 1 WHERE id = ?"
SQL_DEMOTE_USER =                   "UPDATE Users SET admin = 0 WHERE id = ?"
SQL_INSERT_ADMIN =                  "INSERT INTO Users (id,firstName,username,admin,allowed) VALUES (?,?,?,1,1)"
SQL_INSERT_USER =                   "INSERT INTO Users (id,firstName,username) VALUES (?,?,?)"
SQL_UPDATE_USER =                   "UPDATE Users SET firstName = ?, username = ? WHERE id = ?"
# Strings
STRING_ADDED_USER =                 "Added User!"
STRING_ADMIN_SUBSCRIBED =           "Subscribed to notifications as Administrator!"
STRING_AUTH_SUGGEST =               "To Authorize {}:{}:{}, type /allow {}"
STRING_DEMOTED =                    "You have been demoted"
STRING_MODIFIED_USER =              "Updated User"
STRING_PROMOTED =                   "You have been promoted to an Administrator"
STRING_SUBSCRIBED =                 "You are Subscribed"
STRING_UNSUBSCRIBED =               "You are Unsubscribed"
STRING_UPDATED_SELF =               "Updated User Info!"
STRING_WAIT_FOR_AUTH =              "Added to UserList, please wait for an admin to authorize your subscription!"
STRING_ERROR_OPENING_DB =           "Unable to open DB: {}"
STRING_ERROR_USER_DOESNT_EXIST =    "Unable to get matching users"
STRING_ERROR_USER_NO_MATCH =        "No Matching Users!"
STRING_ERROR_USER_UNABLE =          "Unable to Update User: {}"
STRING_ERROR_NOT_AUTHORIZED =       "You are NOT AUTHORIZED to make changes!"
STRING_ERROR_NO_ADMINS =            "Unable to get Admins: {}"
STRING_ERROR_NO_USERS =             "Unable to get Users: {}"
STRING_ERROR_NO_ID =                "No ID Provided"
STRING_ERROR_HELP =                 "ERROR Sending Help Info: {}"
STRING_ERROR_INIT_DB =              "ERROR Initializing DB: {}"
