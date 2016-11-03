
# foo outside comment
def foo(a, b):
    print a + b
    # foo inside comment
    return a + b


# bar outside comment
def bar(a):
    print a
    # bar inside comment
    a += 1
    return a