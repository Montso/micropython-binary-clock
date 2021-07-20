"""
Convert decimal to BCD
returns tuple with each digit as tuple item
"""
def BCDConversion(n) :
    if n < 10: 
      bcd = ["0000"] #leading zero bcd for numbers less than zero
    else:
      bcd = []

    str_repr = str(n) #int to string to allow indexing
    for digit in str_repr:
      """4bit binary representation of each number. Store it in a list of len 2"""
      binary = "{:04b}".format(int(digit))
      bcd.append(binary)
    return tuple(bcd)
