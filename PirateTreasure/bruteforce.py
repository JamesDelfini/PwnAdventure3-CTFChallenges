from itertools import chain, product

# https://stackoverflow.com/a/11747419

def bruteforce(charset, maxlength):
    return (''.join(candidate)
            for candidate in chain.from_iterable(product(charset, repeat=i)
                                                 for i in range(1, maxlength + 1)))


print(list(bruteforce('abcde', 2)))

# attempt - the characters
# for attempt in bruteforce(string.ascii_lowercase, 10):
#     # match it against your password, or whatever
#     if matched:
#         break
