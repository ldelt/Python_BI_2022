def test_rna_or_dna(lst):
    dna = {'a','t','g','c','A','T','G','C'}
    rna = {'a','u','g','c','A','U','G','C'}
    st_set = set(lst)
    if st_set.issubset(dna) and lst != '':
        result = 'dna'
    elif st_set.issubset(rna) and lst != '':
        result = 'rna'
    else:
        result = 'Invalid Alphabet. Try again!'
    return result
    
            
def transcribe(lst):
    result = test_rna_or_dna(lst)
    if result == 'rna':
        trna = 'You have entered an RNA sequence, but this function only works with DNA. Try again and enter DNA sequence.'
        return trna
    elif result != 'dna':
        return result
    rna_dic = {'t':'u', 'T':'U'}
    trna = ''
    for i in lst:
        if i in rna_dic:
            trna = trna + rna_dic[i]
        else:
            trna = trna + i
    return trna


def reverse(lst):
    result = test_rna_or_dna(lst)
    if result != 'dna' and result != 'rna':
        return result
    rev = lst[::-1]
    return rev
    

def complement(lst):
    comp_dic_dna = {'a':'t', 'A':'T', 't':'a', 'T':'A', 'c':'g', 'C':'G', 'g':'c', 'G':'C'}
    comp_dic_rna = {'a':'u', 'A':'U', 'u':'a', 'U':'A', 'c':'g', 'C':'G', 'g':'c', 'G':'C'}
    comp_dic = {}
    comp = ''
    result = test_rna_or_dna(lst)
    if result == 'dna':
        comp_dic = comp_dic_dna
    elif result == 'rna':
        comp_dic = comp_dic_rna
    else:
        return result
    for i in lst:
        comp = comp + comp_dic[i]
    return comp
    
    
def reverse_complement(lst):
    comp = complement(lst)
    rev_c = reverse(comp)
    return rev_c
    
    
def prog():
    while True:
        com = input('Enter command: ')
        if com == 'transcribe':
            seq = input('Enter sequence: ')
            print(transcribe(seq))
        elif com == 'reverse':
            seq = input('Enter sequence: ')
            print(reverse(seq))
        elif com == 'complement':
            seq = input('Enter sequence: ')
            print(complement(seq))
        elif com == 'exit':
            print('Good luck!')
            return
        elif com == 'reverse complement':
            seq = input('Enter sequence: ')
            print(reverse_complement(seq))
        else:
            print('Wrong command. Try again!')
            
            
prog()