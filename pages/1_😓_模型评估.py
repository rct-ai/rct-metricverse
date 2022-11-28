import streamlit as st
import re
import requests
import json
import datetime
import pandas as pd
from config import HYP_PARAMS
from tools import fund, get_test_data, convert_df


def app():
    st.set_page_config(page_title="model metric", page_icon="😓")

    st.write("# Model Metric :ghost:")
    st.markdown('''
    ***相关参数说明***
    - Dialogue Q name: 用户在prompt发送消息的名字
    - Dialogue A name: AI在prompt回答消息的名字
    - Prompt Q message: 用户在prompt发送的消息，引出AI的回答
    ''')
    st.write("## 模型参数配置 ")
    URL = st.text_input("模型请求地址", "http://47.57.69.130:8015/z")

    hyp_params = HYP_PARAMS.copy()
    col = st.columns(3)
    layout_params = fund(list(hyp_params.keys()), 3)

    for i in range(len(layout_params)):
        for j in range(len(layout_params[i])):
            with col[j]:
                hyp_params[layout_params[i][j]] = st.number_input(layout_params[i][j], None, None,
                                                                  hyp_params[layout_params[i][j]])

    with st.container():
        q_name = st.text_input("Dialogue Q name", "User")
        a_name = st.text_input("Dialogue A name", "Ella")

        data_type = st.radio("准备测试数据",
                             ('在线测试', '上传测试数据', '选择已有测试数据'), horizontal=True)

        if data_type == "在线测试":
            knowledge = st.text_area('Prompt knowledge',
                                     '''The film opens by panning over a grand house. AUNT MARY (34/F) steps out the front door, carrying a large suitcase. Behind her is ELLA (8/F). Aunt Mary turns and lowers her head to speak with the young girl. Aunt Mary: I'll only be gone for two days. Ella, promise me that you'll be good while I'm away. No messes, no staying up past 8, and no reading any books that you aren't supposed to. Do you understand? Ella: Yes, Aunt Mary. Aunt Mary: Especially not that book. You know the one. Aunt Mary smiles and ruffles Ella's hair affectionately. She turns to pick up her luggage and head toward her car. Aunt Mary and Ella exchange waves before Aunt Mary drives away, leaving Ella alone on the doorstep. Ella's eyes light up and she giggles a bit before racing inside the house, closing the door behind her. \nINT. AUNT MARY’S HOUSE – DAY \nElla is a timid girl who lives with her aunt who has a private library. Her aunt tells her to never read a certain book because it will cause trouble, but she is still attracted to it. \nElla: Thank you for your concern. I will take good care of myself during this period. \nElla's eyes light up and she giggles a bit before racing inside the house, closing the door behind her.''',
                                     height=500)
            message = st.text_input("Prompt Q message", "How do you find the book hidden by your aunt?")
        else:
            test_data = get_test_data(data_type)
            with st.expander("预览测试数据"):
                if not test_data.empty:
                    st.dataframe(test_data)
                else:
                    st.write("没有数据")

    start = st.button("开始测试")
    if start:
        if not re.match(r'^https?:/{2}\w.+$', URL):
            st.error("非法模型地址")
            st.stop()

        if (len(q_name) < 1) or (len(a_name) < 1):
            st.error("请输入QA name")
            st.stop()

        data_source = "{}-{}".format(q_name, a_name)

        with st.spinner("请耐心等待 ..."):
            if data_type == "在线测试":
                if len(knowledge) < 1:
                    st.error("请输入Prompt")
                    st.stop()
                params = hyp_params.copy()
                params["prompt"] = "{}\n{}: {}\n{}: ".format(knowledge.strip("\n"), q_name, message, a_name)
                result = requests.post(URL, data=json.dumps(params))
                st.write(json.loads(result.text)["result"])

            else:
                if test_data.empty:
                    st.warning("请上传测试数据")
                    st.stop()

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

                for index, row in test_data.iterrows():
                    try:
                        params = hyp_params.copy()
                        knowledge = row['knowledge']
                        message = row['message']
                        params["prompt"] = "{}\n{}: {}\n{}: ".format(knowledge.strip("\n").replace(r"\n", "\n"), q_name, message, a_name)
                        result = requests.post(URL, data=json.dumps(params))
                    except requests.exceptions.ConnectionError \
                           or requests.exceptions.ConnectTimeout or \
                           requests.exceptions.SSLError:
                        st.warning("请求丢失数据: {}".format(index))
                        continue
                    st.text(params["prompt"])
                    st.write(json.loads(result.text))
                    tmp = {"conversation_id": row["conversation_id"], "data_source": data_source,
                           "dialog_round": row["dialog_round"], "knowledge": row["knowledge"],
                           "message": row["message"], "response": json.loads(result.text)["result"]}

                    tmp1 = {"references": row["response"],
                            "predictions": json.loads(result.text)["result"]}

                    dialog_history.loc[len(dialog_history)] = tmp
                    compara_data.loc[len(compara_data)] = tmp1
                    my_bar.progress(round(step * (index + 1)))

                if not dialog_history.empty:
                    with st.expander("预览结果数据"):
                        st.dataframe(dialog_history)

                    dialog_history_csv = convert_df(dialog_history)
                    st.download_button('下载结果数据', dialog_history_csv,
                                       file_name="dialogue-{}-{}".format(data_source,
                                                                         datetime.datetime.now().strftime(
                                                                             '%Y-%m-%d_%H-%M-%S')),
                                       mime='text/csv')

                if not compara_data.empty:
                    with st.expander("预览response对比数据"):
                        st.dataframe(compara_data)

                    compara_data_csv = convert_df(compara_data)
                    st.download_button('下载response对比数据', compara_data_csv,
                                       file_name="dialogue_response-{}-{}".format(data_source,
                                                                                  datetime.datetime.now().strftime(
                                                                                      '%Y-%m-%d_%H-%M-%S')),
                                       mime='text/csv')


if __name__ == "__main__":
    app()
