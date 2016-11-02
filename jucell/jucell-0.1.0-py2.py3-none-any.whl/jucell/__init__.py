from IPython.display import HTML
import os


def iframe(source, ratio=0.7):
    with open(os.path.dirname(os.path.abspath(__file__)) + "/template.html") as fp:
        con = fp.read()
    con = con.replace("{{time}}", "1").replace("{{ratio}}", str(ratio)).replace("{{path}}", source)
    return HTML(con)