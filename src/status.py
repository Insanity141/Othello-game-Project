current_meesage = "Game started"
previous_message = ""

def update_status(message):

    global current_meesage, previous_message

    previous_message = current_meesage
    current_meesage = message

def get_status():
    return current_meesage, previous_message

