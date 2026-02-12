import streamlit as st
import cv2
import numpy as np
from PIL import Image
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="SkinSensei", page_icon="🧴")

# ระบบจำลองฐานข้อมูล
if 'history' not in st.session_state:
    st.session_state.history = []

# ฟังก์ชันวาดกราฟ 6 เหลี่ยม
def draw_radar(v):
    cat = ['ความเรียบเนียน', 'ความใส', 'ความชุ่มชื้น', 'ริ้วรอย', 'จุดด่างดำ', 'สุขภาพรวม']
    fig = go.Figure(data=go.Scatterpolar(r=v+[v[0]], theta=cat+[cat[0]], fill='toself'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])))
    return fig

# ส่วนแสดงผล
st.sidebar.title("🧴 SkinSensei Menu")
menu = st.sidebar.radio("เลือกหน้า:", ["วิเคราะห์ผิว", "SkinDiary (ประวัติ)", "คำแนะนำ"])

if menu == "วิเคราะห์ผิว":
    st.title("🧴 วิเคราะห์สุขภาพผิว")
    st.write("อัปโหลดรูปภาพเพื่อเริ่มการวิเคราะห์รอยสิว ริ้วรอย และความกระจ่างใส")
    up = st.file_uploader("เลือกรูปใบหน้า", type=["jpg","png","jpeg"])
    
    if up:
        img = Image.open(up)
        st.image(img, width=300)
        # สุ่มคะแนนจำลอง (เพื่อให้เห็นภาพก่อนในเวอร์ชันแรก)
        scores = [80, 75, 60, 85, 90, 78] 
        st.plotly_chart(draw_radar(scores))
        if st.button("บันทึกประวัติ"):
            st.session_state.history.append({"วันที่": datetime.now().strftime("%d/%m/%Y"), "คะแนน": 78})
            st.success("บันทึกแล้ว!")

elif menu == "SkinDiary (ประวัติ)":
    st.title("📅 ประวัติผิวของคุณ")
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        st.line_chart(df.set_index("วันที่"))
        st.table(df)
    else:
        st.write("ยังไม่มีข้อมูล")

elif menu == "คำแนะนำ":
    st.title("💡 เคล็ดลับดูแลผิว")
    st.info("🍎 ทานวิตามิน C และ Zinc | 😴 นอนให้ครบ 8 ชม. | 🧴 ทากันแดดทุกวัน")