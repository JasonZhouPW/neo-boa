

def Main(operation, args):
    if operation == 'test':
        return test()
    return False

def test():
    arr = [1, 2, 3, 4, 5]
    Log