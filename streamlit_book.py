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

# コンテンツ一覧を取得
contents = enum_contents()

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

# コンテンツ一覧を表示
is_initial = True
st.sidebar.title('Contents')
for content_name, title in contents:
    if st.sidebar.button(title):
        # コンテンツを表示
        show_content(content_name)
        is_initial = False

# URLパラメータを取得
params = st.experimental_get_query_params()
# URLパラメータからpageの値を取得
page = params['page'][0] if 'page' in params else DEFAULT_CONTENT_NAME

# コンテンツを表示
if is_initial:
    show_content(page)
