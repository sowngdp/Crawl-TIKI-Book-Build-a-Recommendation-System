import requests
import pandas as pd
import time
import random
from tqdm import tqdm


cookies = {
    'TOKENS': '{%22access_token%22:%22qZiGHb0Td8XMI2ajroStwKDR4OnUs3Ql%22}',
    '_trackity': '55366ea5-ba26-a8f8-ed65-9cff43ee38c4',
    '_ga': 'GA1.2.288386721.1665365821',
    'tiki_client_id': '288386721.1665365821',
    'TKSESSID': 'f7fe638fbb23d5841d32c07f4a13c00c',
    'TIKI_RECOMMENDATION': '88b1b14b31441df49ac28336d8407e54',
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'Referer': 'https://tiki.vn/so-ke-hoach-planner-18-thang-2023-2024-sdstationery-dream-crafter-48-trang-16-5x20-5cm-p249009518.html?itm_campaign=CTP_YPD_TKA_PLA_UNK_ALL_UNK_UNK_UNK_UNK_X.273998_Y.1856318_Z.3861366_CN.So-2024&itm_medium=CPC&itm_source=tiki-ads&spid=249009520',
    'x-guest-token': 'qZiGHb0Td8XMI2ajroStwKDR4OnUs3Ql',
}

params = {
    'product_id': '249009518',
    'sort': 'score|desc,id|desc,stars|all',
    'page': '1',
    'limit': '10',
    'include': 'comments,contribute_info,attribute_vote_summary',
    'spid': '249009520',
    'seller_id': '148',
}

def comment_parser(json):
    d = dict()
    d['id'] = json.get(id)
    d['title'] = json.get('title')
    d['content'] = json.get('content')
    d['thank_count'] = json.get('thank_count')
    d['customer_id']  = json.get('customer_id')
    d['rating'] = json.get('rating')
    d['created_at'] = json.get('created_at')
    d['customer_name'] = json.get('created_by').get('name')
    d['purchased_at'] = json.get('created_by').get('purchased_at')
    return d


df_id = pd.read_csv('product_id_ncds.csv')
p_ids = df_id.id.to_list()
result = []
for pid in tqdm(p_ids, total=len(p_ids)):
    params['product_id'] = pid
    print('Crawl comment for product {}'.format(pid))
    for i in range(2):
        params['page'] = i
        response = requests.get('https://tiki.vn/api/v2/reviews', headers=headers, params=params, cookies=cookies)
        if response.status_code == 200:
            print('Crawl comment page {} success!!!'.format(i))
            for comment in response.json().get('data'):
                result.append(comment_parser(comment))
df_comment = pd.DataFrame(result)
df_comment.to_csv('comments_data_ncds.csv', index=False)