import ast
from typing import Dict, List, Union

def awsret2dict(aws_return: str) -> Dict:
    '''Convert the raw AWS_RETURN value for an API call to a python dict.
    '''
    def wrap_value(frag: str) -> str:
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

def flatten_awsret(aws_return: str) -> Dict:
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
    def type2delim(v_type: str) -> str:
        '''Return character based upon V_TYPE
        '''
        print('v_type %s' % v_type)
        try:
            type_dict={"<class 'list'>"  :','
                      ,"<class 'str'>"   :'s'
                      ,"<class 'dict'>"  :':'
                      ,'datetime':'d'
                      ,'int'     :'i'
                      }
        except:
            print(v_type)
        return type_dict[v_type]

    def descend(input: Union[List,Dict,str,int]) -> None:
        for k,v in d.items():
            t=type2delim(str(type(v)))
            print('key_name %s, value type %s' \
                 % (k, t))

            #If we're dealing with a list or dict, we need to descend.
            #  need a "descend iterator" that checks the type of the
            #  container member and does key/value discrimination as required.
            if t in [',',':']:
                if t==',':
                    for w in v:
                        #print('list entry %s' % w)
                        descend(w)
                else:
                    for vk, vv in v.items():
                        descend(vv)

    d: dict=awsret2dict(aws_return)
    descend(d)
