import zipfile
import os.path
import hashlib
import requests
import re

directory_to_extract_to = R'C:\Users\Admin\PycharmProjects\PythonLab_1\directory'
arch_file = R'C:\Users\Admin\PycharmProjects\PythonLab_1\tiff-4.2.0_lab1.zip'

test_zip = zipfile.ZipFile(arch_file)
test_zip.extractall(directory_to_extract_to)
test_zip.close()

txt_files = []
for r, d, f in os.walk(directory_to_extract_to):
    for fs in f:
        if fs.endswith('.txt') == 1:
            txt_files.append(os.path.normpath(os.path.join(r, fs)))

for file in txt_files:
    target_file_data = open(file, 'rb').read()
    result = hashlib.md5(target_file_data).hexdigest()
    print(result)

target_hash = "4636f9ae9fef12ebd56cd39586d33cfb"
target_file = ''
target_file_data = ''

for r, d, f in os.walk(directory_to_extract_to):
    for fs in f:
        file = os.path.join(r, fs)
        t_f_d = open(file, 'rb').read()
        if hashlib.md5(t_f_d).hexdigest() == target_hash:
            target_file = file
            target_file_data = open(file, 'r').read()

print(target_file)
print(target_file_data)

r = requests.get(target_file_data)
result_dct = {}
counter = 0
lines = re.findall(R'<div class="Table-module_row__3TH83">.*?</div>.*?</div>.*?</div>.*?</div>.*?</div>', r.text)
for line in lines:
    if counter == 0:
        headers = re.sub(R'(\<(/?[^\>]+)\>)', ';', line)
        headers = re.findall(r'[А-Яа-яёЁ]+\s?', headers)
        headers[3] = headers[3] + ' ' + headers[4]
        headers.pop(4)
        counter += 1
        continue
    temp = re.sub(r'(\<(/?[^\>]+)\>)', ';', line)
    temp = re.sub(r'\([^)]*\)', '', temp)
    temp = re.sub(r'[A-Za-z]', '', temp)
    temp = temp[5:].strip()
    temp = re.sub(r'\;+', ';', temp)
    temp = re.sub(r'^;', '', temp)
    temp = re.sub(r';$', '', temp)
    temp = re.sub(r';В', 'В', temp)
    temp = re.sub(r'\*', '', temp)
    temp = re.sub(r'_', '-1', temp)
    temp = re.sub(r'\xa0', '', temp)
    tmp_split = re.split(r';', temp)
    country_name = tmp_split[0]
    col1_val = tmp_split[1]
    col2_val = tmp_split[2]
    col3_val = tmp_split[3]
    col4_val = tmp_split[4]

    result_dct[country_name] = {}
    result_dct[country_name][headers[0]] = col1_val
    result_dct[country_name][headers[1]] = col2_val
    result_dct[country_name][headers[2]] = col3_val
    result_dct[country_name][headers[3]] = col4_val
    counter += 1

output = open('data.csv', 'w')
counter = 0
for key in result_dct.keys():
    if counter == 0:
        output.write('Country' + ';' + ';'.join(headers) + '\n')
        counter += 1
        continue
    output.write(key + ';')
    for i in range(0, 4):
        output.write(result_dct[key][headers[i]] + ';')
    output.write('\n')
output.close()

try:
    target_country = input("Enter the name of the country: ")
    print(result_dct[target_country])
except KeyError:
    print("Unknown country")


