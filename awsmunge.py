import ast

def awsret2dict(aws_return):
    '''Convert the raw AWS_RETURN value for an API call to a python dict.
    '''
    def wrap_value(frag):
        '''Pipes, and datetime() calls, in FRAG must be double quoted.
           Be mindful of commas at the end of the line.
        '''
        maybe_comma=''
        use_text=''
        f=frag.split(': ')
        if f[1][-1:]==',':
            maybe_comma=','
            use_text=f[1][:-1]
        else:
            maybe_comma=''
            use_text=f[1]
        return '''%s: "%s"%s''' % (f[0].lstrip(),use_text,maybe_comma)

    #Split the return text on newlines, and prepare to write it line-for-line
    #  to a new list. Check for problem characters and wrap with double
    #  quotes if needful.
    z=[]
    for y in aws_return.split('\n'):
        a=y
        if '|' in y or 'datetime(' in y:
            a=wrap_value(y)
        z.append(a)

    #https://docs.python.org/3/library/ast.html#ast-helpers
    return ast.literal_eval(''.join(z))

def flatten_awsret(aws_return):
    '''Take the AWS_RETURN, convert to dict via awsret2dict(), then
         do depth-first traversals of that dict, and store the results
         in a new, flattened traversal form (FTF).

       The keys of FTF are of this wise:

         a:b,c.d

       Where:
         a, b, c, and d are arbitrary key names in the aws_return, and the
         category of the delimiter indicates the value portion:
         :   more child key values, as a csv string
         ,   a list
         .   a terminating value of type indicated by character d:
             s=string
             i=integer
             d=datetime
    '''
    def type2delim(v_type):
        '''Return character based upon V_TYPE
        '''
        #print('v_type %s' % v_type)
        type_dict={"<class 'list'>"    :','
                  ,"<class 'str'>"     :'s'
                  ,'datetime':'d'
                  ,'int'     :'i'
                  ,'dict'    :':'
                  }
        return type_dict[v_type]

    d=awsret2dict(aws_return)
    print()
    for k,v in d.items():
        print('key_name %s, value type %s' % (k, type2delim(str(type(v)))))
