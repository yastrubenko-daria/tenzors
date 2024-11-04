import re
tensor1='1*ij-2*jj+1*jk-1*ii'
tensor2='1*ii+1*jj'
def components(tensor):
    components={'ii':0, 'ij':0, 'ik':0, 'ji':0, 'jj':0, 'jk':0, 'ki':0, 'kj':0, 'kk':0}
    elements=re.split(r"[+-]", tensor)
    for elem in elements:
        if elem == '':
            continue
        el=elem.split('*')
        index=tensor.find(elem)
        if tensor[index-1] == '+' or index==0:
            num = int(el[0])
        else:
            num = -1*int(el[0])
        com = el[1]
        components[com]=num
    return components

def scalar(tensor1, tensor2):
    comp1=components(tensor1)
    comp2 = components(tensor2)
    new_components={}
    for one in comp1:
        for two in comp2:
            if one[1] == two[0]:
                com=one[0]+two[1]
                if com in new_components:
                    new_components[com]+=comp1[one]*comp2[two]
                    continue
                new_components[com] = comp1[one] * comp2[two]

    return new_components

def find_tensor(components):
    tensor=''
    for el in components:
        num=components[el]
        if num!=0:
            if tensor!='' and num>0:
                tensor+='+'
            tensor+=str(num)+'*'+str(el)
    return tensor

def mul_vector(tensor1, tensor2):
    new_components = {}
    comp1 = components(tensor1)
    comp2 = components(tensor2)
    for one in comp1:
        for two in comp2:
            if one[1] != two[0]:
                compon = one[1] + two[0]
                if compon=='ij' or compon =='jk' or compon =='ki':
                    num=comp1[one] * comp2[two]
                if compon == 'ji' or compon == 'kj' or compon == 'ik':
                    num = -1 * comp1[one] * comp2[two]
                if compon =='ij' or compon=='ji':
                    com=one[0]+'k'+two[1]
                if compon =='jk' or compon=='kj':
                    com=one[0]+'i'+two[1]
                if compon =='ki' or compon=='ik':
                    com=one[0]+'j'+two[1]
                if com in new_components:
                    new_components[com] += num
                    continue
                new_components[com] = num
    tensor = find_tensor(new_components)
    return tensor
def doble_scaler(tensor1, tensor2):
    sum=0
    compon=scalar(tensor1, tensor2)
    #compon=components(new_tensor)
    for one in compon:
        if one[0]==one[1]:
            sum+=compon[one]
    return sum

def double_vector(tensor1, tensor2):
    compon_tensor={}
    new_tensor=mul_vector(tensor1,tensor2)
    new_components=components(new_tensor)
    for one in new_components:
        if len(one)!=3:
            continue
        if one[0]!=one[2]:
            compon = one[0] + one[2]
            num = new_components[one]
            if compon == 'ji' or compon == 'kj' or compon == 'ik':
                num = -1 * num
            if compon == 'ij' or compon == 'ji':
                com = one[1]+'k'
            if compon == 'jk' or compon == 'kj':
                com = one[1] + 'i'
            if compon == 'ki' or compon == 'ik':
                com = one[1] + 'j'
            if com in compon_tensor:
                compon_tensor[com] += num
                continue
            compon_tensor[com] = num
    tensor = find_tensor(compon_tensor)
    return tensor

def scalar_vector(tensor1, tensor2):
    compon_vector = {}
    new_components = scalar(tensor1, tensor2)
    for one in new_components:
        if one[0]!=one[1]:
            num = new_components[one]
            if one == 'ji' or one == 'kj' or one == 'ik':
                num = -1 * num
            if one == 'ij' or one == 'ji':
                com = 'k'
            if one == 'jk' or one == 'kj':
                com = 'i'
            if one == 'ki' or one == 'ik':
                com = 'j'
            if com in compon_vector:
                compon_vector[com] += num
                continue
            compon_vector[com] = num
    #todo: подключить класс вектор
    vector = find_tensor(compon_vector)
    return vector

def vector_scalar(tensor1, tensor2):
    compon_vector = {}
    new_tensor = mul_vector(tensor1, tensor2)
    new_components = components(new_tensor)
    for one in new_components:
        if len(one)!=3:
            continue
        if one[0] == one[2]:
            num = new_components[one]
            com = one[1]
            if com in compon_vector:
                compon_vector[com] += num
                continue
            compon_vector[com] = num
    # todo: подключить класс вектор
    vector = find_tensor(compon_vector)
    return vector
def transpose(tensor):
    comp=components(tensor)
    compon_vector={}
    for el in comp:
        num=comp[el]
        com=el[1]+el[0]
        if com in compon_vector:
            compon_vector[com] += num
            continue
        compon_vector[com] = num
    # todo: подключить класс вектор
    vector = find_tensor(compon_vector)
    return vector
#print(scalar(tensor1, tensor2))
components1=components(tensor1)
#print(components(tensor1))
#print(find_tensor(components1))
print(transpose(tensor1))