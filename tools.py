import os
import streamlit as st
import pandas as pd
from typing import List
from config import TESTDATA_PATH, EXAMPLE
from io import StringIO


def fund(listTemp, n):
    result = []
    for i in range(0, len(listTemp), n):
        temp = listTemp[i:i + n]
        result.append(temp)
    return result


def get_files(path=TESTDATA_PATH):
    return os.listdir(path)


@st.cache
def get_data(path):
    path = os.path.join(TESTDATA_PATH, path)
    test_data = pd.read_csv(path)
    return test_data


def get_example(id):
    return EXAMPLE[id]


def get_test_data(data_type):
    test_data = pd.DataFrame()
    if data_type == '上传测试数据':
        st.write("参考数据格式: ")
        st.dataframe(pd.read_csv(StringIO(get_example(1)), sep="\t"))
        uploaded_file = st.file_uploader("Choose a file")
        if uploaded_file is not None:
            test_data = pd.read_csv(uploaded_file)
            with st.expander("预览测试数据"):
                st.dataframe(test_data)
    else:
        _test = st.selectbox("选择测试数据", get_files())
        test_data = get_data(_test)

    return test_data


@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False).encode('utf-8')

