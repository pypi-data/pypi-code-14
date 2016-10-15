import sys
import time
import os

def prnt(rawinp):
    inp=""
    errmsg=''
    def wsrem(rawinp):
        errmsg = ''
        inp = ''
        while len(rawinp) > 0 and errmsg == '':
            if rawinp.startswith("\ "):
                inp=inp+" "
                rawinp=rawinp[2:]
            if rawinp[0]==" ":
                rawinp=rawinp[1:]
            elif rawinp.startswith("\n"):
                rawinp=rawinp[1:]
            elif rawinp.startswith("#"):
                while rawinp[0:2] != '##':
                    rawinp = rawinp[1:]
                rawinp = rawinp[2:]
            else:
                inp=inp+rawinp[0]
                rawinp=rawinp[1:]
        if not inp.lower().startswith("8v"):
            errmsg = ("\n[8var] ERROR: 8var not initialized. ")
            return errmsg
        if not inp.lower().endswith("fin"):
            errmsg = ("\n[8var] ERROR: Unexpected end of file.")
            return errmsg
        return inp
    inp = wsrem(rawinp)
    if inp.startswith("\n"):
        errmsg = inp
    outLines=''
    version=''
    ucFloat=0
    ucode=""
    ucodeInt=0
    outLinesInt=0
    out=''
    delay=""
    intVar=""
    lastInt=0
    curInt=0
    newInt=0
    intFin=0
    checkInt=[False, False, False, False, False, False, False, False]
    varInt=[0, 0, 0, 0, 0, 0, 0, 0]
    lastBool=0
    curBool=0
    newBool=0
    boolFin=0
    checkBool=[False, False, False, False, False, False, False, False]
    varBool=[False, False, False, False, False, False, False, False]
    strVar=""
    lastStr=0
    curStr=0
    newStr=0
    checkStr=[False, False, False, False, False, False, False, False]
    varStr=["", "", "", "", "", "", "", ""]
    strFin=0
    quotes=""
    floatVar=""
    lastFloat=0
    curFloat=0
    newFloat=0
    checkFloat=[False, False, False, False, False, False, False, False]
    varFloat=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    floatFin=0
    add=0
    sub=0

    while len(inp) > 0 and errmsg == '':



        add=0
        sub=0
        ucFloat=0
        quotes=""
        intVar=""
        strVar=""
        floatVar=""
        delay=""



        if newStr != 7:
            while checkStr[newStr] != False and newStr != 8:
                newStr=newStr+1
            if newStr==8:
                strFin=1
        else:
            if checkStr[newStr] != False:
                strFin=1

        if newFloat != 7:
            while checkFloat[newFloat] != False and newFloat != 8:
                newFloat=newFloat+1
            if newFloat==8:
                floatFin=1
        else:
            if checkStr[newStr] != False:
                strFin=1

        if newBool != 7:
            while checkBool[newBool] != False and newBool != 8:
                newBool=newBool+1
            if newBool==8:
                boolFin=1
        else:
            if checkBool[newBool] != False:
                boolFin=1

        if newInt != 7:
            while checkInt[newInt] != False and newInt != 8:
                newInt=newInt+1
            if newInt==8:
                intFin=1
        else:
            if checkInt[newInt] != False:
                intFin=1



        if inp.lower().lower().startswith("int"):
            inp=inp[3:]
            if inp.lower().lower()[0]=="n":
                lastInt=newInt
                if intFin==1:
                    errmsg = ("\n[8var] ERROR: Out of empty variables of type int.")
                if newInt<=7:
                    inp=inp[1:]
                    intVar=""
                    if inp.lower().lower()[0]=="-":
                        sub=1
                        inp=inp[1:]
                    elif inp.lower().lower()[0]=="+":
                        inp=inp[1:]
                    while inp[0] in "0123456789":
                        intVar=intVar+inp[0]
                        inp=inp[1:]
                    if intVar != '':
                        if sub==1:
                            intVar="-"+intVar
                            sub=0
                        varInt[newInt]=int(intVar)
                        checkInt[newInt]=True
                    intVar=""
                else:
                    errmsg = ("\n[8var] ERROR: Out of empty variables of type int.")
            elif inp.lower().lower()[0] in ("01234567l"):
                if inp.lower().lower()[0]=="l":
                    curInt=lastInt
                else:
                    curInt=int(inp[0])
                if 0<=curInt<=8:
                    inp=inp[1:]
                    intVar=""
                    if inp.lower().lower()[0]=="+":
                        inp=inp[1:]
                        add=1
                    elif inp.lower().lower()[0]=="-":
                        inp=inp[1:]
                        sub=1
                    while inp[0] in "0123456789":
                        intVar=intVar+inp[0]
                        inp=inp[1:]
                    if intVar != '':
                        if add==1:
                            varInt[curInt]=varInt[curInt]+int(intVar)
                            add=0
                        elif sub==1:
                            varInt[curInt]=varInt[curInt]-int(intVar)
                            sub=0
                        else:
                            varInt[curInt]=int(intVar)
                        checkInt[curInt]=True
                    intVar=""
                else:
                    errmsg = ("\n[8var] ERROR: Variable doesn't exist.")
            continue



        elif inp.lower().lower().startswith("bool"):
            inp=inp[4:]
            if inp.lower().lower()[0]=="n":
                lastBool=newBool
                if boolFin==1:
                    errmsg = ("\n[8var] ERROR: Out of empty variables of type bool.")
                if newBool<=7:
                    inp=inp[1:]
                    if inp.lower().lower()[0] in "1t0f+-":
                        if inp.lower().lower()[0] in "1t+":
                            varBool[newBool]=True
                        if inp.lower().lower()[0] in "0f-":
                            varBool[newBool]=False
                        checkBool[newBool]=True
                        inp=inp[1:]
                else:
                    errmsg = ("\n[8var] ERROR: Out of empty variables of type bool.")
            elif inp.lower().lower()[0] in "01234567l":
                if inp.lower().lower()[0]=="l":
                    curBool=lastBool
                else:
                    curBool=int(inp[0])
                inp=inp[1:]
                if inp.lower().lower()[0] in "1t0f+-":
                    if inp.lower().lower()[0] in "1t+":
                        varBool[curBool]=True
                    if inp.lower().lower()[0] in "0f-":
                        varBool[curBool]=False
                    checkBool[curBool]=True
                    inp=inp[1:]
            else:
                errmsg = ("\n[8var] ERROR: Variable doesn't exist.")
            continue



        elif inp.lower().lower().startswith("str"):
            inp=inp[3:]
            if inp.lower().lower()[0]=="n":
                lastStr=newStr
                if strFin==1:
                    errmsg = ("\n[8var] ERROR: Out of variables of type str.")
                if newStr<=7:
                    inp=inp[1:]
                    strVar=""
                    while inp[0] != "'" and inp[0] != '"':
                        inp=inp[1:]
                    if inp.lower()[0]=="'":
                        quotes="s"
                    if inp.lower()[0]=='"':
                        quotes="d"
                    inp=inp[1:]
                    if quotes=="s":
                        while inp[0] != "'":
                            strVar=strVar+inp[0]
                            inp=inp[1:]
                    if quotes=="d":
                        while inp[0] != '"':
                            strVar=strVar+inp[0]
                            inp=inp[1:]
                    inp=inp[1:]
                    quotes=""
                    varStr[newStr]=strVar
                    checkStr[newStr]=True
                    strVar=""
                else:
                    errmsg = ("\n[8var] ERROR: Out of variables of type str.")
            if inp.lower()[0] in "01234567l":
                if inp.lower()[0]=="l":
                    curStr=lastStr
                else:
                    curStr=int(inp[0])
                inp=inp[1:]
                strVar=""
                if inp.lower()[0]=="+":
                    add=1
                    inp=inp[1:]
                while inp[0] != "'" and inp[0] != '"':
                    inp=inp[1:]
                if inp.lower()[0]=="'":
                    quotes="s"
                if inp.lower()[0]=='"':
                    quotes="d"
                inp=inp[1:]
                while inp[0] != "'" and inp[0] != '"':
                    strVar=strVar+inp[0]
                    inp=inp[1:]
                inp=inp[1:]
                if add==1:
                    varStr[curStr]=varStr[curStr]+strVar
                    add=0
                else:
                    varStr[curStr]=strVar
                checkStr[curStr]=True
                strVar=""
                continue



        elif inp.lower().startswith("float"):
            inp=inp[5:]
            if inp.lower()[0]=="n":
                lastFloat=newFloat
                if floatFin==1:
                    errmsg = ("\n[8var] ERROR: Out of variables of type float.")
                if newFloat<=7:
                    inp=inp[1:]
                    floatVar=""
                    if inp.lower()[0]=="+":
                        inp=inp[1:]
                    if inp.lower()[0]=="-":
                        sub=1
                        inp=inp[1:]
                    while inp[0] in "0123456789.":
                        floatVar=floatVar+inp[0]
                        inp=inp[1:]
                    if floatVar != '':
                        if sub==1:
                            floatVar="-"+floatVar
                            sub=0
                        varFloat[newFloat]=float(floatVar)
                        checkFloat[newFloat]=True
                    floatVar=""
            if inp.lower()[0] in "01234567l":
                if inp.lower()[0]=="l":
                    curFloat=lastFloat
                else:
                    curFloat=int(inp[0])
                inp=inp[1:]
                if inp.lower()[0]=="+":
                    add=1
                    inp=inp[1:]
                if inp.lower()[0]=="-":
                    sub=1
                    inp=inp[1:]
                while inp[0] in "0123456789.":
                    floatVar=floatVar+inp[0]
                    inp=inp[1:]
                if floatVar != '':
                    if sub==1:
                        varFloat[curFloat]=varFloat[curFloat]-float(floatVar)
                        sub=0
                    elif add==1:
                        varFloat[curFloat]=varFloat[curFloat]+float(floatVar)
                        add=1
                    else:
                        varFloat[curFloat]=float(floatVar)
                    checkFloat[curFloat]=True
                    floatVar=""
            continue



        elif inp.lower().startswith("flt"):
            inp=inp[3:]
            inp="float"+inp
            continue



        elif inp.lower().startswith("dly"):
            inp=inp[3:]
            while inp[0] in "0123456789.":
                delay=delay+inp[0]
                inp=inp[1:]
            time.sleep(float(delay))
            sys.stdout.write("\n")
            delay=""
            continue


        elif inp.lower().startswith("incl"):
            inp = inp[4:]
            inclfilename = ''
            if inp[0] == "'":
                inp = inp[1:]
                while inp[0] != "'":
                    inclfilename = inclfilename + inp[0]
                    inp = inp[1:]
                inp = inp[1:]
            elif inp[0] == '"':
                inp = inp[1:]
                while inp[0] != '"':
                    inclfilename = inclfilename + inp[0]
                    inp = inp[1:]
                inp = inp[1:]
            if not os.path.isfile(inclfilename):
                errmsg = "\n[8var] File " + inclfilename + " not found. "
                break
            else:
                inpincl = open(inclfilename, 'r').read()
            inpincl = wsrem(inpincl)
            if inpincl.startswith("\n"):
                errmsg = inpincl
                break
            else:
                inpincl = inpincl[3:]
                version = version + " --- " + inclfilename + " --- "
                while not inpincl.startswith('v.'):
                    version = version + inpincl[0]
                    inpincl = inpincl[1:]
                inpincl = inpincl[2:]
                inpincl = inpincl[:-3]
                inp = inpincl + inp
                inclfileread = ''
                inpincl = ''

        elif inp.lower().startswith("in"):
            inp = inp[2:]
            if inp.lower()[0:3] in ['int', 'flt']:
                inVar = inp[0:3]
                inp = inp[3:]
                while inp[0] in '01234567ln+-':
                    inVar = inVar + inp[0]
                    inp = inp[1:]
                inp = inVar + raw_input('') + inp
            elif inp.lower()[0:3] == 'str':
                inVar = inp[0:3]
                inp = inp[3:]
                while inp[0] in '01234567ln+-':
                    inVar = inVar + inp[0]
                    inp = inp[1:]
                inp = inVar + '"' + raw_input('') + '"' + inp
            elif inp.lower()[0:4] == 'bool':
                inVar = inp[0:4]
                inp = inp[4:]
                while inp[0] in '01234567ln+-':
                    inVar = inVar + inp[0]
                    inp = inp[1:]
                inp = inVar + raw_input('') + inp
            elif inp.lower()[0:5] == 'float':
                inVar = inp[0:5]
                inp = inp[5:]
                while inp[0] in '01234567ln+-':
                    inVar = inVar + inp[0]
                    inp = inp[1:]
                inp = inVar + raw_input('') + inp

        elif inp.lower().startswith("out"):
            inp=inp[3:]
            if inp.lower()[0]=="'":
                inp=inp[1:]
                while inp[0] != "'":
                    sys.stdout.write(inp[0])
                    inp=inp[1:]
                inp=inp[1:]
            elif inp.lower()[0]=='"':
                inp=inp[1:]
                while inp[0] != '"':
                    sys.stdout.write(inp[0])
                    inp=inp[1:]
                inp=inp[1:]
            elif inp.lower().startswith("int"):
                inp=inp[3:]
                if inp.lower()[0] in "01234567l":
                    if inp.lower()[0]=="l":
                        sys.stdout.write(str(varInt[int(lastInt)]))
                    else:
                        sys.stdout.write(str(varInt[int(inp[0])]))
                    inp=inp[1:]
                else:
                    errmsg = ("\n[8var] ERROR: Variable doesn't exist.")
                    break
            elif inp.lower().startswith("float"):
                inp=inp[5:]
                if inp.lower()[0] in "01234567l":
                    if inp.lower()[0]=="l":
                        sys.stdout.write(str(varFloat[int(lastFloat)]))
                    else:
                        sys.stdout.write(str(varFloat[int(inp[0])]))
                    inp=inp[1:]
                else:
                    errmsg = ("\n[8var] ERROR: Variable doesn't exist.")
                    break
            elif inp.lower().startswith("flt"):
                inp=inp[3:]
                if inp.lower()[0] in "01234567l":
                    if inp.lower()[0]=="l":
                        sys.stdout.write(str(varFloat[int(lastFloat)]))
                    else:
                        sys.stdout.write(str(varFloat[int(inp[0])]))
                    inp=inp[1:]
                else:
                    errmsg = ("\n: Variable doesn't exist.")
            elif inp.lower().startswith("str"):
                inp=inp[3:]
                if inp.lower()[0] in "01234567l":
                    if inp.lower()[0]=="l":
                        sys.stdout.write(str(varStr[int(lastStr)]))
                    else:
                        sys.stdout.write(str(varStr[int(inp[0])]))
                    inp=inp[1:]
                else:
                    errmsg = ("\n[8var] ERROR: Variable doesn't exist.")
            elif inp.lower().startswith("bool"):
                inp=inp[4:]
                if inp.lower()[0] in "01234567l":
                    if inp.lower()[0]=="l":
                        sys.stdout.write(str(varBool[int(lastBool)]))
                    else:
                        sys.stdout.write(str(varBool[int(inp[0])]))
                    inp=inp[1:]
                else:
                    errmsg = ("\n[8var] ERROR: Variable doesn't exist.")
            elif inp.lower()[0] in "0123456789":
                while inp[0] in "0123456789.":
                    sys.stdout.write(inp[0])
                    inp=inp[1:]
            elif inp.lower().startswith("ln"):
                inp=inp[2:]
                outLines=""
                if inp.lower()[0] in "0123456789":
                    while inp[0] in "0123456789":
                        outLines=outLines+inp[0]
                        inp=inp[1:]
                else:
                    outLines="1"
                outLinesInt=int(outLines)
                outLines=""
                while outLinesInt>0:
                    sys.stdout.write("\n")
                    outLinesInt=outLinesInt-1
                outLinesInt=0
            continue



        elif inp.lower().startswith("uout"):
            inp=inp[4:]
            if inp.lower()[0] in "0123456789":
                while inp[0] in "0123456789":
                    ucode=ucode+inp[0]
                    inp=inp[1:]
            elif inp.lower().startswith("int"):
                inp=inp[3:]
                if inp.lower()[0] in "01234567":
                    ucode=varInt[int(inp[0])]
                    inp=inp[1:]
                elif inp.lower()[0]=="l":
                    ucode=varInt[lastInt]
                    inp=inp[1:]
            elif inp.lower().startswith("fl"):
                inp=inp[2:]
                if inp.lower().startswith("oat"):
                    ucFloat=1
                    inp=inp[3:]
                elif inp.lower()[0]=="t":
                    ucFloat=1
                    inp=inp[1:]
                if ucFloat==1:
                    ucFloat=0
                    if inp.lower()[0] in "01234567":
                        ucode=varFloat[int(inp[0])]
                        inp=inp[1:]
                    elif inp.lower()[0]=="l":
                        ucode=varInt[lastInt]
                        inp=inp[1:]
            ucodeInt=int(ucode)
            ucode=""
            sys.stdout.write(chr(ucodeInt))
            ucodeInt=0
            continue

        elif inp.lower().startswith("fin"):
            inp=inp[3:]
            sys.stdout.write("\n")
            sys.stdout.flush()
            continue

        elif inp.lower().startswith("8v"):
            inp=inp[2:]
            while not inp.startswith("v."):
                version=version+inp[0]
                inp=inp[1:]
            inp=inp[2:]
            version=version.lower()

        else:
            inp=inp[1:]
            continue
    if errmsg != '':
        return errmsg
        errmsg = ''
    else:
        return ''
