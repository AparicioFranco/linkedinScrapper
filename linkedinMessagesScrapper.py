import time
import config
from supabase import create_client

from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()
driver.get("https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
database_url = config.SUPABASE_URL
database_key = config.SUPABASE_PASSWORD
supabase = create_client(database_url, database_key)
time.sleep(5)

# Put credentials into the login
username = driver.find_element(By.ID, "username")
username.send_keys(config.USERNAME)
password = driver.find_element(By.ID, "password")
password.send_keys(config.PASSWORD)

# Click the log in button
driver.find_element("xpath", '//*[@id="organic-div"]/form/div[3]/button').click()
time.sleep(15)

# Click the message tab on top
driver.find_element("xpath", '//*[@id="global-nav"]/div/nav/ul/li[4]/a').click()
time.sleep(5)

# Finds the ul container with all the conversations on the left
conversations_container = driver.find_element("xpath", '/html/body/div[5]/div[3]/div[2]/div/div/main/div/div[1]/div[2]/ul')


# Creates a list of all messages conversations, and pops the first element because it is always null
conversation_list = conversations_container.find_elements(By.TAG_NAME, "li")

# Pops the first element because is always null
conversation_list.pop(0)

# Loops by each conversation
for conversation in conversation_list:
    # Clicks on that conversation to open the messages
    conversation.click()

    # Creates a new conversation in the database and store the chat_id for later
    create_chat_response = supabase.table('chat').insert({}).execute()
    chat_id = create_chat_response.data[0].get('chat_id')
    time.sleep(5)

    # Checks if it is a promotion, and skips it
    if len(driver.find_elements(By.CLASS_NAME, "msg-sponsored-conversation-thread")) > 0:
        continue

    # Other type of promotion
    if len(driver.find_elements(By.CLASS_NAME, "msg-spinmail-thread-presenter__message")) > 0:
        continue

    # Saves the message list to iterate later
    messageList = driver.find_element(By.CLASS_NAME, "msg-s-message-list-content")

    # Filters only the messages that have text in them
    messageListMessages = messageList.find_elements(By.CLASS_NAME, '''msg-s-message-list__event''')

    # Click on the first message, so we can load all the conversation
    messageListMessages[0].click()

    # A variable so we know who was the past user, because not all messages have a user associated.
    pastUser = ''

    # We create two empty list, so we can add the users and messages to it for later
    userList = []
    messageList = []
    for message in messageListMessages:
        time.sleep(1)

        # Check if the message have a username attached to it
        if len(message.find_elements(By.CLASS_NAME, "msg-s-message-group__profile-link")) != 0:
            username = message.find_elements(By.CLASS_NAME, "msg-s-message-group__profile-link")[0].get_attribute(
                'innerHTML').strip()
            pastUser = username

        # Stores the particular message in a variable
        particularMessage = message.find_element(By.CLASS_NAME, "msg-s-event-listitem__body").text

        # Append the user and the message to the respective lists
        userList.append(username)
        messageList.append(particularMessage)

    # Zip the lists together, so we can have two tuples with the user in the first position and the message in the second
    user_message_list = list(zip(userList, messageList))

    # Iterate the user_message_list, so we can save the conversations in the database
    for messages_tuple in user_message_list:
        tuple_username = messages_tuple[0]
        tuple_message = messages_tuple[1]

        # Checks if the username exists, if it doesn't, it creates a new one, and stores its id for the database
        username_response = supabase.table('chat_user').select('*').eq('username', tuple_username).execute()
        if len(username_response.data) == 0:
            create_user_response = supabase.table('chat_user').insert({'username': tuple_username}).execute()
            user_id = create_user_response.data[0].get('chat_user_id')
        else:
            user_id = username_response.data[0].get('chat_user_id')

        # Insert the message with the user_id and the chat_id to the database
        supabase.table('chat_line').insert(
            {'chat_user_id': user_id, 'chat_id': chat_id, 'line_text': tuple_message}).execute()
