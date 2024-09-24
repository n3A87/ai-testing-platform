from page.page import Page
import streamlit as st
import pandas as pd
import os
from multiprocessing import Process
import base64
from zhipuai import ZhipuAI

def get_project_root():
    current_file_path = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(current_file_path))
    return project_root

def call_mllm_task(task_name):
    df = pd.read_excel('static/data/pic/mllm_anno.xlsx')
    df['模型答案'] = ''

    for index, row in df.iterrows():
        prefix = 'static/data/pic/'
        image_path = os.path.join(prefix, row['图片'])
        questions = row['问题']

        with open(image_path, 'rb') as img_file:
            img_base = base64.b64encode(img_file.read()).decode('utf-8')
            

        client = ZhipuAI(api_key="kkkkkkkkkkkkkkkkkkk")  # 填写您自己的APIKey
        response = client.chat.completions.create(
            model="glm-4v-plus",  # 填写需要调用的模型名称
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": img_base
                            }
                        },
                        {
                            "type": "text",
                            "text": questions
                        }
                    ]
                }
            ]
        )
        answer = response.choices[0].message.content
        df.loc[index, '模型答案'] = answer
        df['人工评分'] = ''
        df['错误类型'] = ''

    df.to_excel(f'static/mllm/{task_name}.xlsx', index=False)

class MLLM(Page):
    def write(self):
        def on_click():
            task_name = st.session_state['task_name']
            process_mllm = Process(target=call_mllm_task,args=(task_name,))
            process_mllm.start()

        with st.popover("创建多模态测试任务"):
            with st.form(key='mllm_test_task'):
                st.text_input('任务名称',key='task_name')
                st.form_submit_button("提交",on_click=on_click)

        df = pd.read_excel('static/mllm/xy_test_v1.xlsx')
        prefix = 'http://localhost:8501/app/static/data/pic/'
        df['图片'] = df['图片'].apply(lambda x: os.path.join(prefix, x))

        st.data_editor(df,key='mllm_task_table',
                       column_config={
                           "图片": st.column_config.ImageColumn(),
                           '人工评分': st.column_config.SelectboxColumn(
                               options=['完全正确', '基本正确', '完全错误']
                           ),
                           '错误类型': st.column_config.SelectboxColumn(
                               options=['指令错误', '上下文错误', '数字计算错误']
                           ),
                       })

        def save_anno():
            edit_df = st.session_state['mllm_task_table']['edited_rows']
            for index,value in edit_df.items():
                for column,v in value.items():
                    df.loc[index,column] = v

            df.to_excel(f'static/mllm/xy_test_v1.xlsx', index=False)

        def cal_mllm():
            cal_df = df.groupby('人工评分').size().to_frame().T
            # cal_df.columns = ['数量']
            cal_df['总分'] = (cal_df['基本正确'] * 6 + cal_df['完全正确'] * 10)/ (cal_df['基本正确']+cal_df['完全正确'] + cal_df['完全错误'])

            err_df = df.groupby('错误类型', dropna=True).size().to_frame().T
            err_df['上下文错误'] = err_df['上下文错误']/len(df)
            err_df['指令错误'] = err_df['上下文错误']/len(df)
            err_df['数字计算错误'] = err_df['上下文错误']/len(df)

            sence_df = df.groupby(['场景', '人工评分']).size()

            st.write(cal_df)
            st.write(err_df)
            # st.write(sence_df)
            pass

        st.button('记录标注', on_click=save_anno)
        st.button('计算指标', on_click=cal_mllm)


mllm_test = MLLM('mllm_test')