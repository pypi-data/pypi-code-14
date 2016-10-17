import crabmd as mistune


def test_box():
    ret = mistune.markdown('{{box!s:\ns\nbox!s}}', escape=True)
    raise ValueError(ret)
    assert false
 

 


