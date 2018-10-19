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

       What's tricky is that you don't descend a list the same way you
         do a dict.
       So the code gets clearer knowing that it starts with a dictionary,
         then has a separate dispatcher pushing the thread of execution
         to either a dictionary or a list handler.
    '''
    all_your_symbols={}

    def type2delim(v_type: str) -> str:
        '''Return character based upon V_TYPE

           'datetime':'d' shows up as str
        '''
        #print('v_type %s' % v_type)
        try:
            type_dict={"<class 'list'>"  :','
                      ,"<class 'str'>"   :'s'
                      ,"<class 'dict'>"  :':'
                      ,"<class 'int'>"   :'i'
                      }
        except:
            print("surpsise type in type2delim() => %s" % v_type)
        return type_dict[v_type]

    def _descend_dispatch(v: Union[Dict,List,str,int])->str:
        '''Switch on the type of the input.
        '''
        t=type2delim(str(type(v)))
        if t == ',':
            _descend_list(v)
        elif t == ':':
            descend(v)
        else:
            pass
        return t

    def _descend_list(alist: List)-> None:
        '''Descend() will encounter a list. do that.
        '''
        for _,v in enumerate(alist):
            t=_descend_dispatch(v)

    def descend(d: Dict) -> None:
        '''Descend a structure known to be a Dict at the top level.
        '''
        current=[]
        t=''
        for k,v in d.items():
            all_your_symbols.append(k)
            t=_descend_dispatch(v)
            if t in [",",":"]:
                current.append('%s%s' % (k,t))

    d: dict=awsret2dict(aws_return)
    descend(d)
    print(all_your_symbols)
