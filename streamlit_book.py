import streamlit as st # type:ignore

# デフォルトのコンテンツ名
DEFAULT_CONTENT_NAME = 'section01'

# コンテンツのタイトルを取得する関数
def get_title(content_name, directory='contents'):
    # ファイルを開く
    with open(f'{directory}/{content_name}.md', 'r') as f:
        # コンテンツをすべて読み出して改行で分割
        content = f.read()
        lines = content.split('\n')
        # タイトルは最初に#がついている行とする。#を除去して返す
        for line in lines:
            if line.startswith('#'):
                return line.replace('#', '').strip()
    return content_name

# コンテンツ一覧を検索する関数
def enum_contents(directory='contents'):
    # pathで指定したディレクトリ内の*.mdファイルを検索
    import glob
    files = glob.glob(f'{directory}/*.md')
    # ファイル名から拡張子を除去
    tmp = [file.replace('.md', '') for file in files]
    # ファイル名からディレクトリ名を除去。これをコンテンツ名とする
    tmp = [file.replace(f'{directory}/', '') for file in tmp]
    tmp = [file.replace(f'{directory}\\', '') for file in tmp]
    # コンテンツ名を昇順でソートする
    tmp.sort()
    # コンテンツ名とコンテンツのタイトルのタプルを作成
    contents = [(content, get_title(content, directory)) for content in tmp]
    return contents

# URLパラメータを更新
def update_params(content_name):
    st.experimental_set_query_params(page=content_name)
    st.session_state['content_name'] = content_name

# セレクトボックスのイベントハンドラ
def selectbox_changed():
    # セレクトボックスで選ばれた値がst.session_state.titleにセットされる
    # titleからcontent_nameを取得
    content_name = [content[0] for content in contents if content[1] == st.session_state.title][0]
    # URLパラメータを更新
    update_params(content_name)

# コンテンツを表示する関数
def show_content(content_name):
    # URLパラメータを設定
    st.experimental_set_query_params(page=content_name)
    # コンテンツをcontentsディレクトリから読み込んで表示
    with open(f"contents/{content_name}.md", "r") as f:
        st.markdown(f.read())
    # imagesディレクトリに{content_name}.csvがあればそこにリストされている画像を表示
    import os
    if os.path.exists(f"images/{content_name}.csv"):
        # 画像のファイル名を取得
        with open(f"images/{content_name}.csv", "r") as f:
            images = f.read().split('\n')
        # 画像を表示
        image_count = 1
        for image in images:
            # 空行は無視
            if image == '':
                continue
            # ファイルが存在する場合のみ表示
            if os.path.exists(f"images/{image}"):
                st.divider()
                st.subheader(f'Figure {image_count}')
                st.image(f"images/{image}")
                image_count += 1

# コンテンツ一覧を取得
contents = enum_contents()

# コンテンツ一覧をサイドバーに表示
st.sidebar.title('Contents')
for content_name, title in contents:
    if st.sidebar.button(title):
        # URLパラメータを更新
        update_params(content_name)

# URLパラメータを取得
params = st.experimental_get_query_params()
page = st.session_state['content_name'] if 'content_name' in st.session_state else DEFAULT_CONTENT_NAME

# セレクトボックスの初期値(index)を取得
index = [content[0] for content in contents].index(page)
# コンテンツ一覧をセレクトボックスで表示
title_list = [content[1] for content in contents]
selected_content = st.selectbox(
    "コンテンツ一覧", title_list, index=index, key='title', on_change=selectbox_changed
)

# コンテンツを表示
show_content(page)
