import streamlit as st
from page.page import Page
from page.mllm_task import mllm_test
from page.test import rag_test


class MultiApp:
    def __init__(self):
        self.apps = []
        self.extra_apps = []
        self.buttons_status = []

    def add_xiaoguo_app(self,title,page):
        self.apps.append({
            "title":title,
            "page":page,
        })

    def add_extra_app(self,page):
        self.extra_apps.append({
            "page":page
        })

    def run(self):
        def change_route():
            app = st.session_state['app_key']
            app['page'].refresh_route()

        route = st.query_params.get('page')
        default_page = 0
        if route:
            for a in self.apps:
                pa: Page = a['page']
                print(pa.get_route())
                if route == pa.get_route():
                    default_page = self.apps.index(a)

        st.sidebar.title("任务导航")
        with st.sidebar.expander("效果测试管理", expanded=True):
            app = st.radio(
                '',
                self.apps,
                format_func=lambda app: app['title'],
                on_change=change_route,
                key="app_key",
                index=default_page,
            )
        url = 'http://localhost:8501/'
        st.markdown(f'<a href="{url}" target="_self">{"返回首页"}</a>', unsafe_allow_html=True)
        if route:
            for a in self.apps:
                pa: Page = a['page']
                if route == pa.get_route():
                    pa.write()
            for a in self.extra_apps:
                pa: Page = a['page']
                if route == pa.get_route():
                    pa.write()
        else:
            app['page'].refresh_route()
            app['page'].write()

st.set_page_config(page_title='人工智能模型评测平台',layout='wide')
app = MultiApp()
# 开始注册效果测试侧边栏
app.add_xiaoguo_app("多模态", mllm_test)
# app.add_extra_app(doc_split_detail)
app.run()