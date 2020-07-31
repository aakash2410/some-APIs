import requests
from json import loads
from bs4 import BeautifulSoup
def scrape_data(username):
    response = requests.get("https://www.instagram.com/{}/".format(username))
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        scripts = soup.find_all('script')
        try:
            data_script = scripts[4]
            content = data_script.contents[0]
            data_object = content[content.find('{"config"') : -1]
            data_json = loads(data_object)
            data_json = data_json['entry_data']['ProfilePage'][0]['graphql']['user']
            return data_json
        except ValueError:
            data_script = scripts[3]
            content = data_script.contents[0]
            data_object = content[content.find('{"config"') : -1]
            data_json = loads(data_object)
            data_json = data_json['entry_data']['ProfilePage'][0]['graphql']['user']
            return data_json
    else:
        print('Account Not found, please check the username')
        return None


def get_data(data_json):
    if data_json != None:
        results = {
            'biography' : data_json['biography'],
            'external_url' : data_json['external_url'],
            'followers_count': data_json['edge_followed_by']['count'],
            'following_count': data_json['edge_follow']['count'],
            'full_name': data_json['full_name'],
            'dp_url': data_json['profile_pic_url_hd'],
            'username': data_json['username'],
            'is_private': data_json['is_private'],
            'posts':data_json['edge_owner_to_timeline_media']['count']
        }
        return results
    else:
        pass

def clean_data(username):
    
    data = get_data(scrape_data(username))
    if data !=None:
        bio_length = len(data['biography'])
        if data['external_url'] == None:
            ext_url = 0
        else:
            ext_url = 1
        followers = data['followers_count']
        following = data['following_count']
        fullname_words = len(data['full_name'].split(' '))
        num_count_ui = 0
        for i in username:
            if i.isdigit():
                num_count_ui += 1
            else:
                pass
        num_per_user = num_count_ui/len(username)
        num_count_name = 0
        for j in data['full_name']:
            if i.isdigit():
                num_count_name += 1
            else:
                pass
        try:    
            num_per_name = num_count_name/len(data['full_name'])
        except ZeroDivisionError:
            num_per_name = num_count_name
        name_user_same = 0
        for k in data['full_name'].split(" "):
            if k.lower() in username.lower():
                name_user_same = 1
            else:
                pass
                
        
        if '44884218_345707102882519_2446069589734326272_n.jpg' in data['dp_url']:
            profile_pic = 0
        else:
            profile_pic = 1
        private = data['is_private']
        posts = data['posts']

        cleaned_data = {
            'profile_pic': [float(profile_pic)],
            'num_per_user': [float(num_per_user)],
            'fullname_words': [float(fullname_words)],
            'num_per_name': [float(num_per_name)],
            'num_user_same': [float(name_user_same)],
            'bio_length': [float(bio_length)],
            'external_url': [float(ext_url)],
            'private': [float(private)],
            'posts': [float(posts)],
            'followers': [float(followers)],
            'following': [float(following)],
        
        }

        return cleaned_data
    else:
        return None 

if __name__ == '__main__':
    print(clean_data('aakash.sangani1'))
