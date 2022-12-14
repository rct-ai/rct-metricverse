import json

import pandas as pd
import requests
import streamlit as st
import re
import datetime
from config import headers
from tools import get_test_data, convert_df


def app():
    st.set_page_config(page_title="dialogue metric", page_icon="ð¨âð©âð§âð¦")

    st.write("# Dialogue Metric :kissing_heart:")
    st.markdown('''
    ***ç¸å³åæ°è¯´æ***
    - AI NAME: èæäººåå­
    ''')
    st.write("## å¯¹è¯åæ°éç½® ")
    URL = {}
    accessKey = {}
    accessToken = {}
    ai_name = {}
    params = {}
    ai_nums = 2
    for i in range(ai_nums):
        st.write("### å¯¹è¯AI-{}åæ°éç½® ".format(i))
        URL[i] = st.text_input("å¯¹è¯è¯·æ±å°å-{}".format(i), "https://socrates-api.rct.ai/v1/applications/222/nodes/ed19e08c-8223-4982-b0e1-071635e1847a/conversation")
        accessKey[i] = st.text_input("accessKey-{}".format(i), 'ab2f2d27-0705-4268-b5ac-b954746504cd')
        accessToken[i] = st.text_input("accessToken-{}".format(i), '6d0139d3-b7f1-427d-95eb-86354ce467d6')
        ai_name[i] = st.text_input("AI NAME-{}".format(i), "bot")
        params[i] = {"accessKey": accessKey[i],
                     "accessToken": accessToken[i]}

    st.write("### åæ°éç½® ")
    first_message = st.text_input("å¯åä¿¡æ¯ï¼ç¬¬ä¸ä¸ªAIä¸»å¨ååºçæ¶æ¯ï¼", "Hi!")
    dialog_num = int(st.number_input("å¯¹è¯æ¬¡æ°", 1, step=1))
    dialog_round = int(st.number_input("æ¯æ¬¡å¯¹è¯è½®æ°", 1, step=1))

    start = st.button("å¼å§æµè¯")
    if start:
        for i in range(ai_nums):
            if (not re.match(r'^https?:/{2}\w.+$', URL[i])) or (len(accessKey[i]) < 2) or (len(accessToken[i]) < 2):
                st.error("éæ³åæ°")
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

            with st.spinner("è¯·èå¿ç­å¾ ..."):
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

                            st.warning("è¯·æ±ä¸¢å¤±æ°æ®: {}".format(i))
                            continue

                        for i in range(ai_nums):
                            dialog_history[i].loc[len(dialog_history[i])] = tmp[i]

                    my_bar.progress(round(step))
                    step += step

            for i in range(ai_nums):
                dialog_history_csv = {}
                if not dialog_history[i].empty:
                    with st.expander("é¢è§AI {}ç»ææ°æ®".format(i)):
                        st.dataframe(dialog_history[i])

                    dialog_history_csv[i] = convert_df(dialog_history[i])
                    st.download_button('ä¸è½½AI {}ç»ææ°æ®'.format(i), dialog_history_csv[i],
                                       file_name="dialogue-{}-{}.csv".format(ai_name[i], datetime.datetime.now().strftime(
                                           '%Y-%m-%d_%H-%M-%S')),
                                       mime='text/csv')


if __name__ == "__main__":
    app()
