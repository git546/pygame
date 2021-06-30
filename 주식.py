# -*- coding: utf-8 -*-
"""
Created on Fri Jun  4 22:51:10 2021

@author: 오상윤

추가된 기능
-그래프의 제목 표시
-가로축, 세로축 명칭 표시
-범례 표시
*위 항목들의 경우 warn[1]의 주의사항에 따라 오류 발생시 해당 폰트 설치 및 폰트 변경으로 해결 가능
font_list = [font.name for font in fonm.fontManager.ttflist]
for f in font_list:
    print(f"{f}.ttf")
자신의 터미널에 설치된 폰트를 알 수 있는 코드, 폰트 필요시 최하단에 붙여서 사용.

-지정된 종목만 출력하는 대신 코스피에서 매번 새로운 종목 n개를 무작위로 선정하여 보여줌
-추가 정보 요청시 최고가 평균 최저가 평균 지역에 관한 정보를 알려줌.
"""
import pandas as pd
import  pandas_datareader.data  as  web
import  datetime
import  matplotlib.pyplot  as  plt
import random as rd
import numpy as np
import matplotlib as mat

mat.rcParams['font.family'] = 'Hancom Gothic' #warn[1] 해당 폰트가 없으면 한글이 깨질 수 있습니다. 
#날짜 입력하는 칸
#시작하는 날 연 월 일
SY=2021
SM=4
SD=1
#끝나는 날 연 월 일
EY=2021
EM=5
ED=21

start = datetime.datetime(SY,SM,SD)
end = datetime.datetime(EY,EM,ED)

MD = datetime.datetime(EY,EM,1)

M1=SM
M2=EM

#코스피 코스닥 종합 데이터 제작
ksp_code=pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&marketType=stockMkt', header=0)[0]
ksd_code=pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&marketType=kosdaqMkt',header=0)[0]

ksp_code['시장구분']="KS"
ksd_code['시장구분']="KQ"

krxcode=pd.concat([ksp_code,ksd_code])
#이름을 입력 받으면 종목 코드 호출
def get_code(stk_nm):
    targetcode=krxcode.loc[krxcode['회사명']==stk_nm,['종목코드']]
    targetcode= '%06d' %int(targetcode.values)
    
    return targetcode

def get_local(stk_nm):
    targetcode=krxcode.loc[krxcode['회사명']==stk_nm,['지역']]
    targetcode= '%s' %targetcode.values
    return targetcode
#코스피 코스닥 구분
def call_data(stk_1):
    global ksp_code,ksd_code,start,end
    for i in ksp_code['회사명']:
        if i == stk_1:
            stk = web.DataReader(get_code(stk_1)+'.KS', "yahoo", start, end)
    for i in ksd_code['회사명']:
        if i == stk_1:
            stk = web.DataReader(get_code(stk_1)+'.KQ', "yahoo", start, end)
    
    return stk  


s=ksp_code['회사명']
M1=str(M1)
M2=str(M2)

g_data=np.array([['종목/월',M1+'월',M2+'월','평균']])
pyo = pd.DataFrame( g_data, columns= ['','','',''],index=['코스피 번호'])

cnt=0
stk_lst=[]
rank_lst=[]

n=input("몇 개의 종목을 알아보고 싶으싶니까?:")
n=int(n)

while cnt<n:
    chk=0
    rank=rd.randint(0,808)
    for i in rank_lst:
        if i==rank:
            chk+=1
    if chk==0:
        stk_1=s[rank]
        stk=call_data(stk_1)
        plt.plot(stk['Close'])
       
        stk_lst.append(stk_1)
        rank_lst.append(rank)
    
        favr=stk[stk.index<MD]
        favr=format(favr["Volume"].sum()/len(stk["Volume"]),".1f")
    
        savr=stk[stk.index>MD]
        savr=format(savr["Volume"].sum()/len(stk["Volume"]),".1f")
    
        avr=stk["Volume"].sum()
        avr=format(avr/len(stk["Volume"]),".1f")
    
        pyo.loc[rank]=[stk_1,favr,savr,avr]
        cnt+=1

print(pyo)

plt.xticks(rotation='vertical') # x축 수직으로 전환
plt.title('무작위 선정 %d개 종목 가격 변동 그래프(KS)'%n,fontsize = 30,) #제목 설정
plt.xlabel("연-월-일",fontsize = 20) # 축 이름 만들기
plt.ylabel("거래가",fontsize = 20) # 축 이름 만들기
plt.legend(stk_lst,fontsize=15)

plt.show()

while 1==1:
    ask=input("위 종목 중 더 알아보고 싶은 종목이 있다면 이름을 입력해수십시오(X입력시 종료됨): ")
    if ask=='X':
        break
    elif (ask in stk_lst)==True:
        stk_1=ask
        stk=call_data(stk_1)
        print("최고가 평균 = %.1f"%stk["High"].mean())
        print("최저가 평균 = %.1f"%stk["Low"].mean())
        print("지역 : %s"%get_local(stk_1))
        print()
    else:
        print("해당 종목은 선정되지 않았습니다.")