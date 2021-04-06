# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode
import json
import requests
from datetime import datetime

f = open("ig_users.txt", 'w')

# 인플루언서 리스트번호를 입력해서 포스트를 업데이트하는 코드입니다.
#    ex. 0 입력하면 처음부터 마지막 리스트까지 업데이트가 가능합니다.


token = 'a9151baac138bde82e0bf7fd342f741109bb3687'

headers= {'Authorization': 'token ' + token,
    'Accept': 'application/json',
    'Content-Type': 'application/json;charset=UTF-8'
    }
url ='https://api.staging.dabi-api.com/api/influencer/'
user_list = []


def list_update(num):
    num = int(num)
    while 1:
        response = requests.get(url+'?offset='+str(num), headers=headers)
        data = response.json()
        result = data['results']
        
        for i2 in range(len(result)):
            user_list.append(result[i2]['insta_id'])
            k = result[i2]['insta_id']
            f.write(f'{k}\n')
        num+=20
        if data['next']==None:
            print(f'ID added to the list: {user_list}')
            break   




def influencer_list(input_user):
    url ='https://api.staging.dabi-api.com/api/influencer/'

    i=0
    while 1:
        response = requests.get(url+'?offset='+str(i), headers=headers)
        print(response)
        data = response.json()
        result = data['results']
        for i2 in range(len(result)):
            if result[i2]['insta_id'] == input_user:
                print('Registered influencer')
                break
        i+=20
        if data['next']==None:
            print('New influencer')  
            f.write(input_user) 
            break   


input_ = input("1 or 2\n")
if input_== '1':
    num = input("List num: ")
    list_update(num)
    
if input_== '2':
    name = input("User name: ")
    influencer_list(name)

f.close() 