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
            if now - os.path.getmtime(file_path) > 24 * 3600:
                os.remove(file_path)

cleanup_old_files()

st.title("📂 24시간 파일 & 텍스트 공유소")
st.write("마! 파일도 올리고 텍스트도 복붙해서 나눌 수 있데이. 24시간 지나면 싹 다 날아간데이.")

# --- 텍스트 공유 부분 ---
st.subheader("📝 텍스트 공유하기")
shared_text = st.text_area("공유할 텍스트 여다가 팍팍 적어라", height=100)
if st.button("텍스트 올리기"):
    if shared_text.strip():
        # 저장할 때 시간 달아서 파일명 안 겹치게 맹근다
        text_filename = f"텍스트메모_{int(time.time())}.txt"
        with open(os.path.join(SAVE_DIR, text_filename), "w", encoding="utf-8") as f:
            f.write(shared_text)
        st.success("텍스트 잘 올라갔데이!")
        time.sleep(0.5)
        st.rerun()
    else:
        st.warning("마! 뭐라도 좀 적고 올리라.")

st.divider()

# --- 파일 업로드 부분 ---
st.subheader("📤 파일 올리기")
uploaded_files = st.file_uploader("파일 여다가 쫌 끌어다 놔라 (여러 개 가능)", accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        with open(os.path.join(SAVE_DIR, uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
    st.success("짜잔! 파일 싹 다 올라갔데이.")
    time.sleep(0.5)
    st.rerun()

st.divider()

# --- 목록 보여주기 및 다운로드 ---
st.subheader("📥 다운로드 및 텍스트 복사")
files = os.listdir(SAVE_DIR)
# 최신 파일이 맨 위로 오구로 정렬
files.sort(key=lambda x: os.path.getmtime(os.path.join(SAVE_DIR, x)), reverse=True)

if files:
    for f in files:
        file_path = os.path.join(SAVE_DIR, f)
        
        # 텍스트 메모는 화면에 바로 보여줘서 복사하기 쉽게 맹근다
        if f.startswith("텍스트메모_") and f.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as text_file:
                content = text_file.read()
            st.write(f"📄 **{f}** (텍스트)")
            # st.code 쓰면 우측 상단에 복사 버튼이 자동으로 생긴데이
            st.code(content, language="text")
        
        # 일반 파일은 다운로드 버튼
        else:
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
    st.info("아직 올라온 기 없네. 빨리 하나 올려보라!")
