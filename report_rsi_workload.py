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


def summarize_course_units(f):
    units = pd.concat([     f["จำนวน หน่วยกิต (ทฤษฎี-ปฏิบัติ-เรียนรู้ด้วยตนเอง) [หน่วยกิต]"],
                                    f["จำนวน หน่วยกิต (ทฤษฎี-ปฏิบัติ-เรียนรู้ด้วยตนเอง) [ทฤษฎี]"],
                                    f["จำนวน หน่วยกิต (ทฤษฎี-ปฏิบัติ-เรียนรู้ด้วยตนเอง) [ปฏิบัติ]"],
                                    f["จำนวน หน่วยกิต (ทฤษฎี-ปฏิบัติ-เรียนรู้ด้วยตนเอง) [เรียนรู้ด้วยตนเอง]"]],axis=1).rename(columns={   'จำนวน หน่วยกิต (ทฤษฎี-ปฏิบัติ-เรียนรู้ด้วยตนเอง) [หน่วยกิต]':'หน่วยกิต',
                                                                                                                                                                                'จำนวน หน่วยกิต (ทฤษฎี-ปฏิบัติ-เรียนรู้ด้วยตนเอง) [ทฤษฎี]':'ทฤษฎี',
                                                                                                                                                                                'จำนวน หน่วยกิต (ทฤษฎี-ปฏิบัติ-เรียนรู้ด้วยตนเอง) [ปฏิบัติ]':'ปฏิบัติ',
                                                                                                                                                                                'จำนวน หน่วยกิต (ทฤษฎี-ปฏิบัติ-เรียนรู้ด้วยตนเอง) [เรียนรู้ด้วยตนเอง]':'เรียนรู้ด้วยตนเอง'})
    units = pd.concat([f['ชื่อวิชา'],f['รหัสวิชา'],f['อาจารย์ผู้รับผิดชอบรายวิชา'],units],axis=1)
    return units

def rename_columns(fd):
    kv = {}
    for i,ki in enumerate(fd.keys()):
        if i == 0: kv[ki] = 'items'
        else:       kv[ki] = 'data'
    return kv

def extract_non_empty_cells(f,ci):
    # transpose row2col
    fd = pd.DataFrame(f.loc[f["รหัสวิชา"]==ci].T.reset_index())
    kv = rename_columns(fd)
    fd = fd.rename(columns=kv)
    fd = fd.loc[fd["data"].notna()].reset_index(drop=True)
    return pd.DataFrame(fd)

def calculate_lect_hr_per_course(lec):
    for kk in lec.keys():
        print('-----'*10)
        print(kk,'เวลาบรรยายทั้งหมด',sum([ti for _,ti in lec[kk].items()]))
        print('-----'*10)
        for li,ti in lec[kk].items():
            print('\t',li,ti)

def add_labels(y):
    for i in range(len(y)):
        plt.text(y[i], i, y[i], va='center')

def get_sorted_name():
    import io
    import pandas as pd
    temp = pd.read_csv(io.StringIO('''
    นพ.สมเกียรติ ลีละศิธร,0
    พญ.วัชรา ริ้วไพบูลย์,5
    ศ.ดร.ทวี  เชื้อสุวรรณทวี,41.83
    รศ.ดร.อาดัม นีละไพจิตร,38
    รศ.ดร.ณัฏฐนียา โตรักษา,67
    ผศ.ดร.อารี ภาวสุทธิไพศิฐ,84
    ผศ.ดร.ธีรศักดิ์ ศรีสุรกุล,57
    ผศ.ดร.เจนจิรา เจนจิตรวาณิช,77
    ดร.รติรส จันทรสมดี,33.83
    ดร.อิศวรา ศิริรุ่งเรือง,44
    ดร.ธรรม จตุนาม,67.5
    ดร.รุจิรา สงขาว,53
    ดร.ปรเมศวร์ บุญยืน,3
    ดร.ปกรณ์กิตติ์ ม่วงประสิทธิ์,22.5
    ดร.สุนันทา ขลิบทอง,52
    ดร.วรางคณา รัชตะวรรณ,69.33
    ดร.ญาณิศา เนียรนาทตระกูล,12
    ดร.สุภชาญ ตรัยตรึงศ์สกุล,32
    ดร.วิษณุ นิตยธรรมกุล,23
    พฤหัส ศุภจรรยา,78
    ราษฏร์ บุญญา,28
    กุลยา ไทรงาม,57
    ณัฐวิชญ์ ศุภสินธุ์,57
    พชร นิลมณี,25
    สิรินทรา ฤทธิเดช,200
    สร้อยทอง หยกสุริยันต์,28
    ภัทรานิษฐ สงประชา,12
    อาจารย์พิเศษ (ภายนอกม.มหิดล),15
    อาจารย์พิเศษ (ภายนอกคณะแพทย์ฯรามา ม.มหิดล),3
    '''), header=None)

    temp=temp.rename(columns={0:'name',1:'hr'})
    return temp['name'].to_list()

def get_worksheet(worksheet,tab_number):
    data_ws = worksheet.get_worksheet(tab_number)
    #get_all_values gives a list of rows
    rows = data_ws.get_all_values()
    #Convert to a DataFrame
    df = pd.DataFrame(rows)
    new_header = df.iloc[0] #grab the first row for the header
    df =df[1:] #take the data less the header row
    df.columns = new_header #set the header row as the df header
    return df

def special_hr_705(lec,ci):
    lec[ci]['อาจารย์พิเศษ (ภายนอกม.มหิดล)']+=1
    lec[ci]['ศ.ดร.ทวี  เชื้อสุวรรณทวี'] = int(lec[ci]['ศ.ดร.ทวี  เชื้อสุวรรณทวี'])
    lec[ci]['ดร.วรางคณา รัชตะวรรณ'] = int(lec[ci]['ดร.วรางคณา รัชตะวรรณ'])
    lec[ci]['ดร.รติรส จันทรสมดี']    = int(lec[ci]['ดร.รติรส จันทรสมดี'])
    return lec

def collect_programs(lec):
    c = defaultdict(list)
    for l in lec.keys():
        if 'รมคพ'   in l: c['รมคพ'].append(l)
        elif 'รมกพ' in l: c['รมกพ'].append(l)
        elif 'รมหศ' in l: c['รมหศ'].append(l)
        elif 'รมศท' in l: c['รมศท'].append(l)
        elif 'รมศษ' in l: c['รมศษ'].append(l)
    return c


def complie_mm3(units,lec):
    owner_courses = defaultdict(list)
    num_owner_courses = defaultdict(int)
    name_other_courses = defaultdict(int)

    for name,code in zip(units['อาจารย์ผู้รับผิดชอบรายวิชา'],units['รหัสวิชา']):
        owner_courses[name]+=[code.strip()]
        num_owner_courses[name]+=1


    for (code, names) in lec.items():
        for name in names.keys():
            if code.strip() not in owner_courses[name]:
                name_other_courses[name]+=1
    return owner_courses, num_owner_courses, name_other_courses

def courses(f):
    cols  = f.keys()
    data = defaultdict(lambda:defaultdict(list))
    lec   = defaultdict(lambda:defaultdict(float))
    # ดึงทีละวิชา
    for p,ci in enumerate(f["รหัสวิชา"]):
        # print(f'---------{ci.strip()}-----------')
        # if ci.strip() in [
        #                     # 'รมศษ ๑๐๒',  # หายไป 2 ชั่วโมง (มีสอบกลางภาค-ปลายภาค)
        #                     # 'รมศษ ๓๓๑',  # จะต้องส่ง มม3 ให้พี่สาวกรอกใหม่ # หายไป 2 ชั่วโมง (มีสอบกลางภาค-ปลายภาค) และอัพเดทโจ๊ก
        #                     # 'รมศษ ๑๗๐',  # หายไป 1 ชั่วโมง
        #                     ]:
            fdi = extract_non_empty_cells(f,ci)
            # ดึงชั่วโมงบรรยาย
            hr_lecture = int(fdi[fdi['items']=="จำนวน หน่วยกิต (ทฤษฎี-ปฏิบัติ-เรียนรู้ด้วยตนเอง) [ทฤษฎี]"]['data'].to_numpy()[0])
            # ดึงผู้สอนหลัก
            fdii = fdi.loc[(fdi['data'] == 'ผู้สอนหลัก') | (fdi['data'] == 'ผู้สอนหลัก, ผู้ปฏิบัติ')].reset_index(drop=True)
            for i in range(1,17):
                J = [j for j in fdii['items'] if f'(คาบที่ {i})' in j]
                if len(J) > 0:
                    data[i][ci] = hr_lecture/len(J)
                    for jj in J:
                        lec[ci][jj.split('[')[1].split(']')[0]]+=hr_lecture/len(J)
                else:
                    data[i][ci] = 0
            # fdi.replace(r'^\s*$', np.nan, regex=True, inplace=True)
            # fdi.dropna(how='any').to_csv(f'วิชา {ci.strip()}.csv')

            if 'รมคพ 705' in ci: lec = special_hr_705(lec,ci)

    # calculate_lect_hr_per_course(lec)

    # collect_programs(lec)
    return lec

def plot_teaching_hours(temp):
    fig = figure(figsize=(6,10))
    names = temp['name'].to_list()
    hrs = temp['hr']
    plt.barh(names, hrs)
    for i,xval in enumerate(hrs):
        if xval > 0:
            plt.text(xval, i, f'{int(xval)}', ha='left', va='center')
    plt.title("# teaching hours")
    plt.xlabel("Hours")
    plt.gca().invert_yaxis()
    # plt.show()
    st.pyplot(plt.gcf())

def plot_teaching_courses(temp1):
    fig = figure(figsize=(6,10))
    names = temp1['name'].to_list()
    no1 = temp1['จำนวนวิชาที่รับผิดชอบ']

    plt.barh(names, no1)
    for i,xval in enumerate(no1):
        if xval < 0:
            plt.text(xval, i, f'{abs(xval):.0f}', ha='right', va='center')
    # add_labels(no1)
    no2 = temp1['จำนวนวิชาที่สอน'].astype('int64')
    plt.barh(names, no2)
    for i,xval in enumerate(no2):
        if xval > 0:
            plt.text(xval, i, f'{abs(xval):.0f}', ha='left', va='center')
    plt.title("Number of Courses [สีน้ำเงิน = วิชาที่รับผิดชอบ / สีส้ม = วิชาที่สอน]")
    # plt.xlabel("Number of Courses")
    plt.gca().invert_yaxis()
    # plt.show()
    st.pyplot(plt.gcf())

def report_mm3(f):

    units = summarize_course_units(f)
    lec = courses(f)
    owner_courses, num_owner_courses, name_other_courses = complie_mm3(units,lec)

    lec = pd.DataFrame(lec).fillna(0).sum(axis=1).reset_index().rename(columns={'index':'name',0:'hr'})

    sorted_name = {}
    sorted_name['นพ.สมเกียรติ ลีละศิธร'] = 0
    for b in get_sorted_name():
        for n,h in zip(lec['name'],lec['hr']):
            if n in b: sorted_name[b] = h

    temp = pd.DataFrame([sorted_name]).T.reset_index().rename(columns={'index':'name',0:'hr'})


    temp1 = pd.DataFrame([num_owner_courses,name_other_courses]).T.fillna(0)
    lec1  = temp1.reset_index().rename(columns={'index':'name',0:"จำนวนวิชาที่รับผิดชอบ", 1:"จำนวนวิชาที่สอน"})

    sorted_name = defaultdict(list)
    sorted_name['นพ.สมเกียรติ ลีละศิธร'] = [0,0]
    for b in get_sorted_name():
        for n,h1,h2 in zip(lec1['name'],lec1['จำนวนวิชาที่รับผิดชอบ'],lec1['จำนวนวิชาที่สอน']):
            if n in b: sorted_name[b.strip()] = [-h1,h2]

    temp1 = pd.DataFrame(sorted_name).T.reset_index().rename(columns={'index':'name',0:"จำนวนวิชาที่รับผิดชอบ", 1:"จำนวนวิชาที่สอน"})
    plot_teaching_hours(temp)

    plot_teaching_courses(temp1)
    return temp, temp1

def get_publication(publication):
    # publication = get_worksheet(worksheet,3)

    Year = publication.columns[3]
    TCI = publication.columns[4]
    Qs  = publication.columns[5]
    IntConf  = publication.columns[6]
    NatConf = publication.columns[7]
    Role = publication.columns[7]

    lecturers = [n.split('    ')[1] for n in get_sorted_name()[:-2]]

    rec_year = defaultdict(lambda:defaultdict(int))
    for i,a in enumerate(publication[Year]):
        if len(publication[TCI].iloc[i]) > 0:
            rec_year[a][publication[TCI].iloc[i]]+=1
        elif len(publication[Qs].iloc[i]) > 0:
            rec_year[a][publication[Qs].iloc[i]]+=1
        elif len(publication[IntConf].iloc[i]) > 0:
            rec_year[a][publication[IntConf].iloc[i]]+=1
        elif len(publication[NatConf].iloc[i]) > 0:
            rec_year[a][publication[IntConf].iloc[i]]+=1

    df = pd.DataFrame(rec_year).T.fillna(0).astype(int)

    # Get current column names and sort them
    sorted_column_names = sorted(df.columns)

    # Reindex the DataFrame with the sorted column names
    df_sorted = df[sorted_column_names].sort_index()
    ax = df_sorted.plot(kind='bar', stacked=True, figsize=(8, 6), colormap='viridis')
    fig = ax.get_figure()
    st.pyplot(fig)
    return publication,df_sorted

def get_adv_coadv_list():
    Advisor_CoAdvisor_list =  ['อาจารย์ที่ปรึกษาหลัก /  อาจารย์ที่ปรึกษาร่วม [นพ.สมเกียรติ ลีละศิธร]',
    'อาจารย์ที่ปรึกษาหลัก /  อาจารย์ที่ปรึกษาร่วม [พญ.วัชรา ริ้วไพบูลย์]',
    'อาจารย์ที่ปรึกษาหลัก /  อาจารย์ที่ปรึกษาร่วม [ศ.ดร.ทวี  เชื้อสุวรรณทวี]',
    'อาจารย์ที่ปรึกษาหลัก /  อาจารย์ที่ปรึกษาร่วม [รศ.ดร.อาดัม นีละไพจิตร]',
    'อาจารย์ที่ปรึกษาหลัก /  อาจารย์ที่ปรึกษาร่วม [รศ.ดร.ณัฏฐนียา โตรักษา]',
    'อาจารย์ที่ปรึกษาหลัก /  อาจารย์ที่ปรึกษาร่วม [ผศ.ดร.อารี ภาวสุทธิไพศิฐ]',
    'อาจารย์ที่ปรึกษาหลัก /  อาจารย์ที่ปรึกษาร่วม [ผศ.ดร.ธีรศักดิ์ ศรีสุรกุล]',
    'อาจารย์ที่ปรึกษาหลัก /  อาจารย์ที่ปรึกษาร่วม [ผศ.ดร.เจนจิรา เจนจิตรวาณิช]',
    'อาจารย์ที่ปรึกษาหลัก /  อาจารย์ที่ปรึกษาร่วม [ดร.รติรส จันทรสมดี]',
    'อาจารย์ที่ปรึกษาหลัก /  อาจารย์ที่ปรึกษาร่วม [ดร.อิศวรา ศิริรุ่งเรือง]',
    'อาจารย์ที่ปรึกษาหลัก /  อาจารย์ที่ปรึกษาร่วม [ดร.ธรรม จตุนาม]',
    'อาจารย์ที่ปรึกษาหลัก /  อาจารย์ที่ปรึกษาร่วม [ดร.รุจิรา สงขาว]',
    'อาจารย์ที่ปรึกษาหลัก /  อาจารย์ที่ปรึกษาร่วม [ดร.ปรเมศวร์ บุญยืน]',
    'อาจารย์ที่ปรึกษาหลัก /  อาจารย์ที่ปรึกษาร่วม [ดร.ปกรณ์กิตติ์ ม่วงประสิทธิ์]',
    'อาจารย์ที่ปรึกษาหลัก /  อาจารย์ที่ปรึกษาร่วม [ดร.สุนันทา ขลิบทอง]',
    'อาจารย์ที่ปรึกษาหลัก /  อาจารย์ที่ปรึกษาร่วม [ดร.วรางคณา รัชตะวรรณ]',
    'อาจารย์ที่ปรึกษาหลัก /  อาจารย์ที่ปรึกษาร่วม [ดร.ญาณิศา เนียรนาทตระกูล]',
    'อาจารย์ที่ปรึกษาหลัก /  อาจารย์ที่ปรึกษาร่วม [พฤหัส ศุภจรรยา]',
    'อาจารย์ที่ปรึกษาหลัก /  อาจารย์ที่ปรึกษาร่วม [ราษฏร์ บุญญา]',
    'อาจารย์ที่ปรึกษาหลัก /  อาจารย์ที่ปรึกษาร่วม [กุลยา ไทรงาม]',
    'อาจารย์ที่ปรึกษาหลัก /  อาจารย์ที่ปรึกษาร่วม [ณัฐวิชญ์ ศุภสินธุ์]',
    'อาจารย์ที่ปรึกษาหลัก /  อาจารย์ที่ปรึกษาร่วม [พชร นิลมณี]',
    'อาจารย์ที่ปรึกษาหลัก /  อาจารย์ที่ปรึกษาร่วม [สิรินทรา ฤทธิเดช]',
    'อาจารย์ที่ปรึกษาหลัก /  อาจารย์ที่ปรึกษาร่วม [ดร.สุภชาญ ตรัยตรึงศ์สกุล]',
    'อาจารย์ที่ปรึกษาหลัก /  อาจารย์ที่ปรึกษาร่วม [ดร.วิษณุ นิตยธรรมกุล]',
    'อาจารย์ที่ปรึกษาหลัก /  อาจารย์ที่ปรึกษาร่วม [สร้อยทอง หยกสุริยันต์]',
    'อาจารย์ที่ปรึกษาหลัก /  อาจารย์ที่ปรึกษาร่วม [ภัทรานิษฐ สงประชา]']
    return Advisor_CoAdvisor_list

def get_thesis_workload(worksheet,degree_interest):
    # theses = get_worksheet(worksheet,4)
    theses = worksheet
    Advisor_CoAdvisor_list = get_adv_coadv_list()

    ID = [i.split(' ')[0] for i in theses['รหัส (นักศึกษา)']]

    Title    = theses['ชื่อหัวข้อวิทยานิพนธ์']
    Status   = theses["""สถานะของความก้าวหน้าวิทยานิพนธ์
(ลำดับไล่จาก สอบโครงร่างแล้ว ไปถึง อยู่ระหว่างรอเผยแพร่ตีพิมพ์)
หมายเหตุ 
1. "อยู่ระหว่างขอ IRB" ให้ตีความครอบคลุมถึง "กำลังร่าง IRB" / "กำลังแก้ไข IRB" 
2. "กำลังเก็บข้อมูล" ให้ตีความครอบคลุมถึง "ได้ขอ IRB ผ่านแล้ว จึงดำเนินการเก็บข้อมูลได้" แต่ยังเก็บไม่เสร็จ
3. "อยู่ระหว่างการวิเคราะห์ข้อมูล" รวมถึงกระบวนการ "การอภิปรายผล และ/หรือสรุปผล"
4. ลำดับ "อยู่ระหว่างรอเผยแพร่การตีพิมพ์" และ "สอบป้องกันวิทยานิพนธ์แล้ว" ให้เลือกสถานการณ์ปัจจุบัน เนื่องจาก จะมีการบันทึกข้อมูลไว้ในระบบ เช่น สอบป้องกันแล้วรอผลตีพิมพ์ (เลือก-->รอตีพิมพ์) หรือ ยังไม่สอบป้องกัน แต่รอตีพิมพ์ (--> เลือกรอตีพิมพ์) ก็เลือกสิ่งที่เป็นปัจจุบัน"""]
    DegProg  = theses['หลักสูตร']

    rea = defaultdict(lambda:defaultdict(int))
    for n in Advisor_CoAdvisor_list:
        for a in theses[n]:
            if len(a) > 0:
                rea[n][a]+=1

    for n in Advisor_CoAdvisor_list:
        for a in theses[n]:
            if len(a) > 0:
                rea[n][a]+=1
    phd,ma,me = 0,0,0
    Enr_Yr = [Enrolled_Year[:2] for Enrolled_Year in ID]
    re = defaultdict(lambda:defaultdict(int))
    rep= defaultdict(lambda:defaultdict(list))
    ret= defaultdict(lambda:defaultdict(list))
    for i,(e,s,t,d) in enumerate(zip(Enr_Yr,Status,Title,DegProg)):
        if degree_interest in d:
            re[e][s]+=1
            ret[e][s].append(t)
            rep[e][s].append(d)

        if 'ปริญญาเอก' in d:
            phd +=1
        elif 'คุณภาพชีวิต' in d:
            ma +=1
        else:
            me +=1
    print(f'#advisees in MA_QoL={ma}, MEd={me}, PhD_QoL={phd}')
    return re,rea,ret,rep

def report_MainAd_CoAd(rea):
    df = pd.DataFrame(rea).T.fillna(0).astype(int)

    # Get current column names and sort them
    sorted_column_names = sorted(df.columns)

    # Reindex the DataFrame with the sorted column names
    df_sorted = df[sorted_column_names].sort_index()
    return df_sorted

def change_degree_name(dd):
    for ddi in dd.columns:
        C = []
        for cell in dd[ddi]:
            if len(cell) > 0 and cell != '-': 
                for i,ci in enumerate(cell):
                    if "ปริญญาโท-ศิลปศาสตรมหาบัณฑิต" in ci:
                        cell[i] = "MA"
                    elif "ปริญญาโท-ศึกษาศาสตรมหาบัณฑิต" in ci:
                        cell[i] = "MEd"
                    elif "ปริญญาเอก-ปรัชญาดุษฎีบัณฑิต" in ci:
                        cell[i] = "PhD"
            C.append(cell)
        dd[ddi] = C
    return dd

def collect_cells(new,dd):
    for y in dd['ปีการศึกษา']:
        for ddi in dd.columns[1:]:

            for i,cell in enumerate(dd.loc[dd['ปีการศึกษา']==y][ddi]):
                if len(cell) > 0 and cell != '-':
                    for ci in cell:
                        new[y][ddi].append(ci)
    return new

def sub_collect(dv):
    g = defaultdict(int)
    for n in dv:
        g[n]+=1

    return ', '.join([f'{gk}[{gv}]' for gk,gv in g.items()])

def grouping_programs(new):
    for y,data in new.items():
        
        for dk,dv in data.items():
            new[y][dk]=sub_collect(dv)
    return new

# if __name__ == "__main__":
#     import streamlit as st
#     mm3_url         = "https://docs.google.com/spreadsheets/d/1NrR5_OKyydIklO2UPBwHYdqI0Y_x1CaQxrie4OTFaDs/export?format=csv&gid=1475905714"
#     publication_url = "https://docs.google.com/spreadsheets/d/1NrR5_OKyydIklO2UPBwHYdqI0Y_x1CaQxrie4OTFaDs/export?format=csv&gid=2125519370"
#     theses_url      = "https://docs.google.com/spreadsheets/d/1NrR5_OKyydIklO2UPBwHYdqI0Y_x1CaQxrie4OTFaDs/export?format=csv&gid=609352385"
#     publication = pd.read_csv(publication_url).fillna("")
#     publication,df = get_publication(publication)
#     st.write(df)

mm3_url         = "https://docs.google.com/spreadsheets/d/1NrR5_OKyydIklO2UPBwHYdqI0Y_x1CaQxrie4OTFaDs/export?format=csv&gid=1475905714"
publication_url = "https://docs.google.com/spreadsheets/d/1NrR5_OKyydIklO2UPBwHYdqI0Y_x1CaQxrie4OTFaDs/export?format=csv&gid=2125519370"
theses_url      = "https://docs.google.com/spreadsheets/d/1NrR5_OKyydIklO2UPBwHYdqI0Y_x1CaQxrie4OTFaDs/export?format=csv&gid=609352385"

f = pd.read_csv(mm3_url)
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

# theses = pd.read_csv(theses_url).fillna("")
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
st.title('ภาระงานของคณาจารย์ในสถาบันราชสุดาปีการศึกษา 2568 (เทอม1)')

st.subheader("1. ชั่วโมงสอนและจำนวนวิชาที่รับผิดชอบ")
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

st.subheader("4. ภาพรวมความก้าวหน้าวิทยานิพนธ์ของนักศึกษา")
st.write(A.reset_index(drop=True))
st.write("หมายเหตุ::")
st.write("MA  = หส.ปริญญาโท สาขาคุณภาพชชีวิตคนพิการ")
st.write("MEd = หส.ปริญญาโท สาขาการศึกษาพิเศษ")
st.write("PhD = หส.ปรัชญาดุษฎีบัณฑิต สาขาคุณภาพชีวิตคนพิการ")