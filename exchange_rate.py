import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib
from io import BytesIO

def get_exchange(currency_code):
    currency_code = 'usd'
    last_page_num = 10
    df = pd.DataFrame()

    for page_no in range(1,last_page_num+1):
        url = f"https://finance.naver.com/marketindex/exchangeDailyQuote.naver?marketindexCd=FX_{currency_code}KRW&page={page_no}"
        dfs = pd.read_html(url, header=1, encoding="cp949")

        if dfs[0].empty:
            if (page_no == 1):
                print(f"통합코드({currency_code})가 잘못 지정되었습니다.")
            else:
                print(f"{page_no}마지막 페이지 입니다.")
            break

        # print(dfs[0])
        df = pd.concat([df, dfs[0]], ignore_index=False)

    return df

currency_name_dict = {'미국달러':'USD', '유럽연합':'EUR', '일본 엔':'JPY'}
currency_name = st.sidebar.selectbox('통화선택',currency_name_dict.keys())
clicked = st.sidebar.button("환율 데이터 가져오기")

if clicked:
    currency_code = currency_name_dict[currency_name]
    df_exchage = get_exchange(currency_code)
    #print(df_exchage)
    st.dataframe(df_exchage)

    df_exchage_rate = df_exchage[['날짜','매매기준율','사실 때','파실 때','보내실 때','받으실 때']]
    df_exchage_rate2 = df_exchage_rate.set_index('날짜')
 
    df_exchage_rate2.index = pd.to_datetime(df_exchage_rate2.index,format='%Y-%m-%d',errors="ignore")

    st.subheader(f"{currency_name} 환율 데이터")
    st.dataframe(df_exchage_rate2.head(20))

    matplotlib.rcParams['font.family']='Malgun Gothic'

    ax = df_exchage_rate2['매매기준율'].plot(figsize=(15,5),grid=True)
    ax.set_title("환율(매매기준율) 그래그", fontsize=20)
    ax.set_xlabel("기간", fontsize=10)
    ax.set_ylabel(f"원화/{currency_name}", fontsize=10)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    fig = ax.get_figure()
    st.pyplot(fig)

    st.text("** 환율 데이터 파일 다운로드 **")
    csv_data = df_exchage_rate.to_csv()

    excel_data = BytesIO()
    df_exchage_rate.to_excel(excel_data)

    col = st.columns(2)
    with col[0]:
        st.download_button("csv 파일 다운로드",csv_data,file_name='exchange_rate_data.csv')
    with col[1]:
        st.download_button("excel 파일 다운로드",csv_data,file_name='exchange_rate_data.xlsx')


