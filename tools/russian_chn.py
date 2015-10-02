import re
import MySQLdb as mysql
def lingoes2dic():
    dicpath = '/home/hehe/Programming/dics/kdictionary-lingoes/output.txt'
    dic = {}
    pattern = re.compile(ur'([^\u4e00-\u9fff]+)(.+)')
    with open(dicpath) as f:
        for line in f:
            # print line
            word,full_meaning = line.split('=', 1) # max split length=2
            word = word.decode('utf8')
            full_meaning = full_meaning.decode('utf8')
            all_part = pattern.findall(full_meaning)
            all_part = all_part[0]
            variants = all_part[0].strip().split('|')
            meaning = all_part[1].strip()
            dic.setdefault(word,{})
            dic[word]['variants'] = variants
            dic[word]['meaning'] = meaning
            # print all_part[1]
    return dic
def insert2mysql(cursor, dic):
    sql = '''insert into russian_chn (word, variants, meaning) values (%s, %s, %s)'''
    for key in dic.keys():
        print key
        variant_string = ','.join(dic[key]['variants'])
        values = [key, variant_string, dic[key]['meaning']]
        cursor.execute(sql, values)
if __name__ == '__main__':
    dictionary = lingoes2dic()
    connection=mysql.connect(charset='utf8', host='localhost',user='root', passwd='password',db='russian')
    cursor=connection.cursor()
    insert2mysql(cursor, dictionary)
    cursor.close()
    connection.commit()
    connection.close()
    print 'finished'