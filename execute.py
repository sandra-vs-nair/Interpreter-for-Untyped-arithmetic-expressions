import collections
import syntax

#Global variable to mark stuck terms
#If flag is equal to 1, the term is a stuck term
flag = 0

#Flatten nested list to single list
def flatten(L):
    if(type(L) != list):
        return [L]
    if len(L) == 1:
        if type(L[0]) == list:
            result = flatten(L[0])
        else:
            result = L
    elif type(L[0]) == list:
        result = flatten(L[1:])
        result = flatten(L[0]) + result
    else:
        if L[0] == "if":
            res1 = flatten(L[1])
            res2 = flatten(L[2])
            res3 = flatten(L[3])
            result = ["if", "("] + res1 + [")", "then", "("] + \
                res2 + [")", "else", "("]+res3+[")"]
            return result
        elif L[0] == "and":
            res1 = flatten(L[1])
            res2 = flatten(L[2])
            res3 = flatten(L[3])
            result = ["and", "("] + res1 + [")", "or", "("] + \
                res2 + [")", "not", "("]+res3+[")"]
            return result
        else:
            result = flatten(L[1:])
            result = [L[0],"("] + result + [")"]
    return result

#Convert nested list to string
def listToString(s):

    if isinstance(s, (str)):
        return s
    # initialize an empty string
    str1 = ""
    s1 = flatten(s)
    # return string
    return (str1.join(s1))

#Starts evaluation
def evaluation(t):
    global flag
    flag = 0
    ls = eval_term(t)
    return listToString(ls)

#Recursive function
def eval_term(t):
    global flag 
    
    if t == ['true'] or t == ['false'] or t == ['0']:
        return t

    #iszero t
    elif t[0] == 'iszero':
        val = (eval_term(t[1]))
        if flag == 1:
            return ['iszero',val]
        if (val == ['0']):
            return ['true']
        elif val[0]  == 'succ':
            return ['false']
        else:
            s = ['iszero', val]
            flag = 1
            return s

    #succ t
    elif t[0] == 'succ':
        val = (eval_term(t[1]))
        if flag == 1:
            return ['succ',val]
        if val == ['true'] or val == ['false']:
            s = ['succ', val]
            flag = 1
            return s
        else:
            s = ['succ', val]
            return s
    
    #pred t
    elif t[0] == 'pred':
        val = (eval_term(t[1]))
        if flag == 1:
            return ['pred',val]
        if val == ['0']:
            return ['0']
        elif val[0] == 'succ':
            s = val[1:]
            return s
        else:
            s = ['pred', val]
            flag = 1
            return s

    #and t or t not t
    elif t[0] == 'and':
        t1 = eval_term(t[1])
        if flag == 1:
            return ['and',t1,t[2],t[3]]
        if t1 == ['false']:
            return ['false']
        elif t1 == ['true']:
            t2 = eval_term(t[2])
            if flag == 1:
                return ['and',t1,t2,t[3]]
            if t2 == ['true']:
                return ['true']
            elif t2 == ['false']:
                t3 = eval_term(t[3])
                if flag == 1:
                    return ['and',t1,t2,t3]
                if t3 == ['true']:
                    return ['false']
                elif t3 == ['false']:
                    return ['true']
                else:
                    flag = 1
                    return ['and',t1,t2,t3]
            else:
                flag = 1
                return ['and',t1,t2,t[3]]
        else:
            flag = 1
            return ['and',t1,t[2],t[3]]

    #if-then-else
    elif t[0] == 'if':
        val = eval_term(t[1])
        if flag == 1:
            return ['if',val,t[2],t[3]]
        if val == ['true']:
            return eval_term(t[2])
        elif val == ['false']:
            return eval_term(t[3])
        else:
            flag = 1
            return t
   
   #others
    else:
        return listToString(t)
