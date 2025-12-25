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

def main_inside(aca_year,semester):
    mm3_url         = "https://docs.google.com/spreadsheets/d/1NrR5_OKyydIklO2UPBwHYdqI0Y_x1CaQxrie4OTFaDs/export?format=csv&gid=1475905714"
    publication_url = "https://docs.google.com/spreadsheets/d/1NrR5_OKyydIklO2UPBwHYdqI0Y_x1CaQxrie4OTFaDs/export?format=csv&gid=2125519370"
    theses_url      = "https://docs.google.com/spreadsheets/d/1NrR5_OKyydIklO2UPBwHYdqI0Y_x1CaQxrie4OTFaDs/export?format=csv&gid=609352385"

    F = pd.read_csv(mm3_url)
    publication = pd.read_csv(publication_url).fillna("")
    theses = pd.read_csv(theses_url).fillna("")
    theses = theses.drop_duplicates(subset=['รหัส (นักศึกษา)'], keep='last')

    # website:
    # st.title('ภาระงานของคณาจารย์ในสถาบันราชสุดาปีการศึกษา 2568')

    # st.subheader("1. ชั่วโมงสอนและจำนวนวิชาที่รับผิดชอบ")

    # academic_year = st.radio(
    #     "เลือกเทอมและปีการศึกษา",
    #     ["2568/1", "2568/2"], index=1)

    # if academic_year == "2568/1":
    #     aca_year = 'ปีการศึกษา (เทอม) [2568]'
    #     semester   = 'เทอม 1'
    # elif academic_year == "2568/2":
    #     aca_year = 'ปีการศึกษา (เทอม) [2568]'
    #     semester   = 'เทอม 2'

    f = F[F[aca_year]==semester]
    f = f.drop_duplicates(subset=['รหัสวิชา'], keep='last')
    t1,t2 = report_mm3(f)

    st.subheader("2. ผลงานตีพิมพ์ทางวิชาการในแต่ละปี")
    publication,df = get_publication(publication)
    df = df.reset_index().rename(columns={'index':'ปี'})
    st.write(df)

    st.subheader("3. ภาระงานควบคุมวิทยานิพนธ์")
    B = pd.DataFrame(get_thesis_workload_new(theses)).T
    st.write(B)

    st.subheader("4. ภาพรวมความก้าวหน้าวิทยานิพนธ์ของนักศึกษา")
    N = get_thesis_progression_summary(theses)
    A = pd.concat(N, axis=1)
    st.write(A)
    st.write("หมายเหตุ:")
    st.write("MA  = หส.ปริญญาโท สาขาคุณภาพชชีวิตคนพิการ")
    st.write("MEd = หส.ปริญญาโท สาขาการศึกษาพิเศษ")
    st.write("PhD = หส.ปรัชญาดุษฎีบัณฑิต สาขาคุณภาพชีวิตคนพิการ")


    # pd.DataFrame.to_csv(t1,'teaching_hours.csv',index=False)
    # pd.DataFrame.to_csv(t2,'teaching_courses_responsibility.csv',index=False)

def main():
    # solution: https://discuss.streamlit.io/t/there-is-a-way-to-make-my-webapp-continuously-active/27556
    blabla=True
    loop = 1
    from datetime import date

    today = date.today()
    
    # print("Today's date:", today)
    while blabla == True:
        if loop == 1:
            st.title('ภาระงานของคณาจารย์ในสถาบันราชสุดาปีการศึกษา 2568')
            st.write("ข้อมูลได้อัพเดทเมื่อวันที่:", today.strftime("%d/%m/%Y"))
            st.subheader("1. ชั่วโมงสอนและจำนวนวิชาที่รับผิดชอบ")

            academic_year = st.radio(
                "เลือกเทอมและปีการศึกษา",
                ["2568/1", "2568/2"], index=1)

            if academic_year == "2568/1":
                aca_year = 'ปีการศึกษา (เทอม) [2568]'
                semester   = 'เทอม 1'
            elif academic_year == "2568/2":
                aca_year = 'ปีการศึกษา (เทอม) [2568]'
                semester   = 'เทอม 2'
            # while blabla == True:
            main_inside(aca_year,semester)
        else:
            i+=1
            pass

if __name__ == "__main__":
    main()