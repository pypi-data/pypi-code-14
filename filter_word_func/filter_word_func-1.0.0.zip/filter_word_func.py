def list_word(fname):
    fh = open(fname)
    lst = list()
    for line in fh:
        l = line.split()#loop through every line of the file, and convert the line into list of word
        for word in l:
            if word not in lst:#find word in the list lst or not
                lst.append(word)#if word not in lst, put the word in lst
    lst.sort()
    print lst