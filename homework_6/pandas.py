#!/usr/bin/env python
# coding: utf-8

# ## Задание 1. Работа с реальными данным

# In[448]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# In[449]:


def read_gff(path):
    c_names = ['seq_id', 'source', 'type',
                'start', 'end', 'score', 'strand',
                'phase', 'attributes']
    gff_df = pd.read_csv(path, names=c_names, skiprows=1, sep='\t')
    return gff_df


# In[450]:


ann = read_gff('rrna_annotation.gff')
ann


# In[451]:


def only_RNA(df):
    df['attributes'] = df['attributes'].apply(lambda x: x.split('=')[1].split('_')[0])
    return df


# In[452]:


only_RNA(ann)


# In[453]:


def read_bed6(path):
    c_names = ['seq_id', 'start', 'end',
                'name', 'score', 'strand']
    bed_df = pd.read_csv(path, names=c_names, sep='\t')
    return bed_df


# In[454]:


bed = read_bed6('alignment.bed')
bed


# In[455]:


def inter(df1,df2):
    inter_df = df1.merge(df2, on='seq_id').query('(start_x >= start_y) & (end_x <= end_y)')
    return inter_df


# In[456]:


new_df = inter(ann, bed)
new_df


# In[457]:


def rna_counter(df):
    rna_count = df.groupby(['seq_id','attributes']).size().reset_index(name='count')
    return rna_count


# In[458]:


rna_df = rna_counter(ann)
rna_df


# In[459]:


plt.figure(figsize=(10,6))
ax = sns.barplot(data=rna_df, x='seq_id', y='count', hue='attributes')
plt.xticks(rotation=90)


# ## Задание 2. Визуализация данных

# In[460]:


import seaborn as sns
import matplotlib.pyplot as plt
import math
import pandas as pd
import numpy as np

from matplotlib.ticker import AutoMinorLocator


# In[461]:


df = pd.read_csv('diffexpr_data.tsv.gz', sep='\t')
df


# In[462]:


p05 = - math.log10(0.05)


# In[463]:


def group(x):
    if x.log_pval < p05 and x.logFC < 0:
        return 'Non-significantly downregulated'
    elif x.log_pval > p05 and x.logFC < 0:
        return 'Significantly downregulated'
    elif x.log_pval < p05 and x.logFC > 0:\
        return 'Non-significantly upregulated'
    else:
        return 'Significantly upregulated'


# In[464]:


df['new_factor'] = df.apply(group, axis=1)


# In[465]:


group_df = df.groupby('new_factor')
largest = group_df['logFC'].nlargest(2).reset_index()
lowest = group_df['logFC'].nsmallest(2).reset_index()

lar_key_1 = largest.query('new_factor == "Significantly upregulated"')['level_1'].iloc[0]
lar_key_2 = largest.query('new_factor == "Significantly upregulated"')['level_1'].iloc[1]

low_key_1 = lowest.query('new_factor == "Significantly downregulated"')['level_1'].iloc[0]
low_key_2 = lowest.query('new_factor == "Significantly downregulated"')['level_1'].iloc[1]

lar_g1_n = df['Sample'].iloc[lar_key_1]
lar_g1_x = df['logFC'].iloc[lar_key_1]
lar_g1_y = df['log_pval'].iloc[lar_key_1]

lar_g2_n = df['Sample'].iloc[lar_key_2]
lar_g2_x = df['logFC'].iloc[lar_key_2]
lar_g2_y = df['log_pval'].iloc[lar_key_2]

low_g1_n = df['Sample'].iloc[low_key_1]
low_g1_x = df['logFC'].iloc[low_key_1]
low_g1_y = df['log_pval'].iloc[low_key_1]

low_g2_n = df['Sample'].iloc[low_key_2]
low_g2_x = df['logFC'].iloc[low_key_2]
low_g2_y = df['log_pval'].iloc[low_key_2]


# In[466]:


plt.figure(figsize=(10,6))
ax = sns.scatterplot(data=df, x='logFC', y='log_pval', hue='new_factor', s=4.5, linewidth=0,
                     hue_order=['Significantly downregulated', 'Significantly upregulated', 
                                'Non-significantly downregulated', 'Non-significantly upregulated'])
plt.vlines(0, ymin=-10, ymax=140, linestyle="--", color='gray', linewidth=1.3)
plt.hlines(p05, xmin=-13, xmax=13, linestyle="--", color='gray', linewidth=1.3)
plt.ylim(-6, 119)
plt.xlim(-11.8, 11.8)
ax.xaxis.set_minor_locator(AutoMinorLocator(5))
ax.yaxis.set_minor_locator(AutoMinorLocator(4))
ax.legend().set_title('')
ax.legend(prop={'size':'8.5','weight':'bold'}, markerscale=1, shadow=True)
ax.set_title('Volcano plot', fontstyle='italic', size=20, fontweight='bold')
ax.set_ylabel(r'$\bf{-log _{10}}$(p value corrected)', fontstyle='italic', size=12, fontweight='bold')
ax.set_xlabel(r'$\bf{log _{2}}$(fold change)', fontsize=12, fontstyle='italic', fontweight='bold')
ax.text(7, 2, 'p-value = 0.05', fontsize=10, fontweight='bold', color='gray')
ax.xaxis.set_tick_params(which='major', width=1.3)
ax.yaxis.set_tick_params(which='major', width=1.3)
ax.xaxis.set_tick_params(which='minor', width=1.3)
ax.yaxis.set_tick_params(which='minor', width=1.3)
for axis in ['top','bottom','left','right']:
    ax.spines[axis].set_linewidth(1.3)
ax.annotate(text=lar_g1_n, xy=(lar_g1_x, lar_g1_y), size = 6.5, xytext=(3.55, 12), weight='bold',
            arrowprops=dict(width=2, headwidth=4, headlength=5, fc='red', lw=0.4, shrink=0.1))
ax.annotate(text=lar_g2_n, xy=(lar_g2_x, lar_g2_y), size = 6.5, xytext=(3.25, 13), weight='bold',
            arrowprops=dict(width=2, headwidth=4, headlength=5, fc='red', lw=0.4, shrink=0.1))
ax.annotate(text=low_g1_n, xy=(low_g1_x, low_g1_y), size = 6.5, xytext=(-11, 62), weight='bold',
            arrowprops=dict(width=2, headwidth=4, headlength=5, fc='red', lw=0.4, shrink=0.1)),
ax.annotate(text=low_g2_n, xy=(low_g2_x, low_g2_y), size = 6.5, xytext=(-9.3, 12), weight='bold',
            arrowprops=dict(width=2, headwidth=4, headlength=5, fc='red', lw=0.4, shrink=0.1))

