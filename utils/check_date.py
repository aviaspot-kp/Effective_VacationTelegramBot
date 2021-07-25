from datetime import datetime


def check_date(user_input):
    try:
        day, month = user_input.split('.')
    except ValueError:
        return 'error'

    try:
        if datetime.now() < datetime(
                int(datetime.now().year),
                int(month),
                int(day)):
            return user_input, datetime.now().year
    except ValueError:
        pass

    try:
        datetime(
            int(datetime.now().year + 1),
            int(month),
            int(day))
        return user_input, datetime.now().year + 1
    except ValueError:
        pass

    return 'error'
