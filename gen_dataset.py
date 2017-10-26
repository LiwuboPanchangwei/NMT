# *-* coding:utf-8 *-*
import json
import sys
import numpy as np
from process_data import save

with open('./data/en.dic','r') as f:
    en2idx_dic = json.load(f)
with open('./data/zh.dic','r') as f:
    zh2idx_dic = json.load(f)
with open('./data/dataset.conf','r') as f:
    conf = json.load(f)
max_in_len = conf['max_in_len']
max_out_len = conf['max_out_len']
en_dic_size = conf['en_dic_size']
zh_dic_size = conf['zh_dic_size']

    
def vectorize(en,zh):
    """
    vectorize data
    """
    en_vec = np.zeros((max_in_len,en_dic_size))
    for i in range(len(en)):
        en_vec[i,en[i]] = 1
    zh_vec = np.zeros((1,max_out_len))
    for j in range(len(zh)):
        zh_vec[:,j] = zh[j]
    return en_vec, zh_vec
        
        
def gen_dataset(pp,batch_size):
    """
    """
    data_pp = pp + 'dataset'
    with open(data_pp,'r') as f:
        datas = json.load(f)
    ens = []
    ens_mask = []
    zhs = []
    zhs_mask = []
    idx = 0
    for en, zh in datas[:100]:
        #print idx
        ens.append([en2idx_dic[w] for w in en])
        ens_mask.append([1 for i in range(len(en))] + [0 for i in range(max_in_len-len(en))])
        zhs.append([zh2idx_dic[w] for w in zh])
        zhs_mask.append([1 for i in range(len(zh))] + [0 for i in range(max_out_len-len(zh))])
        idx+=1
    n_batch = int(len(ens)/batch_size)
    xs = []
    xs_mask = []
    ys = []
    ys_mask = []
    for n in range(n_batch):
        #print n
        x = np.zeros((batch_size,max_in_len,en_dic_size))
        x_mask = np.zeros((batch_size,max_in_len))
        y = np.zeros((batch_size,max_out_len))
        y_mask = np.zeros((batch_size,max_out_len))
        for index in range(batch_size):
            #print index
            en_vec,zh_vec = vectorize(ens[n* batch_size + index],zhs[n* batch_size + index]) 
            x[index,:] = en_vec
            x_mask[index,:] = np.array(ens_mask[n* batch_size + index])
            y[index,:] = zh_vec
            y_mask[index,:] = np.array(zhs_mask[n* batch_size + index])
        xs.append(x)
        xs_mask.append(x_mask)
        ys.append(y)
        ys_mask.append(y_mask)
    save(xs,pp+'en.batch','pickle')
    save(xs_mask,pp+'en.mask.batch','pickle')
    save(ys,pp+'zh.batch','pickle')
    save(ys_mask,pp+'zh.mask.batch','pickle')
    
                
if __name__ == '__main__':
    data_pp = sys.argv[1]
    batch_size = int(sys.argv[2])
    gen_dataset(data_pp,batch_size)