import json

import pandas as pd
import requests
import streamlit as st
import re
import datetime
from config import headers
from tools import get_test_data, convert_df


def app():
    st.set_page_config(page_title="dialogue metric", page_icon="🤖️")

    st.write("# Dialogue Metric :ghost:")
    st.write("## 对话参数配置 ")
    URL = {}
    accessKey = {}
    accessToken = {}
    ai_name = {}
    params = {}
    ai_nums = 2
    for i in range(ai_nums):
        st.write("### 对话AI-{}参数配置 ".format(i))
        URL[i] = st.text_input("对话请求地址-{}".format(i), "https://socrates-api.rct.ai/v1/applications/222/nodes/ed19e08c-8223-4982-b0e1-071635e1847a/conversation")
        accessKey[i] = st.text_input("accessKey-{}".format(i), 'ab2f2d27-0705-4268-b5ac-b954746504cd')
        accessToken[i] = st.text_input("accessToken-{}".format(i), '6d0139d3-b7f1-427d-95eb-86354ce467d6')
        ai_name[i] = st.text_input("AI NAME-{}".format(i), "bot")
        params[i] = {"accessKey": accessKey[i],
                     "accessToken": accessToken[i]}

    st.write("### 参数配置 ")
    first_message = st.text_input("启发信息（第一个AI主动发出的消息）", "Hi!")
    dialog_num = int(st.number_input("对话次数", 1, step=1))
    dialog_round = int(st.number_input("每次对话轮数", 1, step=1))

    start = st.button("开始测试")
    if start:
        for i in range(ai_nums):
            if (not re.match(r'^https?:/{2}\w.+$', URL[i])) or (len(accessKey[i]) < 2) or (len(accessToken[i]) < 2):
                st.error("非法参数")
                st.stop()

        with st.container():
            my_bar = st.progress(0)
            step = 100 / dialog_num
            dialog_history = [pd.DataFrame({"conversation_id": [],
                                            "data_source": [],
                                            "dialog_round": [],
                                            "knowledge": [],
                                            "message": [],
                                            "response": []}) for _ in range(ai_nums)]

            with st.spinner("请耐心等待 ..."):
                for n in range(dialog_num):
                    message = first_message
                    for r in range(dialog_round):
                        tmp = {}
                        try:
                            for i in range(ai_nums):
                                result = requests.post(URL[i], params=params[i], headers=headers, json={"text": message})
                                response = json.loads(result.text)["data"][0]["text"].strip()
                                tmp[i] = {"conversation_id": 0, "data_source": ai_name[i],
                                          "dialog_round": r, "knowledge": None,
                                          "message": message, "response": response}
                                message = response

                        except requests.exceptions.ConnectionError \
                               or requests.exceptions.ConnectTimeout or \
                               requests.exceptions.SSLError:

                            st.warning("请求丢失数据: {}".format(i))
                            continue

                        for i in range(ai_nums):
                            dialog_history[i].loc[len(dialog_history[i])] = tmp[i]

                    my_bar.progress(round(step))
                    step += step

            for i in range(ai_nums):
                dialog_history_csv = {}
                if not dialog_history[i].empty:
                    with st.expander("预览AI {}结果数据".format(i)):
                        st.dataframe(dialog_history[i])

                    dialog_history_csv[i] = convert_df(dialog_history[i])
                    st.download_button('下载AI {}结果数据'.format(i), dialog_history_csv[i],
                                       file_name="dialogue-{}-{}".format(ai_name[i], datetime.datetime.now().strftime(
                                           '%Y-%m-%d_%H-%M-%S')),
                                       mime='text/csv')


if __name__ == "__main__":
    app()
