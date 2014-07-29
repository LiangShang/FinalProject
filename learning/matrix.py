import random
import multiprocessing
from itertools import starmap, izip, repeat, imap
from operator import mul
import sys


def calc_row_of_product_matrix(a_row, b, izip=izip):
    '''Calculate a row of the product matrix P = A * B
    Arguments:
      a_row is af A
      b is the B matrix
    returns the corresponding row of P matrix'''
    return map(lambda col: sum(starmap(mul,izip(a_row,col))), izip(*b))

def eval_func_tuple(f_args):
    '''Takes a tuple of a function and args, evaluates and returns result'''
    return f_args[0](*f_args[1:])

class multimatrix(list):



    def __init__(self, iterable=None, cpu=1):
        super(multimatrix, self).__init__(iterable)
        self.cpu = cpu #multiprocessing.cpu_count()

    def __mul__(self, b, izip=izip, repeat=repeat):
        '''Concurrent matrix multiplication with multiprocessing.Pool. '''
        pool = multiprocessing.Pool(self.cpu)
        return pool.map(eval_func_tuple, izip(repeat(calc_row_of_product_matrix), self, repeat(b)))

class itermatrix(list):

    @staticmethod
    def sumprod(row, col, sum=sum, starmap=starmap, mul=mul):
        '''Returns sumproduct of two vectors.'''
        return sum(starmap(mul,izip(row,col)))

    def __mul__(self, b, imap=imap, izip=izip):
        '''Matrix multiplication returning iterable of iterables'''
        return imap(lambda row: imap(lambda col: itermatrix.sumprod(row, col), izip(*b)), self)

def iterate_results(result):
    '''Iterate over iterable of iterables,
    and returns elements in list of lists.
    Usage: if you want to run the whole calculation at once:
    p = iterate_results(itermatrix([[1, 3], [-5, 6], [2, 4]]) * itermatrix([[1, 4], [8, 7]]))'''
    return[[col for col in row] for row in result]

def random_v(K=1000,min=-1000,max=1000):
    '''Generates a random vector of dimension N;
    Returns a list of integers.
    The values are integers in the range [min,max].'''
    return [random.randint(min,max) for k in range(K)]

def random_m(N=1000, K=1000):
    '''Generates random matrix. Returns list of list of integers.'''
    return [random_v(K) for n in range(N)]

def print_matrix(matrix, file_name):
    f = open(file_name, "w")
    for line in matrix:
        f.write("\t".join(map(str, line)) + "\n")

def read_matrix(file_name):
    lines = open(file_name, "r").read().splitlines()
    matrix = []
    for line in lines:
        matrix.append(map(int, line.split("\t")))
    return matrix

if __name__ == "__main__":
    matrix = random_m(int(sys.argv[1]), int(sys.argv[1]))
    print_matrix(matrix, "matrix_"+sys.argv[1])

    #matrix = read_matrix("matrix_100")
    #print matrix
