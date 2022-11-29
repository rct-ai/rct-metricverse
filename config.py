HYP_PARAMS = {
    "number": 1,
    "length": 20,
    "top_p": 0.9,
    "top_k": 50,
    "temperature": 1.0
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

VIEW = '''
<View>
  <Header value="发送消息"/>
  <Text name="message" value="$message"/>
  <Header value="AI回复"/>
  <Text name="response" value="$response"/>
  <View style="box-shadow: 2px 2px 5px #999;                padding: 20px; margin-top: 2em;                border-radius: 5px;">
    <Header value="你觉得回复是否有明智性（sensibleness）"/>
    <Choices name="sensibleness" toName="response" choice="single" showInLine="true">
      <Choice value="Positive"/>
      <Choice value="Negative"/>
      <Choice value="Neutral"/>
    </Choices>
    <Header value="你觉得回复是否有具体性（specificity）"/>
    <Choices name="specificity" toName="response" choice="single" showInLine="true">
      <Choice value="Positive"/>
      <Choice value="Negative"/>
      <Choice value="Neutral"/>
    </Choices>
    <Header value="你觉得回复是否有趣味性（interestingness）"/>
    <Choices name="interestingness" toName="response" choice="single" showInLine="true">
      <Choice value="Positive"/>
      <Choice value="Negative"/>
      <Choice value="Neutral"/>
    </Choices>
  </View>
  <HyperText name="p1">
    <p>明智性：衡量模型的反应在上下文中是否有意义，并且不与之前所说的任何内容相矛盾</p>
    <p>具体性：用于衡量响应是否具体于给定上下文。 例如，如果用户说“我爱欧洲电视网”，而模型回答“我也是”，那么它的特异性得分为Neutral，因为该响应可以用于许多不同的上下文中。 如果它回答“我也是。 我喜欢欧洲歌唱大赛的歌曲”，那么它将获得Positive。</p>
    <p>趣味性：我们试图将直觉转化为第三个分数，一种我们称之为“有趣”的可观察品质。 与明智性和具体性类似。如果判断它可能“引起某人的注意”或“引起他们的好奇心”，或者如果它是出乎意料的、机智的或有见地的，则获得Positive。</p>
  </HyperText>
</View>
'''