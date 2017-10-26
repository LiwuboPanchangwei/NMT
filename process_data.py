# *-* coding:utf-8 *-*
from collections import Counter
import json
import sys
import pickle
import jieba
import re
"""
stdi,stdo,stde=sys.stdin,sys.stdout,sys.stderr
reload(sys)
sys.setdefaultencoding('utf-8')
sys.stdin,sys.stdout,sys.stderr=stdi,stdo,stde
"""
with open('./fan2jian.dic','r') as f:
    f2j_dic = json.load(f)

end_sym = u'^_^'
zh_vocab_size = 50000

def fan2jian(w):
    """
    查字典将繁体字转换成简体字
    """
    if w in f2j_dic:
        return f2j_dic[w]
    return w

def isAlNum(word):
    try:
        return word.encode('ascii').isalnum()
    except UnicodeEncodeError:
        return False

def add_pos(w):
    """
    为zh中得数字和英文添加位置标志<B>，<M>，<E>
    """
    mixed_word = [] 
    for i in range(len(w)):
        s = w[i]
        if i == 0:
            s = '<B>' + s
        elif i == len(w) - 1:
            s = '<E>' + s
        else:
            s = '<M>' + s
        mixed_word.append(s)
    return mixed_word
             
def seg(s):
    segs = jieba.cut(s)
    segs = [s for s in segs]
    words = []
    for w in segs:
        if isAlNum(w.replace('.','').replace('%','')):
            words+=add_pos(w.lower())
        else:
            words += [fan2jian(zh) for zh in w]#繁体转简体
    #print json.dumps(words,ensure_ascii=False)
    return words 

def save(f,pp,method='json'):
    """
    save data
    f: file to save
    pp: save path
    method: save type
    """
    
    if method.lower() == 'json':
        #print type(f)
        #sss
        fp = file(pp,'w')
        json.dump(f, fp)
    elif method.lower() == 'pickle':
        fp = file(pp+'.pkl','wb')
        if isinstance(f,list):
            pickle.dump(f, fp, -1)
        else:
            pickle.dump(f, fp)
    else:
        print 'wrong save type!'
    fp.close()
    
def remove_sym(s):
    syms = {'`':'','\\':'','”':"\"",'~':'','|':'','“':"\"",'。':".",'，':","}
    for sym in syms:
        s = s.replace(sym,'')
    return s
    
def prop_data(pp,is_trian=False):
    """
    func：
        process data and generate dictionary, config file and dataset
    input：
        pp: data path
    output：
        en_dic
        zh_dic
        dataset: [[data1_en,data1_zh],...]
    
    """
    """
    if is_train:
        en_pp = pp + 'train.en'
        zh_pp = pp + 'train.zh'
    else:
        en_pp = pp + 'val.en'
        zh_pp = pp + 'val.zh'
    """
    en_pp = pp + 'train.en'
    zh_pp = pp + 'train.zh'
    en_dic = {}
    en_all_dic = []
    en_dataset = []
    zh_dic = {}
    zh_dic[end_sym.encode('utf-8')] = len(zh_dic)+1
    zh_dataset = []
    config = {}
    max_input_len = 0
    max_output_len = 0
    
    with open(en_pp,'r') as f:
        en_data = f.readlines()        
    for ln in en_data:
        strr = ln
        ln = remove_sym(ln)
        ln = ln.decode('utf-8').strip()
        if not ln:
            continue
        ln = re.split(r'([,. ?!\-\"()$#@\\&*=+:/><])',ln)
        ln = [i.lower() for i in ln if i != u' ' and i != u'']
        #ln = [w.lower().encode('utf-8') for w in ln.split()]
        if len(ln) > max_input_len:
            max_input_len = len(ln)
        item_seg = []
        #拆分缩写的单词组
        for w in ln:
            #w = w.encode('utf-8')
            if '\'' in w:
                #print w.encode('utf-8')
                w = w.split('\'')
                for i in range(len(w)):
                    if i!=1:
                        item_seg.append(w[i])
                    else:
                        item_seg.append('\''+w[i])
                #print json.dumps([j.encode('utf-8') for j in item_seg],ensure_ascii=False)
                continue
            item_seg.append(w)
        en_dataset.append(item_seg)
        en_all_dic.extend(item_seg)
        
    #print json.dumps(en_dataset,ensure_ascii=False)
    #统计词频
    counter = Counter(en_all_dic)
    word_counts = sorted(counter.items(), key=lambda x : -x[1])[:zh_vocab_size]
    #print word_counts
    #sss
    en_words_filter_ = [w[0] for w in word_counts]
    #en_words_filter_ = tuple([i[0] for i in word_counts if i[1]>10])
    #print len(word_counts),len(en_words_filter_)
    en_dic = dict(zip(en_words_filter_, range(len(en_words_filter_))))#源语言不需要终止符
    #print json.dumps(en_dic,ensure_ascii=False)
    #print len(en_dic)
    #转换数据中的oov成mixed word的表达方法
    for i in range(len(en_dataset)):
        data = []
        for w in en_dataset[i]:
            #w = w.decode('utf-8').encode('utf-8')
            if w not in en_dic:
                seg_syms = add_pos(w)
                data += seg_syms
                for sym in seg_syms:
                    if sym not in en_dic:
                        en_dic[sym]= len(en_dic)
            else:
                data.append(w)
        en_dataset[i] = data
    #print json.dumps(en_dataset,ensure_ascii=False)
    
    with open(zh_pp,'r') as f:
        zh_data = f.readlines()
    
    for ln in zh_data:
        ln = ln.decode('utf-8')
        ln = ln.strip()
        ln = seg(ln)+[end_sym] #切割中文，数字和字母的组合
        #print json.dumps([w.encode('utf-8') for w in ln],ensure_ascii=False)
        if len(ln) > max_output_len:
            max_output_len = len(ln)
        zh_dataset.append(ln)
        #统计zh字典
        for w in ln:
            if w.encode('utf-8') not in zh_dic:
                #zh_dic[len(zh_dic)]=w
                #print len(zh_dic)+1
                zh_dic[w.encode('utf-8')]=len(zh_dic)+1#0->padding
                #zh_dic[w.encode('utf-8')]=1
                #continue
            #zh_dic[w.encode('utf-8')]+=1
    
    if is_trian:
        save(en_dic,'./data/en.dic')
        save(zh_dic,'./data/zh.dic')
        config['max_in_len'] = max_input_len
        config['max_out_len'] = max_output_len
        config['en_dic_size'] = len(en_dic)
        config['zh_dic_size'] = len(zh_dic)+1#0—>padding
        save(config,'./data/dataset.conf')
    data = zip(en_dataset,zh_dataset)
    save(data, pp+'dataset')
    
    
    
                
if __name__ == '__main__':
    data_pp = sys.argv[1]
    is_train = False
    flag = sys.argv[2]
    if flag == 'true':
        is_train = True
    #print data_pp
    prop_data(data_pp,is_train)