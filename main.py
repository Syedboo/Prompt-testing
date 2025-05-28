def location2index(loc: str) -> tuple[int, int]:
    '''converts chess location to corresponding x and y coordinates'''
    column = ord(loc[0]) - ord('a') + 1
    row = int(loc[1:])
    return (column, row)

def index2location(x: int, y: int) -> str:
    '''converts  pair of coordinates to corresponding location'''
    column = chr(x + ord('a') - 1)
    row = str(y)
    return column + row
