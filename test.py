A_UPPERCASE = ord('A') # returns 69 as A in ascii is 69th.
ALPHABET_SIZE = 26


def _decompose(number):
    """Generate digits from `number` in base alphabet, most significants
    bits first.
    """

    number -= 1  # Account for A in base alphabet being 1 in decimal rather than 0
    if number < ALPHABET_SIZE:
        yield number
    else:
        number, remainder = divmod(number, ALPHABET_SIZE)
        yield from _decompose(number)
        yield remainder


def base_10_to_alphabet(number):
    """Convert a decimal number to its base alphabet representation"""

    return ''.join(
            chr(A_UPPERCASE + part)
            for part in _decompose(number)
    )


def base_alphabet_to_10(letters):
    """Convert an alphabet number to its decimal representation"""

    return sum(
            (ord(letter) - A_UPPERCASE + 1) * ALPHABET_SIZE**i
            for i, letter in enumerate(reversed(letters.upper()))
    )

input_value = "a"
print("input: ", input_value)
output_num = base_alphabet_to_10(input_value)
print("output number: ", output_num)
output_on_num = base_10_to_alphabet(output_num)
print("output based on number: ", output_on_num)

alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
alphabet_length = len(alphabet)

def _decompose2(number):
    """Generate digits from `number` in base alphabet, most significants
    bits first.
    """

    # number -= 1  # Account for A in base alphabet being 1 in decimal rather than 0
    if number < alphabet_length:
        yield number
    else:
        number, remainder = divmod(number, alphabet_length)
        yield from _decompose2(number)
        yield remainder

def base_10_to_alphabet2(number):
    """Convert a decimal number to its base alphabet representation"""
    letter_combined = ''
    for part in _decompose2(number):
        letter_combined = letter_combined + alphabet[(part-1)]
    return letter_combined
    # return ''.join(
    #         alphabet[part]
    #         for part in _decompose2(number)
    # )

def base_arr_to_10(letters):
    """Convert an alphabet to its decimal representation based on a dictionary"""
    letters_num = 0
    for i, letter in enumerate(reversed(letters)):
        letters_num += (alphabet.index(letter) + 1) * alphabet_length**i

    return letters_num

test_input = "abcde"
print("test input: ", test_input)
test_output = base_arr_to_10(test_input)
print("a># output: ", test_output)
test_output2 = base_10_to_alphabet2(test_output)
print("#>a output: ", test_output2)