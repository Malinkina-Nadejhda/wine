def get_year_string(age):
    if 11 <= age % 100 <= 14:
        return  "лет"
    last_digit = age % 10
    if last_digit == 1:
        return "год"
    elif last_digit in(2, 3, 4):
        return "года"
    else:
        return "лет"
