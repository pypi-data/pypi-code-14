class IDExseption(Exception):
    '''
    spicel exception that raise when you enter a wrong id
    '''
    def __init__(self, message="Problem ID entered"):
        Exception(message)

    def __str__(self):
        return super.__str__()

def checkID(id):
    '''
    This function check if you enter a correct Israel ID
    with the default algorithm
    :param id: the person ID must be in length of 7-9
    :return: true if the algorithm find it good candidate for a valid id. false if this is a fake id.
    '''
    srcID=str(id)
    if len(srcID) > 9:
        raise IDExseption("ID must be 9 numbers or less")
    if len(srcID) < 7:
        raise IDExseption("ID must be at less 7 letters")

    while len(srcID)<9:
        srcID = '0'+srcID
    sum=0 ; mul=1
    for i in srcID:
        tmp=int(i)
        tmp *= mul
        if tmp > 9:
            tmp -=9
        sum+=tmp
        if mul==1:
            mul=2
        else:
            mul=1
    return sum % 10 == 0


if __name__ == '__main__':
    print(checkID(31860984))
