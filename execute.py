import sys
import os
import collections
import re
import syntax

flag = 0


def listToString(s):

    # initialize an empty string
    str1 = " "

    # return string
    return (str1.join(s))


def eval_term(t):
    if t == 'true':

        return t
    elif t == 'false':

        return t
    elif t == 'zero':
        return 0
    elif t[0] == 'succ' and t[1] == 'zero':
        return 'succ 0'
    if t[0] == 'iszero':

        val = (eval_term(t[1]))
        if (val == 0 or val == ' 0'):
            return 'true'
        elif val[-4:] == "true" or val[-5:] == "false":
            s = ['iszero', str(val)]
            return listToString(s)
        elif flag == 1 or val == "true" or val == "false":
            s = ['iszero', str(val)]
            return (listToString(s))

        else:
            return 'false'

    elif t[0] == 'succ':
        val = (eval_term(t[1]))
        s = ['succ', str(val)]
        return (listToString(s))
    elif t[0] == 'pred':
        s = (eval_term(t[1]))
        if s == 0:
            return 0
        elif s[:4] == 'succ' and s[-1] == '0':
            return s[4:]
        else:
            s = ['pred', str(s)]
            return (listToString(s))
    elif t[0] == 'if':
        val = eval_term(t[1])
        if val == 'true':
            return eval_term(t[2])
        elif val == 'false':
            return eval_term(t[3])
        else:
            two = ""
            three = ""
            if(t[2] == "true" or t[2] == "false"):
                two = t[2]
            else:
                two = listToString(t[2])
            if(t[3] == "true" or t[3] == "false"):
                three = t[3]
            else:
                three = listToString(t[3])
            
            return (t[0]+" "+val+" "+"then"+" "+two+" "+"else"+" "+three)
    else:
        return listToString(t)
