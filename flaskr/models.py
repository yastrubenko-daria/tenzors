import re, math
class Tensor:
    '''Нужно писать умножение на диаду 22*ii 0.5*kj и т.д.
    Нужно писать единицу
    *, / - умножение и деление на число '''
    #todo: работает без * ?проверять символ на ijk?
    #todo: проверка на тензор второго ранга
    #todo: прописать условие на единицу
    def __init__(self, tensor):
        self.tensor=tensor
        self.components = self.find_components(self.tensor)

    def __add__(self, other):
        new_components={}
        for el_one, value_one in self.components.items():
            for el_two, value_two in other.components.items():
                if el_two==el_one:
                    value=value_one+value_two
                    new_components[el_one]=value
        tensor=self.find_tensor(new_components)
        new_tensor=Tensor(tensor)
        return new_tensor

    def __sub__(self, other):
        new_components = {}
        for el_one, value_one in self.components.items():
            for el_two, value_two in other.components.items():
                if el_two == el_one:
                    value = value_one - value_two
                    new_components[el_one] = value
        tensor = self.find_tensor(new_components)
        new_tensor = Tensor(tensor)
        return new_tensor

    def __mul__(self, num):
        new_components = {}
        for el_one, value_one in self.components.items():
            value = value_one * num
            new_components[el_one] = value
        tensor = self.find_tensor(new_components)
        new_tensor = Tensor(tensor)
        return new_tensor

    def __truediv__(self, num):
        new_components = {}
        for el_one, value_one in self.components.items():
            value = value_one / num
            new_components[el_one] = value
        tensor = self.find_tensor(new_components)
        new_tensor = Tensor(tensor)
        return new_tensor

    def eye_tensor(self):
        components = {'ii': 1, 'ij': 0, 'ik': 0, 'ji': 0, 'jj': 1, 'jk': 0, 'ki': 0, 'kj': 0, 'kk': 1}
        tensor=self.find_tensor(components)
        new_tensor=Tensor(tensor)
        return new_tensor

    @staticmethod
    def find_components(tensor)->dict:
        components = {'ii': 0, 'ij': 0, 'ik': 0, 'ji': 0, 'jj': 0, 'jk': 0, 'ki': 0, 'kj': 0, 'kk': 0}
        elements = re.split(r"[+-]", tensor)
        for elem in elements:
            el = elem.split('*')
            index = tensor.find(elem)
            if tensor[index - 1] == '+' or index == 0:
                num = int(el[0])
            else:
                num = -1 * int(el[0])
            com = el[1]
            components[com] = num
        return components

    @staticmethod
    def find_tensor(components)->str:
        tensor = ''
        for el in components:
            num = components[el]
            if num != 0:
                if tensor != '' and num > 0:
                    tensor += '+'
                tensor += str(num) + '*' + str(el)
        return tensor

    def scalar(self, other):
        new_components = {}
        for one in self.components:
            for two in other.components:
                if one[1] == two[0]:
                    com = one[0] + two[1]
                    if com in new_components:
                        new_components[com] += self.components[one] * other.components[two]
                        continue
                    new_components[com] = self.components[one] * other.components[two]
        tensor=self.find_tensor(new_components)
        new_tensor=Tensor(tensor)
        return new_tensor

    def vector(self, other):
        new_components = {}
        for one in self.components:
            for two in other.components:
                if one[1] != two[0]:
                    compon = one[1] + two[0]
                    num=0
                    com=''
                    if compon=='ij' or compon =='jk' or compon =='ki':
                        num=self.components[one] * other.components[two]
                    if compon == 'ji' or compon == 'kj' or compon == 'ik':
                        num = -1 * self.components[one] * other.components[two]
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
        tensor = self.find_tensor(new_components)
        new_tensor=Tensor(tensor)
        return new_tensor

    def mult_scal_vec(self, vector):
        new_components = {}
        for one in self.components:
            for two in vector.components:
                if one[1] == two:
                    com = one[0]
                    if com in new_components:
                        new_components[com] += self.components[one] * vector.components[two]
                        continue
                    new_components[com] = self.components[one] * vector.components[two]
        vector = Vector.find_vector(new_components)
        new_vector = Vector(vector)
        return new_vector

    def mult_vect_vec(self, vector):
        new_components = {}
        for one in self.components:
            for two in vector.components:
                if one[1] != two:
                    com=''
                    num=0
                    compon = one[1] + two
                    if compon == 'ij' or compon == 'jk' or compon == 'ki':
                        num = self.components[one] * vector.components[two]
                    if compon == 'ji' or compon == 'kj' or compon == 'ik':
                        num = -1 * self.components[one] * vector.components[two]
                    if compon == 'ij' or compon == 'ji':
                        com = one[0] + 'k'
                    if compon == 'jk' or compon == 'kj':
                        com = one[0] + 'i'
                    if compon == 'ki' or compon == 'ik':
                        com = one[0] + 'j'
                    if com in new_components:
                        new_components[com] += num
                        continue
                    new_components[com] = num
        tensor = self.find_tensor(new_components)
        new_tensor = Tensor(tensor)
        return new_tensor

    def double_scalar(self, other):
        summ=0
        new_tensor = self.scalar(self.tensor, other.tensor).tensor
        compon=self.find_components(new_tensor)
        for one in compon:
            if one[0]==one[1]:
                summ+=compon[one]
        return summ

    def double_vector(self, other):
        compon_tensor={}
        new_tensor=self.vector(self.tensor, other.tensor).tensor
        new_components=self.find_components(new_tensor)
        for one in new_components:
            if len(one) != 3:
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
        tensor = self.find_tensor(compon_tensor)
        new_tensor = Tensor(tensor)
        return new_tensor

    def scalar_vector(self, other):
        compon_vector = {}
        new_tensor = self.scalar(self.tensor, other.tensor).tensor
        new_components = self.find_components(new_tensor)
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
        vector = Vector.find_vector(compon_vector)
        new_vector=Vector(vector)
        return new_vector


    def vector_scalar(self, other):
        compon_vector = {}
        new_tensor = self.vector(self.tensor, other.tensor).tensor
        new_components = self.find_components(new_tensor)
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
        vector = Vector.find_vector(compon_vector)
        new_vector=Vector(vector)
        return new_vector

    def transpose(self):
        new_components={}
        for el in self.components:
            num=self.components[el]
            com=el[1]+el[0]
            if com in new_components:
                new_components[com] += num
                continue
            new_components[com] = num
        tensor = self.find_tensor(new_components)
        new_tensor = Tensor(tensor)
        return new_tensor

    def antisymmetrical(self):
        return 0.5 * (self.tensor-self.transpose())

    def symmetrical(self):
        return 0.5 * (self.tensor+self.transpose())

    def first_invariant(self):
        summ=0
        for el in self.components:
            if el[0] == el[1]:
                num = self.components[el]
                summ+=num
        return summ

    def second_invariant(self):
        return 0.5 * (self.first_invariant()**2-self.second_degree().first_invariant())

    def third_invariant(self):
        vec_i=Vector('i')
        vec_a=self.mult_scal_vec(vec_i)
        vec_j=Vector('j')
        vec_b = self.mult_scal_vec(vec_j)
        vec_k = Vector('k')
        vec_c = self.mult_scal_vec(vec_k)
        return vec_a.scalar(vec_b.vector(vec_c))


    def vector_invariant(self):
        new_components = {}
        for one in self.components:
            if one[0] != one[1]:
                com=''
                num=0
                if one == 'ij' or one == 'jk' or one == 'ki':
                    num = self.components[one]
                if one == 'ji' or one == 'kj' or one == 'ik':
                    num = -1 * self.components[one]
                if one == 'ij' or one == 'ji':
                    com = 'k'
                if one == 'jk' or one == 'kj':
                    com = 'i'
                if one == 'ki' or one == 'ik':
                    com = 'j'
                if com in new_components:
                    new_components[com] += num
                    continue
                new_components[one] = num
        vector = Vector.find_vector(new_components)
        new_vector = Vector(vector)
        return new_vector

    def second_degree(self):
        return self.scalar(self)

    def inverse(self):
        i3=self.third_invariant()
        i2=self.second_invariant()
        i1=self.first_invariant()
        ten=Tensor(self.tensor)
        tensor=1/i3 *(self.second_degree()-i1 * ten + i2*self.eye_tensor)
        new_tensor=Tensor(tensor)
        return new_tensor


class Rotation_tensor(Tensor):
    def __init__(self, tensor=None, vec=None, angle=None):
        '''Угол в радианах'''
        if tensor is None:
            tensor=self.find_rot_tensor()
        if vec is None:
            vec=self.find_vec()
        if angle is None:
            angle=self.find_angle()
        self.vec=Vector(vec)
        self.angle=angle
        self.ort=self.normalize_vec()
        self.tensor=tensor

    def normalize_vec(self):
        compon=self.vec.components
        summ=0
        for el in compon:
            summ+=compon[el]
        new_compon={}
        for el in compon:
            new_compon[el]=compon[el]/summ
        vector=Vector.find_vector(new_compon)
        new_vector=Vector(vector)
        self.ort=new_vector

    def find_rot_tensor(self):
        return self.ort.tensors_mult(self.ort).tensor + '+' + (self.eye_tensor()-self.ort.tensor_mult(self.ort) * math.cos(float(self.angle))).tensor + '+' + (self.ort.vector(self.eye_tensor()) * math.sin(float(self.angle))).tensor

    def find_vec(self):
        value=-1 * self.vector_invariant() / (2 * math.sin(float(self.angle)))
        self.vec=value
        return value

    def find_angle(self):
        value=math.acos((self.first_invariant()-1))/2
        self.angle=value
        return value

    def rotation_vec(self, vec):
        return self.mult_scal_vec(vec)

    def rotation_tensor(self, tensor):
        return self.scalar(tensor).scalar(self.transpose())


class Mapping_tensor(Tensor):
    def __init__(self, tensor=None, normal=None, plane=None ):
        if normal is None:
            normal= self.find_normal()
        if tensor is None:
            tensor= self.find_map_tensor()
        self.normal=Vector(normal)
        self.plane=plane
        self.tensor=tensor

    def find_map_tensor(self):
        value=self.eye_tensor()-2 * self.normal.tensor_mult(self.normal)
        self.tensor = value
        return value

    def find_normal(self):
        components = {'i': 0, 'j': 0, 'k': 0}
        elements = re.split(r"[+-]", self.plane)
        for elem in elements:
            el = elem.split('*')
            index = self.plane.find(elem)
            if self.plane[index - 1] == '+' or index == 0:
                num = int(el[0])
            else:
                num = -1 * int(el[0])
            com = el[1]
            components[com] = num
        vector=Vector.find_vector(components)
        return vector

    def mapping_vec(self, vec):
        return self.mult_scal_vec(vec)

    def mapping_tensor(self, tensor):
        return self.scalar(tensor).scalar(self.transpose())


class Vector:
    def __init__(self, vec):
        self.vec=vec
        self.components=self.find_components

    def scalar(self, other):
        summ=0
        for one in self.components:
            for two in other.components:
                if one == two:
                    summ += self.components[one] * other.components[two]
        return summ

    @staticmethod
    def find_components(vec) -> dict:
        components = {'i': 0, 'j': 0, 'k': 0}
        elements = re.split(r"[+-]", vec)
        for elem in elements:
            el = elem.split('*')
            index = vec.find(elem)
            if vec[index - 1] == '+' or index == 0:
                num = int(el[0])
            else:
                num = -1 * int(el[0])
            com = el[1]
            components[com] = num
        return components

    @staticmethod
    def find_vector(components) -> str:
        vector = ''
        for el in components:
            num = components[el]
            if num != 0:
                if vector != '' and num > 0:
                    vector += '+'
                vector += str(num) + '*' + str(el)
        return vector

    def vector(self, other):
        new_components = {}
        for one in self.components:
            for two in other.components:
                if one != two:
                    compon = one + two
                    num = 0
                    com = ''
                    if compon == 'ij' or compon == 'jk' or compon == 'ki':
                        num = self.components[one] * other.components[two]
                    if compon == 'ji' or compon == 'kj' or compon == 'ik':
                        num = -1 * self.components[one] * other.components[two]
                    if compon == 'ij' or compon == 'ji':
                        com = 'k'
                    if compon == 'jk' or compon == 'kj':
                        com = 'i'
                    if compon == 'ki' or compon == 'ik':
                        com = 'j'
                    if com in new_components:
                        new_components[com] += num
                        continue
                    new_components[com] = num
        vector = self.find_vector(new_components)
        new_vector = Vector(vector)
        return new_vector

    def tensor_mult(self, other):
        new_components = {}
        for one in self.components:
            for two in other.components:
                com = one + two
                num = self.components[one] * other.components[two]
                if com in new_components:
                    new_components[com] += num
                    continue
                new_components[com] = num
        tensor = Tensor.find_tensor(new_components)
        new_tensor = Tensor(tensor)
        return new_tensor

    def mult_scal_tens(self, tensor):
        new_components = {}
        for one in self.components:
            for two in tensor.components:
                if one == two[0]:
                    com = two[1]
                    if com in new_components:
                        new_components[com] += self.components[one] * tensor.components[two]
                        continue
                    new_components[com] = self.components[one] * tensor.components[two]
        vector = self.find_vector(new_components)
        new_vector = Vector(vector)
        return new_vector

    def mult_vect_tens(self, tensor):
        new_components = {}
        for one in self.components:
            for two in tensor.components:
                if one != two[0]:
                    com=''
                    num=0
                    compon = one + two[0]
                    if compon == 'ij' or compon == 'jk' or compon == 'ki':
                        num = self.components[one] * tensor.components[two]
                    if compon == 'ji' or compon == 'kj' or compon == 'ik':
                        num = -1 * self.components[one] * tensor.components[two]
                    if compon == 'ij' or compon == 'ji':
                        com = 'k' + two[1]
                    if compon == 'jk' or compon == 'kj':
                        com = 'i' + two[1]
                    if compon == 'ki' or compon == 'ik':
                        com = 'j' + two[1]
                    if com in new_components:
                        new_components[com] += num
                        continue
                    new_components[com] = num
        tensor = self.find_tensor(new_components)
        new_tensor = Tensor(tensor)
        return new_tensor
