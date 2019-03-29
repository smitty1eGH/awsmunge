from botocore.loaders import Loader

#Make named tuple for operations:
#'http', 'name', 'documentation', 'output', 'input'

#Make named tuple for shapes:
#'required', 'members', 'member', 'type', 'min', 'enum', 'max', 'documentation', 'pattern'

#Mane named tuple for shapes.members:
#'locationName', 'shape', 'queryName', 'idempotencyToken', 'documentation'

l=Loader()
m=l.load_service_model('ec2','service-2')
kset=set()

def process_operations(v1):
    '''v1 is a collection of operations entities for the service.
    Inputs and outputs for c2s are regular, except:
        {"CancelConversionTask,OrderedDict([('shape', 'CancelConversionRequest')])"}
    '''
    for k2,v2 in v1.items():
        print(f'\n{k2}')

        for k3,v3 in v2.items():
            print(f'\n\t{k3}')

            if k3 == 'http':
                #OrderedDict([('method', 'POST'), ('requestUri', '/')])
                #print(f'\n\t\thttp is {v3}')
                #if v3["method"] != 'POST' or v3["requestUri"] != '/':
                #    kset.add(f'{k2} has http == {v3}')
                pass
            elif k3 == 'name': #k3 == k2
                pass
            elif k3 == 'documentation':
                pass
            elif k3 == 'output':
                if v3['shape']==f"{k2}Result":
                    print('\n\t\texpected')
                else:
                   print(f'\n\t\t => {v3["shape"]} or {k3}Result')
            elif k3 == 'input':
                if v3['shape']==f"{k2}Request":
                    print('\n\t\texpected')
                else:
                   print(f'\n\t\t => {v3["shape"]} or {k3}Request')
                   kset.add(f'{k2},{v3}')
        if 'output' not in v2:
            print(f'\n\tno output for {k2}')


def process_shapes(v1):
    '''v1 is a collection of shape entries for the service.
    '''
    for k2,v2 in v1.items():
        print(f'\n{k2}')

        for k3,v3 in v2.items():
            print(f'\n\t{k3}')

            if k3 == 'member':
                for k4,v4 in v3.items():
                    if k4 =='shape':
                        print(f'\t\tshape is {v4}')
                    elif k4 =='locationName':
                        print(f'\t\tlocationName is {v4}')
                    else:
                        print('This is an error state')

            elif k3 == 'required':
                print(f'\t\trequired is {v3}')

            elif k3 == 'members':
                #need to note dependency
                for k4,v4 in v3.items():
                    print(f'\t\t{k4}')
                    for k5,v5 in v4.items():
                        print(f'\t\t\t{k5} {v5}')

            elif k3 == 'type':
                #possibilities include ['list', 'double', 'integer', 'blob', 'timestamp', 'float', 'long', 'string', 'boolean', 'structure']
                print(f'\t\ttype is {v3}')

            elif k3 == 'min':
                print(f'\t\tmin is {v3}')

            elif k3 == 'enum':
                print(f'\t\tenum is {v3}')

            elif k3 == 'max':
                print(f'\t\tmax is {v3}')

            elif k3 == 'documentation':
                pass

            elif k3 == 'pattern':
                print(f'\t\tpattern is {v3}')

for k1,v1 in m.items():
    '''Process in this order: version, metadata, shapes, operations, documentation
    '''
    if k1=='version':
        print(f'{k1}: {v1}')

    elif k1=='metadata':
        print(f'{k1}: {v1}')

    elif k1=='operations':
        process_operations(v1)
        #pass

    elif k1=='shapes':
        #process_shapes(v1)
        pass
    elif k1=='documentation':
        pass
print(kset)
