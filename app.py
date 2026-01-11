import streamlit as st
from googleapiclient.discovery import build
import pandas as pd
from collections import Counter

# 프로그램 화면 설정
st.set_page_config(page_title="유튜브 트렌드 분석기", layout="wide")
st.title("📊 실시간 유튜브 트렌드 분석기")

# 사이드바에서 비밀번호 형식으로 API 키 입력 받기
api_key = st.sidebar.text_input("YouTube API Key를 입력하세요", type="password")

if api_key:
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        query = st.text_input("분석하고 싶은 주제를 입력하세요 (예: 상담심리, 중학생 고민)", "상담심리")
        
        if st.button("트렌드 분석 시작"):
            # 데이터 수집 (최근 인기 영상 50개)
            search_response = youtube.search().list(
                q=query, part='snippet', maxResults=50, order='viewCount', type='video', regionCode='KR'
            ).execute()
            
            titles = [item['snippet']['title'] for item in search_response['items']]
            
            # 단어 빈도 분석 (2글자 이상 단어만)
            words = []
            for title in titles:
                words.extend([w for w in title.split() if len(w) > 1])
            
            common_words = Counter(words).most_common(15)
            
            # 화면 결과 출력
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("🔥 핵심 키워드 순위")
                st.table(pd.DataFrame(common_words, columns=['키워드', '빈도']))
            with col2:
                st.subheader("📺 분석된 인기 영상 목록")
                for t in titles[:10]:
                    st.write(f"- {t}")
    except Exception as e:
        st.error(f"에러가 발생했습니다: {e}")
else:
    st.info("왼쪽 사이드바에 YouTube API Key를 입력하시면 분석이 시작됩니다.")
