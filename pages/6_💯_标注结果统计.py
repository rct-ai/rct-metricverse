import pandas as pd
import numpy as np
import streamlit as st
from tools import convert_df
import datetime

def app():
    st.set_page_config(page_title="test score", page_icon="💯")
    st.write("# 标注结果统计 :books:")

    uploaded_file = st.file_uploader("Choose a file")
    source = None
    if uploaded_file is not None:
        source = pd.read_csv(uploaded_file)
        with st.expander("预览上传数据"):
            st.dataframe(source)

        st.title("结果展示")
        li = ['sensibleness', 'specificity', 'Interestingness', 'groundedness', 'helpfulness', 'role consistency']
        data = []
        for l in li:
            data.append(source.groupby(l)[l].count() / len(source))

        data = pd.DataFrame(data)
        data = data.reset_index()
        data = data.rename(columns={"index": "metric"})

        st.dataframe(data, use_container_width=True)
        st.bar_chart(data, x='metric', y=['优秀', '很差', '一般',
                                         '不涉及'])

        download = convert_df(data)
        st.download_button('下载分析结果数据', download,
                           file_name="分析结果-{}.csv".format(datetime.datetime.now().strftime(
                               '%Y-%m-%d_%H-%M-%S')),
                           mime='text/csv')



if __name__ == "__main__":
    app()
