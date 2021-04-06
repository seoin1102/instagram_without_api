import json
import base64
import requests
from datetime import datetime

token = 'a9151baac138bde82e0bf7fd342f741109bb3687'
headers= {'Authorization': 'token ' + token,
    'Accept': 'application/json',
    'Content-Type': 'application/json;charset=UTF-8'
    }



def influencer_pk(influencer):
    url ='https://api.staging.dabi-api.com/api/influencer/'
    i=760
    while 1:
        response = requests.get(url+'?offset='+str(i), headers=headers)
        print(response)
        data = response.json()
        print(data)
        result = data['results']
        print(result)
        
        for i2 in range(len(result)):
            if influencer == result[i2]['insta_id']:
                return result[i2]['pk']    
        i+=20
        if data['next']==None:
            with open(f'{influencer}/{influencer}.json','rt', encoding='UTF8') as json_file:
                json_data = json.load(json_file)
                influencer_id = json_data['GraphImages']['owner']['id']
                profile_pic = json_data['GraphImages']['owner']['profile_pic_url']
                base64_bytes = base64.b64encode(requests.get(profile_pic).content)
                image_url = base64_bytes.decode('utf-8')
            print('New influencer')   
            requests.post('https://api.staging.dabi-api.com/api/influencer/', json={"insta_id": influencer, "insta_pk":influencer_id , "profile_image": image_url}, headers=headers)
            influencer_pk(influencer)
            break   

  

def post_pk(pk1, post_url):
    url =f'https://api.staging.dabi-api.com/api/influencer/{pk1}/feedback/'
    i=0
    while 1:
        response = requests.get(url+'?offset='+str(i), headers=headers)
        print(response)
        data = response.json()
        print(data)
        result = data['results']
        print(result)
        
        for i2 in range(len(result)):
            if post_url == result[i2]['post_url']:  
                return post_url
        i+=20
        if data['next']==None:
            break  

def check_post(influencer_id):
    pk = influencer_pk(influencer_id)
    response = requests.get('https://api.staging.dabi-api.com/api/influencer/'+str(pk)+'/feedback/', headers=headers)
    print(response)
    data = response.json()
    print(data)
    result = data['results']
    print(result)
    post_list=[]
    for i in range(len(result)):
        post_list.append(result[i]['post_url'])
       
    return post_list         

influencer_list = []
f = open("ig_users.txt", 'r')
lines = f.readlines()
for i in lines:
    influencer_list.append(i.strip('\n'))
f.close()

pk_1 = {}
for i in influencer_list:
    print(i)
    pk = influencer_pk(i)
    pk_1[i] = pk

for name in influencer_list:
    with open(f'{name}/{name}.json','rt', encoding='UTF8') as json_file:
        json_data = json.load(json_file)
        json_string = json_data['GraphImages']

    for text in range(len(json_string)):
        url = 'https://www.instagram.com/p/' + json_string[text]['shortcode']
        image_url = json_string[text]['thumbnail_src']
        base64_bytes = base64.b64encode(requests.get(image_url).content)
        image_url = base64_bytes.decode('utf-8')
        date_posted_timestamp = json_string[text]['taken_at_timestamp']
        date_posted_human = datetime.fromtimestamp(date_posted_timestamp).strftime("%Y-%m-%d")

        for url in range(len(json_string[text]['urls'])):
            display_url = json_string[text]['urls'][url]
            display_url.replace(r'\u0026', "&")
            base64_bytes = base64.b64encode(requests.get(display_url).content)
            display_url = base64_bytes.decode('utf-8')
            pk1 = influencer_pk(name)
            pk2 = post_pk(pk1, url)
            requests.post(f'https://api.staging.dabi-api.com/api/influencer/{pk1}/feedback/{pk2}/image', json={"source": display_url}, headers=headers)   
            print(requests.post(f'https://api.staging.dabi-api.com/api/influencer/{pk1}/feedback/{pk2}/image', json={"source": display_url}, headers=headers))
        if len(json_string[text]['edge_media_to_caption']['edges']) > 0:
            captions = json_string[text]['edge_media_to_caption']['edges'][0]['node']['text']
            print(captions)

        else:
            captions = "No caption"    
            print(captions)


        requests.post(f'https://api.staging.dabi-api.com/api/influencer/{pk1}/feedback/', json={"post_url": url, "post_thumb_image":image_url ,"post_taken_at_timestamp": date_posted_human,
                    "post_description": captions}, headers=headers)   
        print(requests.post(f'https://api.staging.dabi-api.com/api/influencer/{pk1}/feedback/', json={"post_url": url, "post_thumb_image":image_url ,"post_taken_at_timestamp": date_posted_human,
                    "post_description": captions}, headers=headers))            


