# -*- coding:UTF8 -*-
import re
import pandas
import numpy as np
import pandas as pd
import os
import glob
def get_exception_pid(line):
    pattern_exception_PID = re.compile(r'----- pid (.*) at')
    result_PID = pattern_exception_PID.findall(line)
    return result_PID
def get_exception_pkgname(line_unre):
    pkg_name_group = re.search( r'Cmd line: (.*)', line_unre, re.M|re.I)
    pkg_name = pkg_name_group.group(1)
    return pkg_name  
def get_exception_content(PID,new_line):
    global content
    key = '----- end {0} -----\n'.format(int(PID))
    #print PID
    for index_end,line in enumerate(new_line):
        if line == key:
            content = ''.join(new_line[0:index_end+2])
    return content
def get_ANR_loc(line):
    pattern_ANR = re.compile(r'// NOT RESPONDING: (.*)')
    ANR = pattern_ANR.findall(line)
    return ANR 
def get_ANR_pkgname(line_unre):
    pkg_name_group = re.search( r'ANR in (.*)', line_unre, re.M|re.I)
    pkg_name = pkg_name_group.group(1)
    return pkg_name    
def get_ANR_content(new_line):
    global content
    content = ''.join(new_line)
    return content     
def get_crash_loc(line):
    pattern_crash = re.compile(r'// CRASH: (.*)')
    crash = pattern_crash.findall(line)
    return crash 
def get_crash_pkgname(line_unre):
    pkg_name_group = re.search( r'// CRASH: (.*) (.*) (.*)', line_unre, re.M|re.I)
    pkg_name = pkg_name_group.group(1)
    return pkg_name 
def get_crash_content(new_line):
    global content
    for i,j in enumerate(new_line):
        if "//" not in j:
            end_line = i
    
    content = ''.join(new_line[0:i+1])
    return content 
if __name__ == '__main__':
    #file=open('./demo.txt',"r")
    #file_lst = file.readlines()
    df = pd.DataFrame([['Type','Package','Content']])
    cate=[x for x in os.listdir("./")]
    
    
    #print cate
    for i in cate:
        t = re.search( r'(.*).log', i, re.M|re.I)
        if t:
            #print t.group(1)
            file=open('./{0}.log'.format(t.group(1)),"r")
            file_lst = file.readlines()
            for i,j in enumerate(file_lst):
                #查看三种error关键字，每行
                exception_PID = get_exception_pid(j) #exception
                ANR_check = get_ANR_loc(j)#此处是ANR func
                crash_check = get_crash_loc(j)
                #此处是crash func
                if exception_PID:
                    package_name = get_exception_pkgname(file_lst[i+1])
                    part_file_lst = file_lst[i:i+2000]
                    exception_content = get_exception_content(exception_PID[0],part_file_lst)
                    df_row = ['Exception',package_name,exception_content]
                    df = df.append([df_row],ignore_index=True)
                elif ANR_check: #此处是ANR 
                    package_name = get_ANR_pkgname(file_lst[i+1])
                    part_file_lst = file_lst[i:i+120]
                    ANR_content = get_ANR_content(part_file_lst)
                    df_row = ['ANR',package_name,ANR_content]
                    df = df.append([df_row],ignore_index=True)
                elif crash_check:#此处是crash
                    package_name = get_crash_pkgname(file_lst[i])
                    part_file_lst = file_lst[i:i+150]
                    crash_content = get_crash_content(part_file_lst)
                    df_row = ['Crash',package_name,crash_content]
                    df = df.append([df_row],ignore_index=True)
                else:
                    pass
            df.to_excel('{0}.xlsx'.format(t.group(1)), sheet_name='output',header=False, index=False)
            print "{0} analysis done!".format(t.group(1))
            
        