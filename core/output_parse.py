__author__ = 'Sherlock'

SPLITTER = ","

def parse(string):
    #first split the string
    overheads = string.split(SPLITTER)

    #and then put each part of the string into the file
    f = open("result", "a")

    for overhead in overheads:
        f.write(overhead.strip()+'\n')

if __name__ == '__main__':
    parse("123, 345,334,234")