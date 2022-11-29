import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# 欢迎加入AIGC Metricverse! 👋")

st.markdown(
    """
这是一个AIGC质量评估平台，集成了各种生成和评估脚本，目的是快速和科学地得到生成算法到测试结果

**👈 Select  the sidebar** to see more examples
### 说明
- 模型评估
  - 评估模型输出结果，需要输入相关prompt得到结果，目前设计prompt是以对话形式
- 对话评估
  - 评估苏格拉底对话结果，需要输入对话内容
- AI相互对话评估
  - 评估苏格拉底两个AI相互聊天结果
***以上结果需要导入标注平台进行人工评估***
- 评估分数
  - 输入参考数据和生成数据得到各种算法指标结果
- 数据导入标注平台
  - 把生成的结果数据导入到label studio标注平台
"""
)
