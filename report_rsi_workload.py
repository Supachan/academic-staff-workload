import numpy as np
import pandas as pd
import streamlit as st
import csv
from collections import defaultdict
from numpy.random import default_rng as rng

import matplotlib.pyplot as plt
import matplotlib
import matplotlib.font_manager as fm
from os import path
from matplotlib.pyplot import figure
if 'Sarabun' not in [x.name for x in matplotlib.font_manager.fontManager.ttflist]:
    matplotlib.font_manager.fontManager.addfont('Sarabun-Regular.ttf')
matplotlib.rc('font', family='Sarabun')

from rsi_modules import *


mm3_url         = "https://docs.google.com/spreadsheets/d/1NrR5_OKyydIklO2UPBwHYdqI0Y_x1CaQxrie4OTFaDs/export?format=csv&gid=1475905714"
publication_url = "https://docs.google.com/spreadsheets/d/1NrR5_OKyydIklO2UPBwHYdqI0Y_x1CaQxrie4OTFaDs/export?format=csv&gid=2125519370"
theses_url      = "https://docs.google.com/spreadsheets/d/1NrR5_OKyydIklO2UPBwHYdqI0Y_x1CaQxrie4OTFaDs/export?format=csv&gid=609352385"

F = pd.read_csv(mm3_url)
publication = pd.read_csv(publication_url).fillna("")
theses = pd.read_csv(theses_url).fillna("")





# st.write("ผลงานตีพิมพ์ทางวิชาการในแต่ละปี")
# publication = pd.read_csv(publication_url).fillna("")
# publication,df = get_publication(publication)
# df = df.reset_index().rename(columns={'index':'ปี'})

# st.write(df)

# option = st.selectbox(
#     'เลือกปีที่ต้องการดูผลงานตีพิมพ์ทางวิชาการ',
#      df['ปี'])

# 'You selected: ', df.loc[df['ปี'] == option]

# st.write("ชั่วโมงสอนและจำนวนวิชาที่รับผิดชอบ")
# f = pd.read_csv(mm3_url)
# t1,t2 = report_mm3(f)

# theses = pd.read_csv(theses_url).fillna("" )
new = defaultdict(lambda:defaultdict(list))

for degree_interest in ['ศิลปศาสตร','ศึกษา','ปริญญาเอก']:
    re,rea,ret,rep = get_thesis_workload(theses,degree_interest)
    dd = pd.DataFrame(rep).T.fillna('-')
    dd = dd.reset_index().rename(columns={'index':'ปีการศึกษา'})
    dd = change_degree_name(dd)
    new = collect_cells(new,dd)

new = grouping_programs(new)
A = pd.DataFrame(new).T.fillna('-').reset_index().rename(columns={'index':'ปีการศึกษา'})
A.sort_values(by='ปีการศึกษา', inplace=True)
A = pd.concat([A['ปีการศึกษา'],A['สอบโครงร่างแล้ว'],
               A['อยู่ระหว่างขอ IRB'],A['กำลังเก็บข้อมูล'],
               A['อยู่ระหว่างการวิเคราะห์ข้อมูล'],A['สอบป้องกันวิทยานิพนธ์แล้ว'],
               A['อยู่ระหว่างรอเผยแพร่วิทยานิพนธ์']],axis=1)

# website:
st.title('ภาระงานของคณาจารย์ในสถาบันราชสุดาปีการศึกษา 2568')

st.subheader("1. ชั่วโมงสอนและจำนวนวิชาที่รับผิดชอบ")

academic_year = st.radio(
    "เลือกเทอมและปีการศึกษา",
    ["2568/1", "2568/2"],
)

if academic_year == "2568/1":
    start_date = '8/5/2025'
    end_date   = '9/19/2025'
elif academic_year == "2568/2":
    start_date = '12/12/2025'
    end_date   = '12/30/2025'

f = F[F['Timestamp'].between(start_date, end_date)]
t1,t2 = report_mm3(f)

st.subheader("2. ผลงานตีพิมพ์ทางวิชาการในแต่ละปี")
publication,df = get_publication(publication)
df = df.reset_index().rename(columns={'index':'ปี'})
st.write(df)

st.subheader("3. ภาระงานควบคุมวิทยานิพนธ์")
B = pd.DataFrame(rea).T.fillna(0).astype(int)
B = B.reset_index().rename(columns={'index':'รายชื่อ'})
B['รายชื่อ'] = [b.split('อาจารย์ที่ปรึกษาหลัก /  อาจารย์ที่ปรึกษาร่วม [')[1].replace(']','') for b in B['รายชื่อ']]
B = pd.concat([B['รายชื่อ'],B['Main Advisor'],B['Co advisor']],axis=1)
st.write(B)

st.subheader("4. ภาพรวมความก้าวหน้าวิทยานิพนธ์ของนักศึกษา ")
st.write(A.reset_index(drop=True))
st.write("หมายเหตุ::")
st.write("MA  = หส.ปริญญาโท สาขาคุณภาพชชีวิตคนพิการ")
st.write("MEd = หส.ปริญญาโท สาขาการศึกษาพิเศษ")
st.write("PhD = หส.ปรัชญาดุษฎีบัณฑิต สาขาคุณภาพชีวิตคนพิการ")

pd.DataFrame.to_csv(t1,'teaching_hours.csv',index=False)
pd.DataFrame.to_csv(t2,'teaching_courses_responsibility.csv',index=False)
# def faculty_members():
#     names =  ['นพ.สมเกียรติ ลีละศิธร',
#     'พญ.วัชรา ริ้วไพบูลย์',
#     'ศ.ดร.ทวี  เชื้อสุวรรณทวี',
#     'รศ.ดร.อาดัม นีละไพจิตร',
#     'รศ.ดร.ณัฏฐนียา โตรักษา',
#     'ผศ.ดร.อารี ภาวสุทธิไพศิฐ',
#     'ผศ.ดร.ธีรศักดิ์ ศรีสุรกุล',
#     'ผศ.ดร.เจนจิรา เจนจิตรวาณิช',
#     'ดร.รติรส จันทรสมดี',
#     'ดร.อิศวรา ศิริรุ่งเรือง',
#     'ดร.ธรรม จตุนาม',
#     'ดร.รุจิรา สงขาว',
#     'ดร.ปรเมศวร์ บุญยืน',
#     'ดร.ปกรณ์กิตติ์ ม่วงประสิทธิ์',
#     'ดร.สุนันทา ขลิบทอง',
#     'ดร.วรางคณา รัชตะวรรณ',
#     'ดร.ญาณิศา เนียรนาทตระกูล',
#     'ดร.สุภชาญ ตรัยตรึงศ์สกุล',
#     'ดร.วิษณุ นิตยธรรมกุล',
#     'พฤหัส ศุภจรรยา',
#     'ราษฏร์ บุญญา',
#     'กุลยา ไทรงาม',
#     'ณัฐวิชญ์ ศุภสินธุ์',
#     'พชร นิลมณี',
#     'สิรินทรา ฤทธิเดช',
#     'สร้อยทอง หยกสุริยันต์',
#     'ภัทรานิษฐ สงประชา']
#     return names

# col_name, col_role = st.columns(2)

# with col_name:
#     name = st.selectbox(
#         "คาบที่ 1",
#         faculty_members(),
#         index=None,
#         placeholder="เลือกชื่อผู้สอน/ปฏิบัติ",
#     )
# with col_role:
#     role = st.radio(
#         "บทบาท",
#         options=['ผู้สอนหลัก','ผู้ปฏิบัติ'],
#     )


# st.write(f"You selected: {name} [{role}]")