import streamlit as st
from label_studio_sdk import Client
import re
import pandas as pd
from io import StringIO
from tools import get_example

LABEL_STUDIO_URL = 'http://192.168.0.181:9000/'
API_KEY = '508e5d4c79c5fbe0ccd69cdd629e543cc933e7b4'


def app():
    st.set_page_config(page_title="dialogue metric", page_icon="🤖️")

    st.write("# 数据导入标注平台 :books:")
    st.markdown('''
    ***相关说明***
    - 导入label studio，需要获取相关帐号的API_KEY
    - 项目ID可以从URL上获取，如`http://192.168.0.181:9000/projects/87/data?tab=278&page=1`，项目ID为87
    - label studio项目可以参考，demon的数据标注测试模版
    ''')
    URL = st.text_input("LABEL_STUDIO_URL", LABEL_STUDIO_URL)
    api_key = st.text_input("API_KEY", API_KEY)
    project_id = st.number_input("项目ID", 87, step=1)

    st.write("参考数据格式: ")
    st.dataframe(pd.read_csv(StringIO(get_example(1)), sep="\t"))
    uploaded_file = st.file_uploader("Choose a file")
    test_data = None
    if uploaded_file is not None:
        test_data = pd.read_csv(uploaded_file)
        with st.expander("预览上传数据"):
            st.dataframe(test_data)

    start = st.button("开始导入")
    if start:
        if (not re.match(r'^https?:/{2}\w.+$', URL)) or (len(api_key) < 2) or (test_data is None):
            st.error("非法参数")
            st.stop()

        with st.spinner("请耐心等待 ..."):
            ls = Client(url=URL, api_key=api_key)
            project = ls.get_project(int(project_id))
            import_data = test_data.to_dict(orient="records")
            data = []
            for i in import_data:
                data.append({"data": i})
            project.import_tasks(data)
            st.success("导入项目成功")


if __name__ == "__main__":
    app()
