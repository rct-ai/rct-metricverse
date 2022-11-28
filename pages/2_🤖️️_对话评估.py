import json

import pandas as pd
import requests
import streamlit as st
import re
import datetime
from config import headers
from tools import get_test_data, convert_df


def app():
    st.set_page_config(page_title="dialogue metric", page_icon="🤖️️")

    st.write("# Dialogue Metric :ghost:")
    st.markdown('''
    ***相关参数说明***
    - AI NAME: 虚拟人名字
    ''')
    st.write("## 对话参数配置 ")
    URL = st.text_input("对话请求地址",
                        "https://socrates-api.rct.ai/v1/applications/222/nodes/ed19e08c-8223-4982-b0e1-071635e1847a/conversation")
    accessKey = st.text_input("accessKey", 'ab2f2d27-0705-4268-b5ac-b954746504cd')
    accessToken = st.text_input("accessToken", '6d0139d3-b7f1-427d-95eb-86354ce467d6')
    ai_name = st.text_input("AI NAME", "bot")
    params = {"accessKey": accessKey,
              "accessToken": accessToken}

    with st.container():
        data_type = st.radio("准备测试数据",
                             ('使用已有测试数据', '上传测试数据'), horizontal=True)
        test_data = get_test_data(data_type)

        with st.expander("预览测试数据"):
            if not test_data.empty:
                st.dataframe(test_data)
            else:
                st.write("没有数据")

    start = st.button("开始测试")
    if start:
        if (not re.match(r'^https?:/{2}\w.+$', URL)) or (len(accessKey) < 2) or (len(accessToken) < 2):
            st.error("非法参数")
            st.stop()

        if test_data.empty:
            st.warning("请准备好测试数据")
            st.stop()

        with st.container():
            my_bar = st.progress(0)
            step = 100 / len(test_data)
            dialog_history = pd.DataFrame({"conversation_id": [],
                                           "data_source": [],
                                           "dialog_round": [],
                                           "knowledge": [],
                                           "message": [],
                                           "response": []})
            compara_data = pd.DataFrame({"references": [],
                                         "predictions": []})

            with st.spinner("请耐心等待 ..."):
                for index, row in test_data.iterrows():
                    try:
                        result = requests.post(URL, params=params, headers=headers, json={"text": row["message"]})
                    except requests.exceptions.ConnectionError \
                           or requests.exceptions.ConnectTimeout or \
                           requests.exceptions.SSLError:
                        st.warning("请求丢失数据: {}".format(index))
                        continue

                    response = json.loads(result.text)["data"][0]["text"].strip()
                    tmp = {"conversation_id": row["conversation_id"], "data_source": ai_name,
                           "dialog_round": row["dialog_round"], "knowledge": row["knowledge"],
                           "message": row["message"], "response": response}

                    tmp1 = {"references": row["response"],
                            "predictions": response}

                    dialog_history.loc[len(dialog_history)] = tmp
                    compara_data.loc[len(compara_data)] = tmp1
                    my_bar.progress(round(step * (index + 1)))

            if not dialog_history.empty:
                with st.expander("预览结果数据"):
                    st.dataframe(dialog_history)

                dialog_history_csv = convert_df(dialog_history)
                st.download_button('下载结果数据', dialog_history_csv,
                                   file_name="dialogue-{}-{}.csv".format(ai_name, datetime.datetime.now().strftime(
                                       '%Y-%m-%d_%H-%M-%S')),
                                   mime='text/csv')

            if not compara_data.empty:
                with st.expander("预览response对比数据"):
                    st.dataframe(compara_data)

                compara_data_csv = convert_df(compara_data)
                st.download_button('下载response对比数据', compara_data_csv,
                                   file_name="dialogue_response-{}-{}.csv".format(ai_name, datetime.datetime.now().strftime(
                                       '%Y-%m-%d_%H-%M-%S')),
                                   mime='text/csv')


if __name__ == "__main__":
    app()
