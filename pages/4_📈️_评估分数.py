import streamlit as st
import pandas as pd
from io import StringIO
from tools import get_example

Metric = ["abstractness", "accuracy", "aun", "bartscore",
          "bertscore", "bleu", "cider", "coleman_liau",
          "eed", "flesch_kincaid", "gunning_fog", "mauve",
          "meteor", "nist", "nubia", "perplexity",
          "repetitiveness", "rouge"]


def init_metric(option):
    from nlgmetricverse import NLGMetricverse, load_metric
    metric = []
    for o in option:
        metric.append(load_metric(o))
    scorer = NLGMetricverse(metrics=metric)
    return scorer


def app():
    st.set_page_config(page_title="auto metric", page_icon="📈")
    st.write("# Auto Metric :ghost:")
    data_type = st.radio("准备测试数据",
                         ('在线测试', '上传测试数据'), horizontal=True)

    if data_type == '上传测试数据':
        st.write("参考数据格式: ")
        st.dataframe(pd.read_csv(StringIO(get_example(2)), sep="\t"))
        uploaded_file = st.file_uploader("Choose a file")
        references = []
        predictions = []
        if uploaded_file is not None:
            test_data = pd.read_csv(uploaded_file, sep="\t")
            references = test_data["references"].tolist()
            predictions = test_data["predictions"].tolist()
    else:
        references = st.text_input("样本数据")
        predictions = st.text_input('生成数据')

    option = st.multiselect('选择评价方法', Metric)

    start = st.button("开始评估")

    if start:
        if option:
            if len(references) < 1 or len(predictions) < 1:
                st.warning("请准备好数据")
                st.stop()

            with st.spinner("请耐心等待 ..."):
                if not isinstance(predictions, list):
                    predictions = [predictions]
                if not isinstance(references, list):
                    references = [references]
                scorer = init_metric(option)
                scores = scorer.evaluate(predictions=predictions, references=references)
                st.write(scores)
        else:
            st.write("请选择评价方法")


if __name__ == "__main__":
    app()
