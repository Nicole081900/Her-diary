import streamlit as st
from datetime import date
from PIL import Image
import json
import os
import time

# 页面配置
st.set_page_config(page_title="我的日记", page_icon="📔", layout="centered")

# 背景图片（可换 URL）
bg_url = st.text_input("背景图片 URL（留空使用默认）",
                      value="https://i.imgur.com/abcd1234.png"
                      )

# CSS 背景安全写法
st.markdown(
    f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url('{bg_url}');
        background-size: cover;
        background-attachment: fixed;
    }}
    section[data-testid="stAppViewContainer"] > div {{
        background-color: rgba(255,255,255,0.85);
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📔 我的日记")

# 日期选择
entry_date = st.date_input("日期", value=date.today())

# 照片上传
uploaded_file = st.file_uploader("上传照片（可选）", type=["jpg", "jpeg", "png"])

# 滑杆评分
score = st.slider("心情评分", 0.0, 10.0, 7.0, step=0.5)

# 文本记录
note = st.text_area("今天记录", height=200)

# 保存日记
if st.button("💾 保存日记"):
    os.makedirs("data", exist_ok=True)
    os.makedirs("uploads", exist_ok=True)

    image_path = ""
    if uploaded_file is not None:
        timestamp = int(time.time())
        fname = f"{timestamp}_{uploaded_file.name}"
        save_path = os.path.join("uploads", fname)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        image_path = save_path

    entry = {
        "date": str(entry_date),
        "score": float(score),
        "note": note,
        "image": image_path,
        "saved_at": int(time.time())
    }

    diary_file = os.path.join("data", "diary.json")
    if not os.path.exists(diary_file):
        with open(diary_file, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)

    with open(diary_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    data.append(entry)

    with open(diary_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    st.success("✅ 日记已保存！")
    st.balloons()

st.markdown("---")
st.subheader("最近的日记")

# 显示最近 10 条日记
diary_file = os.path.join("data", "diary.json")
if os.path.exists(diary_file):
    with open(diary_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    for entry in reversed(data[-10:]):
        st.write(f"📅 {entry['date']}    评分：{entry['score']}")
        st.write(entry['note'])
        if entry.get("image"):
            try:
                img = Image.open(entry["image"])
                st.image(img, width=300)
            except Exception:
                st.write("（显示图片失败）")
        st.markdown("---")
else:
    st.info("目前没有日记。")
  for i, entry in enumerate(reversed(data[-10:])):
    st.write(f"📅 {entry['date']}    评分：{entry['score']}")
    st.write(entry['note'])
    if entry.get("image"):
        try:
            img = Image.open(entry["image"])
            st.image(img, width=300)
        except Exception:
            st.write("（显示图片失败）")
    # 删除按钮
    if st.button(f"删除这条日记 {i}"):
        # 删除对应条目
        del data[len(data)-10+i]  # 注意索引调整
        with open(diary_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        st.experimental_rerun()
    st.markdown("---")
