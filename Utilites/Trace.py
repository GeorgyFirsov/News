# This module performs debugging log


def trace(string: str, state: bool, file: str = 'stdout'):
    """Prints passed message on screen
    or writes it to a specified file

    :param string: message to display
    :param state: if False, no output performed
    :param file: write destination
    """

    message = 'Debugging message: ' + string + '\n'
    if state and file == 'stdout':
        print(message, end='')
    elif state and file != 'stdout':
        with open(file, 'w') as log:
            log.write(message)
