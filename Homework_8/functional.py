#!/usr/bin/env python
# coding: utf-8

# In[212]:


def sequential_map(*args, str_iter=True):
    container = args[-1] 
    
    if str_iter == True or type(container) != str: 
        try:
            for function in args[0:-1]:
                container = map(function, container)
            return list(container)
        except TypeError:
            for function in args[0:-1]:
                container = function(container)  
            return container
              
    else:
        for function in args[0:-1]:
            container = function(container)
        return container


# In[57]:


def consensus_filter(*args):
    container = args[-1] 
    ty = type(container)
    for function in args[0:-1]:
        container = filter(function, container)
    return ty(container)


# In[111]:


def conditional_reduce(func_con, fun_red, container):
    container = list(filter(func_con, container))
    while True:
        try: 
            container[1] = fun_red(container[0], container[1])
            container = container[1:]
        except IndexError:
            break
    return container[0]


# In[188]:


def func_chain(*args):
    args = list(args)
    def my_chain(value, **kwargs):
        args.append(value)
        return sequential_map(*args, **kwargs)
    return my_chain


# In[340]:


def multiple_partial(*args, **kwargs):
    function_list = []
    def create(fun):
        return lambda *args2, **kwargs2: fun(*args2, **kwargs2, **kwargs)
    for i in args:
        function_list.append(create(i))
    return function_list

