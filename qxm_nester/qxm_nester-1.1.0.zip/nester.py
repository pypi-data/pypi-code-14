def function(para, para2):
    for obj in para:
        if isinstance(obj, list):
            function(obj, para2+1)
        else:
            for tab_stop in range(para2):
                print("\t", end='')
            print(obj)

movie = ["海贼王", "1997年", "760集", ["尾田荣一郎", ["路飞", "娜美", "乔巴"]]]
function(movie, 0)
