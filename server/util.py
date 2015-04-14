""" Utility methods. """

num2words = {1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five',
             6: 'Six', 7: 'Seven', 8: 'Eight', 9: 'Nine', 10: 'Ten',
             11: 'Eleven', 12: 'Twelve', 13: 'Thirteen', 14: 'Fourteen',
             15: 'Fifteen', 16: 'Sixteen', 17: 'Seventeen', 18: 'Eighteen',
             19: 'Nineteen', 20: 'Twenty', 30: 'Thirty', 40: 'Forty',
             50: 'Fifty', 60: 'Sixty', 70: 'Seventy', 80: 'Eighty',
             90: 'Ninety', 0: 'Zero'}


def number_to_words(n):
    """ Convert a number to the word representation. """
    try:
        return num2words[n]
    except KeyError:
        return num2words[n-n % 10] + num2words[n % 10].lower()


def format_grid(grid, should_print=False):
    """ Print out a grid in a readable format. """
    output = ""

    height = len(grid[0])
    width = len(grid)

    for y in range(height):
        row = []
        for x in range(width):
            row.append(str(grid[x][y]))
        output += '\t'.join(row) + "\n"

    # Remove final newline
    output = output[:-1]

    if should_print:
        print "\n" + output + "\n"
    return output
