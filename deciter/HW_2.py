#!/usr/bin/env python
# coding: utf-8

# # Задание 1 (2 балла)

# Напишите класс `MyDict`, который будет полностью повторять поведение обычного словаря, за исключением того, что при итерации мы должны получать и ключи, и значения.
# 
# **Модули использовать нельзя**

# In[1]:


# Ваш код здесь

class MyDict(dict):
    def __iter__(self):
        iterator = iter(self.items())
        return iterator


# In[2]:


dct = MyDict({"a": 1, "b": 2, "c": 3, "d": 25})
for key, value in dct:
    print(key, value)   


# In[3]:


for key, value in dct.items():
    print(key, value)


# In[4]:


for key in dct.keys():
    print(key)


# In[5]:


dct["c"] + dct["d"]


# # Задание 2 (2 балла)

# Напишите функцию `iter_append`, которая "добавляет" новый элемент в конец итератора, возвращая итератор, который включает изначальные элементы и новый элемент. Итерироваться по итератору внутри функции нельзя, то есть вот такая штука не принимается
# ```python
# def iter_append(iterator, item):
#     lst = list(iterator) + [item]
#     return iter(lst)
# ```
# 
# **Модули использовать нельзя**

# In[6]:


def iter_append(iterator, item):
    yield from iterator
    yield item
    
  

my_iterator = iter([1, 2, 3])
new_iterator = iter_append(my_iterator, 4)

for element in new_iterator:
    print(element)


# # Задание 3 (5 баллов)

# Представим, что мы установили себе некотурую библиотеку, которая содержит в себе два класса `MyString` и `MySet`, которые являются наследниками `str` и `set`, но также несут и дополнительные методы.
# 
# Проблема заключается в том, что библиотеку писали не очень аккуратные люди, поэтому получилось так, что некоторые методы возвращают не тот тип данных, который мы ожидаем. Например, `MyString().reverse()` возвращает объект класса `str`, хотя логичнее было бы ожидать объект класса `MyString`.
# 
# Найдите и реализуйте удобный способ сделать так, чтобы подобные методы возвращали экземпляр текущего класса, а не родительского. При этом **код методов изменять нельзя**
# 
# **+3 дополнительных балла** за реализацию того, чтобы **унаследованные от `str` и `set` методы** также возвращали объект интересующего нас класса (то есть `MyString.replace(..., ...)` должен возвращать `MyString`). **Переопределять методы нельзя**
# 
# **Модули использовать нельзя**

# In[7]:


# Ваш код где угодно, но не внутри методов

#Создаем декоратор методов
#Если метод возвращает экземпляр родительского класса - преобразовываем в дочерний класс

def to_myclass(func):
    def inner_func(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        if isinstance(result, type(self).__base__):
            return type(self)(result)
        else:
            return result
    return inner_func

#Пробегаемся по атрибутам класса. Если он callable - декорируем. Возвращаем новый класс.
#Как я понял, для декорирования аргументов родительского класса нужно было использовать метаклассы, но там как-то все сложно, так что пускай уж будет так

def class_decorator(decorator):
    def inner_func_2(cls):
        for attr in cls.__dict__:
            if callable(getattr(cls, attr)):
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls
    return inner_func_2

@class_decorator(to_myclass)
class MyString(str):

    def reverse(self):
        return self[::-1]

    def make_uppercase(self):
        return "".join([chr(ord(char) - 32) if 97 <= ord(char) <= 122 else char for char in self])

    def make_lowercase(self):
        return "".join([chr(ord(char) + 32) if 65 <= ord(char) <= 90 else char for char in self])

    def capitalize_words(self):
        return " ".join([word.capitalize() for word in self.split()])
    
@class_decorator(to_myclass)
class MySet(set):

    def is_empty(self):
        return len(self) == 0

    def has_duplicates(self):
        return len(self) != len(set(self))

    def union_with(self, other):
        return self.union(other)

    def intersection_with(self, other):
        return self.intersection(other)

    def difference_with(self, other):
        return self.difference(other)


# In[8]:


string_example = MyString("Aa Bb Cc")
set_example_1 = MySet({1, 2, 3, 4})
set_example_2 = MySet({3, 4, 5, 6, 6})

print(type(string_example.reverse()))
print(type(string_example.make_uppercase()))
print(type(string_example.make_lowercase()))
print(type(string_example.capitalize_words()))
print()
print(type(set_example_1.is_empty()))
print(type(set_example_2.has_duplicates()))
print(type(set_example_1.union_with(set_example_2)))
print(type(set_example_1.difference_with(set_example_2)))


# # Задание 4 (5 баллов)

# Напишите декоратор `switch_privacy`:
# 1. Делает все публичные **методы** класса приватными
# 2. Делает все приватные методы класса публичными
# 3. Dunder методы и защищённые методы остаются без изменений
# 4. Должен работать тестовый код ниже, в теле класса писать код нельзя
# 
# **Модули использовать нельзя**

# In[9]:


# это было больно


def switch_to_my_methods(cls):
    for attr_name in dir(cls):
        method = getattr(cls, attr_name)
        if callable(method):
            if not attr_name.startswith('_'):
                upd_attr_name = f'_{cls.__name__}__{attr_name}'
                setattr(cls, upd_attr_name, method)
                delattr(cls, attr_name)
            if attr_name.startswith(f'_{cls.__name__}__'):
                upd_attr_name = attr_name.replace(f'_{cls.__name__}__', '')
                setattr(cls, upd_attr_name, method)
                delattr(cls, attr_name)
    return cls

@switch_to_my_methods
class ExampleClass:
    def public_method(self):
        return 1
    
    def _protected_method(self):
        return 2
    
    def __private_method(self):
        return 3
    
    def __dunder_method__(self):
        pass


# In[10]:


test_object = ExampleClass()

test_object._ExampleClass__public_method()   # Публичный метод стал приватным


# In[11]:


test_object.private_method()   # Приватный метод стал публичным


# In[12]:


test_object._protected_method()   # Защищённый метод остался защищённым


# In[13]:


test_object.__dunder_method__()   # Дандер метод не изменился


# In[14]:


hasattr(test_object, "public_method"), hasattr(test_object, "private")   # Изначальные варианты изменённых методов не сохраняются


# # Задание 5 (7 баллов)

# Напишите [контекстный менеджер](https://docs.python.org/3/library/stdtypes.html#context-manager-types) `OpenFasta`
# 
# Контекстные менеджеры это специальные объекты, которые могут работать с конструкцией `with ... as ...:`. В них нет ничего сложного, для их реализации как обычно нужно только определить только пару dunder методов. Изучите этот вопрос самостоятельно
# 
# 1. Объект должен работать как обычные файлы в питоне (наследоваться не надо, здесь лучше будет использовать **композицию**), но:
#     + При итерации по объекту мы должны будем получать не строку из файла, а специальный объект `FastaRecord`. Он будет хранить в себе информацию о последовательности. Важно, **не строки, а именно последовательности**, в fasta файлах последовательность часто разбивают на много строк
#     + Нужно написать методы `read_record` и `read_records`, которые по смыслу соответствуют `readline()` и `readlines()` в обычных файлах, но они должны выдавать не строки, а объект(ы) `FastaRecord`
# 2. Конструктор должен принимать один аргумент - **путь к файлу**
# 3. Класс должен эффективно распоряжаться памятью, с расчётом на работу с очень большими файлами
#     
# Объект `FastaRecord`. Это должен быть **датакласс** (см. про примеры декораторов в соответствующей лекции) с тремя полями:
# + `seq` - последовательность
# + `id_` - ID последовательности (это то, что в фаста файле в строке, которая начинается с `>` до первого пробела. Например, >**GTD326487.1** Species anonymous 24 chromosome) 
# + `description` - то, что осталось после ID (Например, >GTD326487.1 **Species anonymous 24 chromosome**)
# 
# 
# Напишите демонстрацию работы кода с использованием всех написанных методов, обязательно добавьте файл с тестовыми данными в репозиторий (не обязательно большой)
# 
# **Можно использовать модули из стандартной библиотеки**

# In[5]:


from dataclasses import dataclass
import os

@dataclass
class FastaRecord:
    seq: str
    id_: str
    description: str


class OpenFasta:
    def __init__(self, file_name, method="r"):
        self.file_obj = open(file_name, method)
        self.line = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.file_obj.close()

    def read_record(self):
        if self.line == None:
            line = self.file_obj.readline().strip() 
        else:
            line = self.line
        if not line:  
            return None
        if ' ' not in line:
            id_, description = line[1:], ''
        else: 
            id_, description = line[1:].split(maxsplit=1)  
        seq = '' 
        while True:
            line = self.file_obj.readline().strip()  
            if not line or line.startswith('>'):  
                self.line = line
                break
            seq += line
        return FastaRecord(seq=seq, id_=id_, description=description)

    def read_records(self):
        while True:
            record = self.read_record()  
            if not record:  
                break
            yield record


# пример использования


with OpenFasta(os.path.join("data", "example.fasta")) as fasta:
    records = fasta.read_records()
    for record in records:
        print(record)


# # Задание 6 (7 баллов)

# 1. Напишите код, который позволит получать все возможные (неуникальные) генотипы при скрещивании двух организмов. Это может быть функция или класс, что вам кажется более удобным.
# 
# Например, все возможные исходы скрещивания "Aabb" и "Aabb" (неуникальные) это
# 
# ```
# AAbb
# AAbb
# AAbb
# AAbb
# Aabb
# Aabb
# Aabb
# Aabb
# Aabb
# Aabb
# Aabb
# Aabb
# aabb
# aabb
# aabb
# aabb
# ```
# 
# 2. Напишите функцию, которая вычисляет вероятность появления определённого генотипа (его ожидаемую долю в потомстве).
# Например,
# 
# ```python
# get_offspting_genotype_probability(parent1="Aabb", parent2="Aabb", target_genotype="Аabb")   # 0.5
# 
# ```
# 
# 3. Напишите код, который выводит все уникальные генотипы при скрещивании `'АаБбввГгДдЕеЖжЗзИиЙйккЛлМмНн'` и `'АаббВвГгДДЕеЖжЗзИиЙйКкЛлМмНН'`, которые содержат в себе следующую комбинацию аллелей `'АаБбВвГгДдЕеЖжЗзИиЙйКкЛл'`
# 4. Напишите код, который расчитывает вероятность появления генотипа `'АаБбввГгДдЕеЖжЗзИиЙйккЛлМмНн'` при скрещивании `АаБбВвГгДдЕеЖжЗзИиЙйКкЛлМмНн` и `АаБбВвГгДдЕеЖжЗзИиЙйКкЛлМмНн`
# 
# Важные замечания:
# 1. Порядок следования аллелей в случае гетерозигот всегда должен быть следующим: сначала большая буква, затем маленькая (вариант `AaBb` допустим, но `aAbB` быть не должно)
# 2. Подзадачи 3 и 4 могут потребовать много вычислительного времени (до 15+ минут в зависимости от железа), поэтому убедитесь, что вы хорошо протестировали написанный вами код на малых данных перед выполнением этих задач. Если ваш код работает **дольше 20 мин**, то скорее всего ваше решение не оптимально, попытайтесь что-нибудь оптимизировать. Если оптимальное решение совсем не получается, то попробуйте из входных данных во всех заданиях убрать последний ген (это должно уменьшить время выполнения примерно в 4 раза), но **за такое решение будет снято 2 балла**
# 3. Несмотря на то, что подзадания 2, 3 и 4 возможно решить математически, не прибегая к непосредственному получению всех возможных генотипов, от вас требуется именно brute-force вариант алгоритма
# 
# **Можно использовать модули из стандартной библиотеки питона**, но **за выполнение задания без использования модулей придусмотрено +3 дополнительных балла**

# In[6]:


# в равнении с моим первым рабочим вариантом этот работает примерно в 10 раз быстрее
# но все равно крайне медленно
# пускай будет хотя бы так

import itertools

class all_comb():
    def __init__(self, org1, org2):
        self.org1 = org1
        self.org2 = org2
        

    def comb(self):
        genes1 = (self.org1[i:i+2] for i in range(0, len(self.org1), 2))
        genes2 = (self.org2[i:i+2] for i in range(0, len(self.org2), 2))
        
        sep_combs = (itertools.product(gene1, gene2) for gene1, gene2 in zip(genes1, genes2))
        combs = itertools.product(*sep_combs)

        for tpl in combs:
            temp_str = ""
            for inner_tpl in tpl:
                temp_str += "".join(inner_tpl)
            if len(temp_str) >= 4:
                sort = sorted(temp_str, key=lambda x: (x.upper(), x.islower(), temp_str.index(x)))
                yield ''.join(sort)

    def prob(self, genotype):
        combs = self.comb()
        n_comb = 0
        gt_count = 0
        for i in combs:
            n_comb += 1
            if i == genotype:
                gt_count += 1
        prob = gt_count / n_comb
        return prob 

    def cont(self, substring):
        combs = self.comb()
        count = 0
        for i in combs:
            if substring in i:
                count += 1
        return count


# In[4]:


get_ipython().run_cell_magic('time', '', "# Ваш код здесь (3 подзадание)\n\na = all_comb('АаБбввГгДдЕеЖжЗзИиЙйккЛлМм', 'АаббВвГгДДЕеЖжЗзИиЙйКкЛлМм')\na.cont('АаБбВвГгДдЕеЖжЗзИиЙйКк')\n")


# In[5]:


get_ipython().run_cell_magic('time', '', "# Ваш код здесь (4 подзадание)\n\na = all_comb('АаБбВвГгДдЕеЖжЗзИиЙйКкЛлМм', 'АаБбВвГгДдЕеЖжЗзИиЙйКкЛлМм')\na.prob('АаБбввГгДдЕеЖжЗзИиЙйккЛлМм')\n")


# In[ ]:




