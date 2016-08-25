from slackbot.bot import respond_to
import re
import store
import logging

@respond_to("help",re.IGNORECASE)
def help(message):
    message.reply("""Commands: help, why, register, emergency

    Example: why
    Example: register Wife (Helen): 555-555-5555 Local PD (Toronto, Division 54): 555-555-5555
    Example: emergency @someuser
    """)

@respond_to("why",re.IGNORECASE)
def why(message):
    message.reply("""This bot was created by Surge Consulting in response to the tragic events
    on 2016-08-24. In memory of Simon Hancock.
    """)

@respond_to("register (.*)",re.IGNORECASE)
def register(message,contactString):
    user = message._client.users[message._body['user']]
    store.register(user,contactString)
    contactString = store.get(user['id'])
    message.reply("Stored '{0}' for {1}".format(contactString,user['name']))
    message.reply("If this does not look correct, try again")

def _get_user_by_id(message,userid):
    for _,user in message._client.users.iteritems():
        if user['id'] == userid:
            return user

# emergency requests for user
g_emergencies = set()

@respond_to("emergency <@(.*)>",re.IGNORECASE)
def emergency(message,userid):
    logging.info("Emergency for {}".format(userid))
    if userid not in g_emergencies:
        g_emergencies.add(userid)
        message.reply("""If this is an emergency, please request again. Otherwise note that this
        information should not be used for any other purposes and requests will
        be logged to maintain privacy.""")
    else:
        g_emergencies.remove(userid)
        contact = store.get(userid)
        response = "Emergency info: {}".format(contact)
        message.reply(response)
        req_user = _get_user_by_id(message,message._body['user'])
        message.reply("Access by {} recorded".format(req_user['name']))
