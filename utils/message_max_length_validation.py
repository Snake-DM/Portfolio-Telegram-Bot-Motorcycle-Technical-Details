MESSAGE_MAX_LENGTH = 4096

def message_max_length(text):
    valid_message = text[:4096]
    tail_message = text[4096:]
    return valid_message, tail_message
