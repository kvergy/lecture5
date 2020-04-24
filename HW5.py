import os
import sys
import re

def read_fna(file):
    seq = ""
    
    with open(file,"r") as f:
        for string in f:
            n = string.strip('\n')
            seq += n
    return seq       


def read_vcf(file):
    replace = []
    str_chrom = []
    with open(file,"r") as f:
        for string in f:
            str_replace = []
            chrom = ''
            if "#" not in string:
                
                n = string.strip('\n')
                n = n.split('\t')
                
                str_replace.extend(n[0:2])    
                str_replace.extend(n[3:5]) 
                replace.append(str_replace)  
                """if n[0] == chrom:
                    str_replace.append(n[1])    
                    str_replace.extend(n[3:5])  
                    str_chrom.append(str_replace)
                else:
                    replace.append(str_chrom)    
                    str_chrom = []
                    chrom = n[0]
                    str_chrom.append(n[0])"""
                 
    return replace     
    

def repeat(slicee):
#показывает есть ли повтор в строке на 4-15 нуклеотидов около num
    i = 0
    for lett in "ACTG":
        for repeate in re.finditer(lett+'{4,15}',slicee):
            
            if repeate.start() <= 15 and repeate.end() >=15:
                i = 1
           
    return i      

seq = read_fna("sample_genome.fna")
replace = read_vcf("sample1.vcf")

chromas = re.compile('chr[^A-Z]{1,3}')
res = chromas.findall(seq)



for rep in replace:
    chrom = re.compile(rep[0])
    displace = int(rep[1])
    temp = chrom.search(seq)    
    num = temp.start() + len(rep[0]) + displace -1   
    old_seq = seq[num -15:num + 16]
    old = repeat(old_seq)
    new_seq = seq[num -15:num] + rep[3] + seq[num + len(rep[2]):num + len(rep[2]) + 15]
    new = repeat(new_seq)
    """print(seq[num -15:num + 16])
    print(new_seq)
    print(rep)
    print(seq[num], len(rep[2]) )
    print(old, new)"""
    if old == 1 and new == 0:
        print("Замена в хромосоме {0} на {1} нуклеотида {2} на {3} нарушает тандемный повтор".format(rep[0], rep[1], rep[2], rep[3]))
    elif old == 0 and new == 1:
        print("Замена в хромосоме {0} на {1} нуклеотида {2} на {3} создает тандемный повтор".format(rep[0], rep[1], rep[2], rep[3]))

       
