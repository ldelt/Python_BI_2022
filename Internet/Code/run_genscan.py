import requests
import re
from bs4 import BeautifulSoup
from dataclasses import dataclass

@dataclass
class GenscanOutput:
    status: str
    cds_list: list[str] 
    intron_list: list[list]
    exon_list: list[list] # Каждый экзон - список [Gn.Ex, Type, S, Begin, End]


def find_intron(data):

    intron_list = []
    intron_counter = 0
    for index in range(len(data) - 1):
        if data[index][0].split('.')[0] == data[index + 1][0].split('.')[0] and data[index][0].split('.')[0] != 'S':
            intron_counter += 1
            intron_ID = data[index][0].split('.')[0] + '.' + str(intron_counter)
            type_ = 'Intron'

            if data[index][2] == '+':
                strand = '+'
                start = data[index][4] + 1
                stop = data[index + 1][3] - 1
                intron = [intron_ID, type_, strand, start, stop]

            else:
                strand = '-'
                stop = data[index][3] + 1
                start = data[index + 1][4] - 1 

            intron = [intron_ID, type_, strand, start, stop]

            intron_list.append(intron)
            
        else: 
            intron_counter = 0

    return intron_list


def run_genscan(sequence=None, sequence_file=None, organism="Vertebrate", exon_cutoff=1.00, sequence_name=None):

    # Чтение файла
    if sequence_file is not None:
        with open(sequence_file, 'rb') as f:
            sequence_file = f.read()

    # Отправляемые данные
    form_data = {
        "-s": sequence,
        "-u": sequence_file,
        "-o": organism,
        "-e": exon_cutoff,
        "-n": sequence_name,
        "-p": "Predicted peptides only",
        }

    #URL, на который генскан отправляет заполненную форму
    url ="http://hollywood.mit.edu/cgi-bin/genscanw_py.cgi"

    # Отправляем реквест
    response = requests.post(url, data = form_data)
    status = response.status_code
    soup = BeautifulSoup(response.content, "lxml")

    # Получаем результат в виде текста и по регулярнам находим экзоны и последовательности белков
    data = soup.find("pre").text

    exon_list = []
    for line in data.split('\n'):
        if ('Init' in line) or ('Intr' in line) or ('Term' in line) or ('Sngl' in line) or ('Prom' in line) or ('PlyA' in line):
            elements = line.split()
            exon_list.append([elements[0], elements[1], elements[2], int(elements[3]), int(elements[4])])

    pattern_ex = r">.+?\|GENSCAN_predicted_peptide_\d+\|\d+_aa\n([\s\S]+?)(?=>|$)"
    matches_cds = re.findall(pattern_ex, data)
    cds_list = [match.replace('\n', '') for match in matches_cds]

    # Получаем интроны
    intron_list = find_intron(exon_list)

    # Записываем результат в датакласс
    genscan_output = GenscanOutput(status=str(status), cds_list=cds_list, 
                                   intron_list=intron_list, exon_list=exon_list)

    return genscan_output
