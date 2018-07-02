    # -*- coding: utf-8 -*-
__author__ = 'lizexiong'


import os,sys
import subprocess

def add(nums,*args):
    user_id_list = args[0]
    currency = args[1]
    nums = nums
    for user_id in user_id_list:
        for single_currency in currency:
            try:
                subprocess.call("./add.sh %s %s %s &",shell=True) %(user_id,single_currency,nums)
            except Exception as e:
                print (str(e))


if __name__ == '__main__':
    if len(sys.argv) == 4:
        user_id_list = sys.argv[1].split(',')
        currency = sys.argv[2].upper().split(',')
        nums = sys.argv[3]
        add(nums,user_id_list,currency)
        print (user_id_list,currency,nums)
    else:
        print (
            """输入格式不正确
                python UserID currency Nums
            """)

#add(['10001234'],['BTC'],['1000'])