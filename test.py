import itertools

def generate(string):
    output = []
    for i in itertools.product("abcd", repeat=2):
        output.append("".join(i))
    return output


print(generate("...."))
# print(generate("..."))
