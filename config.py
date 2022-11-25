HYP_PARAMS = {
    "number": 1,
    "length": 20,
    "top_p": 0.9,
    "top_k": 50,
    "temperature": 1
}

TESTDATA_PATH = './test_data'


headers = {
    'authority': 'socrates-api.rct.ai',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://socrates.rct.ai',
    'referer': 'https://socrates.rct.ai/',
    'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
}

EXAMPLE = {1: '''conversation_id	data_source	dialog_round	knowledge	message	response
0	human	0		Hi!	What is your favorite holiday?
0	human	1		one where I get to meet lots of different people.	What was the most number of people you have ever met during a holiday?
0	human	2		Hard to keep a count. Maybe 25.	Which holiday was that?''',
           2: '''references	predictions
What is your favorite holiday?	 Hello!
What was the most number of people you have ever met during a holiday?	 That sounds great!
Which holiday was that?	  That's a lot of people!'''}
