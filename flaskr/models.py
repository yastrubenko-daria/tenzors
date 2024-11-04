import re
class Tensor:
    '''Нужно писать умножение на диаду 22*ii 0.5*kj и т.д.'''
    #todo: работает без * ?проверять символ на ijk?
    #todo: проверка на тензор второго ранга
    #todo: прописать условие на единицу
    def __init__(self, tensor):
        self.tensor=tensor
        self.components = self.find_components(self.tensor)

    @staticmethod
    def find_components(tensor):
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
    def find_tensor(components):
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
        return tensor
    def vector(self, other):
        new_components = {}
        for one in self.components:
            for two in other.components:
                if one[1] != two[0]:
                    compon = one[1] + two[0]
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
        return tensor
    def double_scalar(self, other):
        summ=0
        new_tensor=self.scalar(self.tensor, other.tensor)
        compon=self.find_components(new_tensor)
        for one in compon:
            if one[0]==one[1]:
                summ+=compon[one]
        return summ

    def double_vector(self, other):
        compon_tensor={}
        new_tensor=self.vector(self.tensor, other.tensor)
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
        return tensor

    def scalar_vector(self, other):
        compon_vector = {}
        new_tensor = self.scalar(self.tensor, other.tensor)
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
        #todo: подключить класс вектор
        vector = self.find_tensor(compon_vector)
        return vector


    def vector_scalar(self, other):
        compon_vector = {}
        new_tensor = self.vector(self.tensor, other.tensor)
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
        # todo: подключить класс вектор
        vector = self.find_tensor(compon_vector)
        return vector

    def transpose(self):
        compon_vector={}
        for el in self.components:
            num=self.components[el]
            com=el[1]+el[0]
            if com in compon_vector:
                compon_vector[com] += num
                continue
            compon_vector[com] = num
        # todo: подключить класс вектор
        vector = self.find_tensor(compon_vector)
        return vector


    def antisymmetrical(self):
        pass

    def symmetrical(self):
        pass

    def first_invariant(self):
        pass

    def second_invariant(self):
        pass

    def third_invariant(self):
        pass

    def vector_invariant(self):
        pass

    def second_power(self):
        pass

    def inverse(self):
        pass


class Rotation_tensor(Tensor):
    def __init__(self, tensor=None, vec=None, angle=None):
        self.vec=vec
        self.angle=angle
        self.ort=None
        self.tensor=tensor

    def normalize_vec(self):
        pass

    def tensor(self):
        pass

    def vec(self):
        pass

    def angle(self):
        pass

    def rotation(self):
        pass


class Mapping_tensor(Tensor):
    def __init__(self, tensor=None, normal=None, plane=None ):
        self.normal=normal
        self.plane=plane
        self.tensor=tensor

    def tensor(self):
        pass

    def normal(self):
        pass

    def mapping(self):
        pass


class Vector:
    def __init__(self, components):
        self.components=components

    def scalar(self, other):
        pass

    def vector(self, other):
        pass

    def tensor_mult(self):
        pass