import json
import base64
import requests
import time
from datetime import datetime

token = 'a9151baac138bde82e0bf7fd342f741109bb3687'
headers= {'Authorization': 'token ' + token,
    'Accept': 'application/json',
    'Content-Type': 'application/json;charset=UTF-8'
    }



def influencer_pk(influencer):
    url ='https://api.staging.dabi-api.com/api/influencer/'
    i=0
    while 1:
        # Slow down so we not ddos our own server
        time.sleep(1)
        response = requests.get(url+'?offset='+str(i), headers=headers)
        insta_id_list= []
        # We have to check response is in correct form
        if response:
            # What happen if .json() can not execute ? doing this will not stop our server
            try:
                data = response.json()
            except Exception as e:
                print('Invalid response data in influencer_pk')
                continue
            # Check data is in correct form
            if data:
                # We should use .get when we have a dictionary for safety reason
                result = data.get('results', None)
                # Check result is in correct form
                if result:
                    for i2 in range(len(result)):
                        if influencer == result[i2]['insta_id']:
                            print('I found it!')
                            insta_id_list.append(result[i2]['insta_id'])
                            return result[i2]['pk']
                    i+=20
                    if data['next']==None and influencer not in insta_id_list:
                        with open(f'{influencer}/{influencer}.json','rt', encoding='UTF8') as json_file:
                            json_data = json.load(json_file)
                            json_string = json_data['GraphStories']
                            influencer_id = json_string[0]['owner']['id']
                            profile_pic = json_string[0]['owner']['profile_pic_url']
                            base64_bytes = base64.b64encode(requests.get(profile_pic).content)
                            image_url = base64_bytes.decode('utf-8')
                            print('New influencer')
                            time.sleep(1)
                            requests.post('https://api.staging.dabi-api.com/api/influencer/', json={"insta_id": influencer, "insta_pk":influencer_id , "profile_image": image_url}, headers=headers)
                            time.sleep(10)
                            return influencer_pk(influencer)
                            
                    if data['next']==None:
                        break    



  

def post_pk(pk1, post_url):
    print('find pk')
    url =f'https://api.staging.dabi-api.com/api/influencer/{pk1}/feedback/?is-active=all'
    i=0
    while 1:
        time.sleep(1)
        response = requests.get(url+'&offset='+str(i), headers=headers)
        if response:
            try:
                data = response.json()
            except Exception as e:
                print('Invalid response data in post_pk')
                continue
            if data:
                result = data.get('results', None)
                time.sleep(1)
                if result:
                    for i2 in range(len(result)):
                        if post_url == result[i2]['post_url']:
                            pk = result[i2]['pk']
                            return pk
                        else:
                            print('No post')
                            i+=20
                    if data['next']==None:
                        break
            break            

def check_post(influencer_id):
    print('check post')
    post_list=[]
    pk = pk_1[influencer_id]
    time.sleep(1)
    response = requests.get('https://api.staging.dabi-api.com/api/influencer/'+str(pk)+'/feedback/?is-active=all', headers=headers)

    if response:
        try:
            data = response.json()
        except Exception as e:
            print('Invalid response data in check_post')
        if data:
            result = data.get('results', None)
            if result:
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
    pk = influencer_pk(i)
    time.sleep(2)
    pk_1[i] = pk


for name in influencer_list:
    update_image = 0
    update_post = 0
    with open(f'{name}/{name}.json','rt', encoding='UTF8') as json_file:
        json_data = json.load(json_file)
        json_string = json_data['GraphImages']
        
        post_list = check_post(name)
        
    for text in range(len(json_string)):
        url = 'https://www.instagram.com/p/' + json_string[text]['shortcode']

        if post_list == None:
            post_list = []

        if url in post_list:
            text+=1
            print('Already on the list')

        elif url not in post_list:
            image_url = json_string[text]['thumbnail_src']
            base64_bytes = base64.b64encode(requests.get(image_url).content)
            image_url = base64_bytes.decode('utf-8')
            date_posted_timestamp = json_string[text]['taken_at_timestamp']
            date_posted_human = datetime.fromtimestamp(date_posted_timestamp).strftime("%Y-%m-%d")

            pk1 = pk_1[name]
            if len(json_string[text]['edge_media_to_caption']['edges']) > 0:
                captions = json_string[text]['edge_media_to_caption']['edges'][0]['node']['text']
                

            else:
                captions = "No caption"    
                

            time.sleep(1)  
            
            requests.post(f'https://api.staging.dabi-api.com/api/influencer/{pk1}/feedback/', json={"post_url": url, "post_thumb_image":image_url ,"post_taken_at_timestamp": date_posted_human,
                                "post_description": captions}, headers=headers)       
            update_post+=1                    

            post_list.append(url)
                
            for i in range(len(json_string[text]['urls'])):
                display_url = json_string[text]['urls'][i]
                display_url.replace(r'\u0026', "&")
                base64_bytes = base64.b64encode(requests.get(display_url).content)
                display_url = base64_bytes.decode('utf-8')
                time.sleep(1)
                pk2 = post_pk(pk1, url)
                time.sleep(1)
   
                requests.post(f'https://api.staging.dabi-api.com/api/influencer/{pk1}/feedback/{pk2}/image', json={"source": display_url}, headers=headers)
                update_image+=1
    print(f'{name} uapdate content\npost: {update_post}\nimage: {update_image}')        

              
