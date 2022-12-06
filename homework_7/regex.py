#!/usr/bin/env python
# coding: utf-8

# In[21]:


import re
import seaborn as sns
import matplotlib.pyplot as plt

from collections import Counter


# In[22]:


def ftp(file, new_file):
    with open(new_file, 'a') as ftps:
        with open(file, 'r') as file:
            for line in file:
                pattern = re.compile(r'ftp\.[^\s;]*')
                parsed = re.findall(pattern, line)
                for string in parsed:
                    ftps.write(string + '\n')
                
ftp('references', 'ftps')


# In[23]:


def find_numbers(line):
    pattern = re.compile(r'(\d+([\.,/]\d+)?)') # Fractional numbers and decimals (with dot or comma)
    gps = re.findall(pattern, line)
    for i in gps:
        numbers.append(i[0])


# In[24]:


def find_words(line):
    pattern = r'\w*[aA]\w*'
    word = re.findall(pattern, line)
    words.extend(word)


# In[25]:


def find_exclamation(line):
    pattern = r'[^\.\?\!]*\!'
    snt = re.findall(pattern, line)
    exclamations.extend(snt)


# In[26]:


def find_un_words(line):
    line = line.lower()
    pattern = r'\b\w+'
    words = set(re.findall(pattern, line))
    unic_words.update(words)


# In[27]:


def make_hist(unic_words):
    list(unic_words)
    counter = dict(Counter(map(len, unic_words)))
    keys = list(counter.keys())
    vals = [counter[k] for k in keys]
    sns.barplot(x=keys, y=vals)
    plt.ylabel(r'Word length frequency', fontstyle='italic', size=12, fontweight='bold')
    plt.xlabel(r'Word length', fontsize=12, fontstyle='italic', fontweight='bold')


# In[28]:


with open('2430AD', 'r') as file:
    numbers = []
    words = []
    exclamations = []
    unic_words = set()
    for line in file:
        line = line.strip()
        find_numbers(line)
        find_words(line)
        find_exclamation(line)
        find_un_words(line)
        
    make_hist(unic_words)
        


# In[29]:


def translate(string):
    pattern = r'([аАяЯуУюЮоОеЕёЁэЭиИыЫ])'
    substitute = r'\1к\1'
    return re.sub(pattern, substitute, st)


# In[ ]:




