import sys
import os
import collections
import re
import syntax
#from iteration_utilities import deepflatten

flag = 0

def flatten(L):
    
    if len(L) == 1:
        if type(L[0]) == list:
            result = flatten(L[0])
        else:
            result = L
    elif type(L[0]) == list:
        result = flatten(L[1:])
        result = flatten(L[0]) + result
    else:
        result = flatten(L[1:])
        result = [L[0]] + result
    return result

def listToString(s):

    # initialize an empty string
    str1 = " "
    s1=flatten(s)
    # return string
    return (str1.join(s1))


def eval_term(t):
    if t == 'true' or t == True:
        return 'true'
    elif t == 'false' or t == False:
        return 'false'
    elif t == '0':
        return '0'

    elif t[0] == 'succ' and t[1] == '0':
        return 'succ 0'
    if t[0] == 'iszero':

        val = (eval_term(t[1]))
        if (val == 0 or val == '0'):
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
        if s == 0 or s == '0':
            return '0'
        elif s[:4] == 'succ' and s[-1] == '0':
            return s[5:]
        else:
            s = ['pred', str(s)]
            return (listToString(s))
    elif t[0] == 'and':
        t1 = eval_term(t[1])
        t2 = eval_term(t[2])
        t3 = eval_term(t[3])
        b = ['true', 'false']
        if t1 in b and t2 in b and t2 in b:
            t1 = True if t1 == "true" else False
            t2 = eval_term(t[2])
            t3 = eval_term(t[3])
            t2 = True if t2 == "true" else False
            t3 = True if t3 == "true" else False
            m = t1 and (t2 or(not t3)) 
            m = "true" if m == True else "false"
            return m
        else:
            ch = 0

            if t3 in b:
                t3 = True if t3 == "true" else False
                ch = 1
                v = not t3
                res = "true" if v == True else "false"
            else:
                res = "not"+" ( "+t3+" ) "

            if t2 in b:
                if ch == 1:
                    t2 = True if t2 == "true" else False
                    v = t2 or v
                    res = "true" if v == True else "false"
                else:
                    res = "or"+" ( "+t2+" ) "+res
            else:
                ch = 0
                res = "or"+" ( "+t2+" ) "+res

            if t1 in b:
                if ch == 1:
                    t1 = True if t1 == "true" else False
                    v = t1 and v
                    res = "true" if v == True else "false"
                else:
                    res = "and"+" ( "+t1+" ) "+res
            else:
                res = "and"+" ( "+t1+" ) "+res

            return res

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
            elif(t[2] == "0"):
                two = "0"
            else:
                two = listToString(t[2])

            if(t[3] == "true" or t[3] == "false"):
                three = t[3]
            elif(t[3] == "0"):
                three = "0"
            else:
                three = listToString(t[3])
            
            return (t[0]+" ( "+val+" ) "+"then"+" ( "+two+" ) "+"else"+" ( "+three+" ) ")
    else:
        return listToString(t)
