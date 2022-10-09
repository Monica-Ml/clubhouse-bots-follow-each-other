import requests
import time
import sys
import json

def get_token_list(token_list_address):
    tokens_array = []
    # read token list from file
    file = open(token_list_address)
    for token in file:
        # read token
        token = token.replace('\n', '')
        # check not null
        if token:
            # add tokens to array
            tokens_array.append(token)
    if len(tokens_array) > 0:
        return True, tokens_array
    else:
        return False, 'cant fetch token list'
        

def get_bots_username_list(username_list_address):
    username_array = []
    # read username list from file
    file = open(username_list_address)
    for username in file:
        # read username
        username = username.replace('\n', '')
        # check not null
        if username:
            # add username to array
            username_array.append(username)
    if len(username_array) > 0:
        return True, username_array
    else:
        return False, 'cant fetch username list'

def get_user_id(token, username, cofollows_only=False, following_only=False, followers_only=False):
    url = "https://www.clubhouseapi.com/api/search_users"
    headers = {
        'CH-Languages': 'en-US',
        'CH-Locale': 'en_US',
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate',
        'CH-AppBuild': '305',
        'CH-AppVersion': '1.0.9',
        'CH-UserID': '1387526936',
        'User-Agent': 'clubhouse/305 (iPhone; iOS 14.4; Scale/2.00)',
        'Connection': 'close',
        'Content-Type': 'application/json; charset=utf-8',
        'Authorization': 'Token ' + token
    }
    data = {
        "cofollows_only": cofollows_only,
        "following_only": following_only,
        "followers_only": followers_only,
        "query": username
    }
    resp = requests.post(url, headers=headers, json=data)
    return str(resp.status_code), resp.content        
        
def search_username(token_list_array, token_count, target_username):
    while True:
        loop_counter = 0
        for token in token_list_array:
            loop_counter = loop_counter + 1
            if (loop_counter <= token_count):
                r_flg, r_user_info_array = get_user_id(token, target_username)
                if (r_flg == '200'):
                    user_info_array_json = json.loads(r_user_info_array)
                    counter_user_info = 0
                    if (len(user_info_array_json['users']) >= 1):
                        return True, counter_user_info, user_info_array_json['users']
        return False, 'cant search username', ''

def follow_user(token, user_id, source=4):
    url = "https://www.clubhouseapi.com/api/follow"
    headers = {
        'CH-Languages': 'en-US',
        'CH-Locale': 'en_US',
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate',
        'CH-AppBuild': '305',
        'CH-AppVersion': '1.0.9',
        'CH-UserID': '1387526936',
        'User-Agent': 'clubhouse/305 (iPhone; iOS 14.4; Scale/2.00)',
        'Connection': 'close',
        'Content-Type': 'application/json; charset=utf-8',
        'Authorization': 'Token ' + token
    }
    data = {
        "user_id": user_id,
        "source": source
    }
    resp = requests.post(url, headers=headers,timeout=10, json=data)
    return str(resp.status_code), resp.content
       
def follow_users(token_list_array,token_count, username_array):
    for target_username in username_array:
        # get username
        r_flg, r_result_len, r_result_array = search_username(token_list_array, token_count, target_username)
        if (r_flg == True):
            r_result_len = int(r_result_len)
            while True:
                target_array_index = 0
                follow_user_id = r_result_array[target_array_index]['user_id']
                follow_username = r_result_array[target_array_index]['username']
                follow_counter = 0
                for token in token_list_array:
                    follow_counter = follow_counter + 1
                    if (follow_counter <= token_count):
                        #time.sleep(2)
                        r_flg_follow, r_result_follow = follow_user(token, follow_user_id)
                        if (r_flg_follow == '200'):
                            print('bot-> '+token+' ->' + str(follow_counter) + '-> follow ' + str(target_username) + '-> successfully')
                        else:
                            print('bot-> '+token+' ->' + str(follow_counter) + '-> follow ' + str(target_username) + '-> failed')
                print('===============================================')
                time.sleep(30)
                break                
        else:
            print('Username not found => @'+str(target_username))


# get token list
token_list_status, tokens_array = get_token_list('tokens.txt')
if (token_list_status):
    # check tokens
    counter_token = 0
    counter_number=0
    username_list_status, username_array = get_bots_username_list('bots_username_list.txt')
    if (username_list_status):
        counter_number=counter_number+1
        token_count = len(tokens_array)
        follow_users(tokens_array,token_count, username_array)
        print('===============================================')
        print('total valid token=>' + str(counter_token) + ' from=>' + str(len(tokens_array)) + ' token')
        if counter_token == 0:
            print('canot find valid token')
    else:
        print('username list file is empty')
else:
    print('token list file is empty')