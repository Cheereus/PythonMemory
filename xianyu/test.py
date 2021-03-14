
def get_assay_after(assay):
    tmp_word = ''
    last_str = ''
    tmp_str = ''
    tmp_C = ''
    assay_after = ''
    is_first = True
    is_good_word = False
    for c in assay:
        tmp_str += c
        if c.isalpha():
            if c.isupper():
                tmp_C += c
        else:
            if tmp_str.istitle() and len(tmp_str.split(' ')[0]) == 1:
                print(111)
                print(tmp_str)
                last_str = tmp_str
                is_good_word = False
                assay_after = assay_after + tmp_str[:-1] + c
                tmp_str = ''
                tmp_C = ''
            elif tmp_str.istitle() and len(tmp_str.split(' ')) >= 2:
                last_str = tmp_str
                if is_good_word and not c.isspace():
                    assay_after = assay_after + tmp_C + '(' + tmp_str[:-1].replace(' ', '') + ')' + c
                    tmp_str = ''
                    tmp_C = ''
                is_good_word = True
            elif last_str.istitle() and len(last_str.split(' ')) >= 3 and len(tmp_str.split(' ')) >= 3 and not tmp_str.istitle():
                assay_after = assay_after + tmp_C + '(' + last_str[:-1].replace(' ', '') + ')' + c + tmp_str[len(last_str):]
                last_str = ''
                tmp_str = ''
                tmp_C = ''
                is_good_word = False
            else:
                last_str = tmp_str
                is_good_word = False
                assay_after = assay_after + tmp_str[:-1] + c
                tmp_str = ''
                tmp_C = ''
    return assay_after


a_f = ''
while True:
    a = input()
    aaa = get_assay_after(a)
    a_f = a_f + aaa
    if a[-1] == '.':
        break

print(a_f)
