import streamlit as st
import os
import time
from zipfile import ZipFile
import io

# 파일 저장할 폴더 맹글기
SAVE_DIR = "shared_files"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

# 24시간 지난 파일 청소하는 기라
def cleanup_old_files():
    now = time.time()
    for f in os.listdir(SAVE_DIR):
        file_path = os.path.join(SAVE_DIR, f)
        if os.path.isfile(file_path):
            # 24시간(86400초) 지나면 싹 다 지운다
            if now - os.path.getmtime(file_path) > 24 * 3600:
                os.remove(file_path)

# 사이트 열릴 때마다 묵은 파일 정리 한번 싹 해주기
cleanup_old_files()

st.title("📂 24시간 파일 공유소")
st.write("마! 시원하게 스트림릿 기본 용량(200MB)까지 팍팍 올릴 수 있데이. 여러 개 한 번에 올리고 받을 수 있고, 24시간 지나면 싹 다 날아간데이.")

# 다중 파일 업로드
uploaded_files = st.file_uploader("파일 여다가 쫌 끌어다 놔라 (여러 개 가능)", accept_multiple_files=True)

# 20MB 제한 빼삐고 바로 저장하는 부분
if uploaded_files:
    for uploaded_file in uploaded_files:
        with open(os.path.join(SAVE_DIR, uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
    st.success("짜잔! 파일 싹 다 올라갔데이.")

st.divider()

# 올라간 파일 목록 보여주고 다운로드
st.subheader("📥 다운로드")
files = os.listdir(SAVE_DIR)

if files:
    # 하나씩 받기
    for f in files:
        file_path = os.path.join(SAVE_DIR, f)
        with open(file_path, "rb") as file_data:
            st.download_button(label=f"⬇️ {f}", data=file_data, file_name=f)
    
    # 여러 개 한방에 압축해서 받기
    if len(files) > 1:
        st.write("---")
        zip_buffer = io.BytesIO()
        with ZipFile(zip_buffer, "w") as zip_file:
            for f in files:
                zip_file.write(os.path.join(SAVE_DIR, f), f)
        
        st.download_button(
            label="📦 파일 싹 다 ZIP으로 묶어서 받기", 
            data=zip_buffer.getvalue(), 
            file_name="shared_files.zip", 
            mime="application/zip",
            type="primary"
        )
else:
    st.info("아직 올라온 파일이 없네. 빨리 하나 올려보라!")
