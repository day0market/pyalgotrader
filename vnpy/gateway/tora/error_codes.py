error_codes = {
    0: " no error ",
    -1: "TCP connection not established ",
    -2: " invalid interaction channel ",
    -3: " the user is not logged in ",
    -4: " this non-pre-session can not subscribe to a private stream ",
    -5: " repeat private stream subscription request ",
    -6: " private file failed to open stream ",
    -7: " internal communication error ",
    -8: " failed to create session channel ",
    -9: " beyond the flow control restrictions ",
}


def get_error_msg(error_code: int):
    try:
        return error_codes[error_code]
    except KeyError:
        return " unknown mistake "
