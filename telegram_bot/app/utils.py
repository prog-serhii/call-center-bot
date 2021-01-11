import re


def phone_control(number_of_phone):
    # провіряє чи заданий текст є номером телефону
    pattern = re.compile(r'^(\+)?(\(\d{2,3}\) ?\d|\d)(([ \-]?\d)|( ?\(\d{2,3}\) ?)){5,12}\d$')

    if pattern.search(number_of_phone):
        # видаляємо всі лишні символи
        number_of_phone = number_of_phone.replace('(', '')
        number_of_phone = number_of_phone.replace(')', '')
        number_of_phone = number_of_phone.replace('-', '')
        number_of_phone = number_of_phone.replace(' ', '')

        return number_of_phone
    else:
        return None
