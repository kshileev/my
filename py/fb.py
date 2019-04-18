import string
alphabet = {x[0]: x[1] for x in enumerate(string.ascii_lowercase)}


def decode(enc):
    if not enc:
        return 0
    elif len(enc) == 1:
        print(alphabet[enc[0]])
        return 1
    elif len(enc) == 2:
        print(alphabet[enc[0]], alphabet[enc[1]])
        second_variant = 10 * enc[0] + enc[1]
        if second_variant <= 25:
            print(alphabet[second_variant])
            return 2
        else:
            return 1
    else:
        return decode(enc[:1]) + decode(enc[1:])

print ('n=', decode([1, 1, 1, 1]))