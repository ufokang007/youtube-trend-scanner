import streamlit as st
from googleapiclient.discovery import build
import pandas as pd
from collections import Counter

# 결과를 화면에 그려주는 기능
def display_results(titles, tags):
    words = []
    for title in titles:
        # 2글자 이상의 단어만 추출
        words.extend([w for w in title.split() if len(w) > 1])
    
    # 제목 단어와 태그 합치기
    all_keywords = words + tags
    common_words = Counter(all_keywords).most_common(20)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🔥 지금 이 순간 가장 뜨거운 키워드")
        st.table(pd.DataFrame(common_words, columns=['키워드', '출현 빈도']))
    with col2:
        st.subheader("📺 현재 인기 급상승 Top 10 영상")
        for i, t in enumerate(titles[:10]):
            st.write(f"{i+1}. {t}")

# 메인 프로그램 시작
st.set_page_config(page_title="유튜브 트렌드 발견기", layout="wide")
st.title("🚀 실시간 유튜브 트렌드 발견 & 분석")

api_key = st.sidebar.text_input("YouTube API Key를 입력하세요", type="password")

if api_key:
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        
        mode = st.radio("분석 모드를 선택하세요", ["현재 인기 급상승 전체 분석 (발견형)", "특정 주제 집중 분석 (검색형)"])
        
        if mode == "현재 인기 급상승 전체 분석 (발견형)":
            st.info("현재 대한민국에서 가장 핫한 영상 50개를 분석하여 트렌드 키워드를 뽑습니다.")
            if st.button("전체 트렌드 스캔 시작"):
                request = youtube.videos().list(
                    part='snippet', chart='mostPopular', regionCode='KR', maxResults=50
                ).execute()
                
                titles = [item['snippet']['title'] for item in request['items']]
                tags = []
                for item in request['items']:
                    if 'tags' in item['snippet']:
                        tags.extend(item['snippet']['tags'])
                
                display_results(titles, tags)

        else: # 검색형
            query = st.text_input("분석하고 싶은 주제를 입력하세요", "상담심리")
            if st.button("주제 분석 시작"):
                search_response = youtube.search().list(
                    q=query, part='snippet', maxResults=50, order='viewCount', type='video', regionCode='KR'
                ).execute()
                
                titles = [item['snippet']['title'] for item in search_response['items']]
                display_results(titles, [])
                
    except Exception as e:
        st.error(f"에러가 발생했습니다: {e}")
else:
    st.info("왼쪽 사이드바에 API Key를 입력해 주세요.")
