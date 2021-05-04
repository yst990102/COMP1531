def cipher(Key, Message):
    key_list = [x for x in Key]
    sorted_key_list = sorted(key_list)

    Message = filter(str.isalpha, Message)
    message_list = [x for x in Message]

    # supplementary filled char a-z when there are vacant cells
    a_z_list = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    message_list += a_z_list[: sup_num(len(key_list), len(message_list))]

    # turn key_list into sequencial_numbers
    sequencial_key_list = []
    for i in key_list:
        sequencial_key_list.append(sorted_key_list.index(i))
        sorted_key_list[sorted_key_list.index(i)] = ""

    # get the encoded_list
    encoded_list = []
    for i in range(0, len(sequencial_key_list)):
        column_num = sequencial_key_list.index(i)
        Index = column_num
        while Index < len(message_list):
            encoded_list.append(message_list[Index])
            Index += len(sequencial_key_list)

    # transfer list into string then return
    return "".join(encoded_list)


def sup_num(len_key, len_message):
    if len_message % len_key == 0:
        return 0
    else:
        return len_key - (len_message % len_key)


if __name__ == "__main__":
    print(cipher("zebras", "we are discovered. flee at once."))
