# *-* coding:utf-8 *-*
import sys

def parse_file(path, max_len = 1000):
    '''
    #process valid dataset
    parse xml file, and rewrite into a file. Each line is a data
    lines: xml file name
    '''
    with open(path,'r') as f:
        data = f.readlines()
    #idx = 0
    for ln in data:
        """
        if idx >20:
            break
        """
        #print ln
        stack = ''
        sent = ''
        _id = None
        for w in ln:
            if w == '<':
                stack+=w
            elif w == '>':
                stack+=w
                if 'seg id' in stack:
                    _id = stack
                    #pritn stack
                stack = ''
            elif len(stack)!=0:
                stack+=w
            else:
                sent+=w
        if sent =='' or _id == None:
            continue
        print sent.strip()
        #idx+=1
    #return datas
if __name__ == '__main__':
    data_pp = sys.argv[1]
    #print data_pp
    parse_file(data_pp)