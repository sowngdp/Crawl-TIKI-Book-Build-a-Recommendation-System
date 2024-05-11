import requests
import time
import random
import pandas as pd

cookies = {
    'cto_bundle': 'OpdQHF9IJTJCR0YyNEJPWTRuUktNcFY1dFA0OWdjUGRJWW1Yek1NZEN5JTJGTjB1M2wzcm1VJTJCUGhodlNUY3Y0cTZNWUY2S2ZBNTJNS1lmSXczbWdxVk9UdDNNVkZQNkpqTE81V3UzdXFrS20xbWNFTGRnOWFPdTE0ZTJpQ2pyTVdaREhvTHFzUkxMczFiT0dTbW11JTJGSk5YRzdsR3BHdyUzRCUzRA',
    'TOKENS': '{%22access_token%22:%224950hSYN8o1cMWVFyHCqdtOkDpUeEKfJ%22%2C%22expires_in%22:157680000%2C%22expires_at%22:1873036437233%2C%22guest_token%22:%224950hSYN8o1cMWVFyHCqdtOkDpUeEKfJ%22}',
    '_gcl_au': '1.1.264536885.1715356436',
    'delivery_zone': 'Vk4wMjUwMDMwMDM=',
    '_hjSession_522327': 'eyJpZCI6IjUxZGJkYjUwLWUwYTEtNDcwMi05YTk4LTE2YWU2ZjYzZDRlZCIsImMiOjE3MTUzNTY0MzY0NTMsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MH0=',
    '_hjSessionUser_522327': 'eyJpZCI6Ijg4MTZmZjg4LTc3ODgtNWU2Mi04ZDU0LWNiZDhjYTljN2YyZCIsImNyZWF0ZWQiOjE3MTUzNTY0MzY0NTEsImV4aXN0aW5nIjp0cnVlfQ==',
    '__uidac': '01663e4314fc627b46d68fd72c5866ab',
    'dtdz': 'd62e761f-760f-5b20-88c0-1a722f48bd21',
    '__RC': '31',
    '__R': '2',
    '__adm_upl': 'eyJ0aW1lIjoxNzE1MzYwNjA3LCJfdXBsIjoiMC05MDA5MDEzNzAyMzU2NDY1NTkwIn0=',
    '_trackity': 'd63eca42-0960-d0de-9537-b9fe6138dde6',
    '_ga': 'GA1.1.1359842104.1715356433',
    'au_aid': '11935756853',
    '__iid': '749',
    '__su': '0',
    '__tb': '0',
    '__IP': '251319713',
    '__uif': '__uid%3A9009013702356465590%7C__ui%3A1%252C6%7C__create%3A1709013705',
    '_gid': 'GA1.2.867846791.1605974237',
    '_fbp': 'fb.1.1715356437248.970911423',
    'tiki_client_id': '1359842104.1715356433',
    '_ga_S9GLR1RQFJ': 'GS1.1.1715358775.2.1.1715360331.60.0.0',
    'amp_99d374': 'IHItCFf-LwrDZL8NZ1QgV8...1hthljct7.1hthn3160.m.16.1s',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9,vi;q=0.8',
    'Referer': 'https://tiki.vn/nha-sach-tiki/c8322',
    'x-guest-token': '4950hSYN8o1cMWVFyHCqdtOkDpUeEKfJ',
}

params = {
    'limit': '10',
    'include': 'advertisement',
    'aggregations': '2',
    'trackity_id': 'd63eca42-0960-d0de-9537-b9fe6138dde6',
    'category': '8322',
    'page': '1',
    'version': 'home-persionalized',
    'urlKey':  'nha-sach-tiki',
}

product_id = []
for i in range(1, 11):
    params['page'] = i
    response = requests.get('https://tiki.vn/api/personalish/v1/blocks/listings', headers=headers, params=params) #, cookies=cookies)
    if response.status_code == 200:
        print('request success!!!')
        for record in response.json().get('data'):
            product_id.append({'id': record.get('id')})
    time.sleep(random.randrange(3, 10))

df = pd.DataFrame(product_id)
df.to_csv('product_id.csv', index=False)