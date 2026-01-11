import streamlit as st
from googleapiclient.discovery import build
import pandas as pd
from collections import Counter

# [1] 화면에 결과를 그려주는 기능을 맨 위로 올렸습니다.
def display_results(titles, tags):
    words = []
    for title in titles:
        # 2글자 이상의 단어만 추출
        words.extend([w for w in title.split() if len(w) > 1])
    
    # 제목에서 나온 단어와 태그를 합쳐서 분석
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

# [2] 메인 프로그램 시작
st.set_page_config(page_title="유튜브 트렌드 발견기", layout="wide")
st.title("🚀 실시간 유튜브 트렌드 발견 & 분석")

api_key = st.sidebar.text_input("YouTube API Key를 입력하세요", type="password")

if api_key:
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        
        # 분석 모드 선택
        mode = st.radio("분석 모드를 선택하세요", ["현재 인기 급상승 전체 분석 (발견형)", "특정 주제 집중 분석 (검색형)"])
        
        if mode == "현재 인기 급상승 전체 분석 (발견형)":
            st.info("현재 대한민국에서 가장 핫한 영상 50개를 분석하여 트렌드 키워드를 뽑습니다.")
            if st.button("전체 트렌드 스캔 시작"):
                # 인기 급상승 차트 데이터 가져오기
                request = youtube.videos().list(
                    part='snippet', chart='mostPopular', regionCode='KR', maxResults=50
                ).execute()
                
                titles = [item['snippet']['title'] for item in request['items']]
                tags = []
                for item in request['items']:
                    if 'tags' in item['snippet']:
                        tags.extend(item['snippet']['tags'])
                
                # 분석 결과 출력 함수 실행
                display_results(titles, tags)

        else: # 검색형 모드
            query = st.text_input("분석하고 싶은 주제를 입력하세요", "상담심리")
            if st.button("주제 분석 시작"):
                search_response = youtube.search().list(
                    q=query, part='snippet', maxResults=50, order='viewCount', type='video', regionCode='KR'
                ).execute()
                
                titles = [item['snippet']['title'] for item in search_response['items']]
                # 검색 결과는 태그 수집이 제한적이므로 제목 위주로 분석
                display_results(titles, [])
                
    except Exception as e:
        st.error(f"에러가 발생했습니다: {e}")
else:
    st.info("왼쪽 사이드바에 API Key를 입력해 주세요.")
```⠀
⠀
---⠀
⠀
### **🛠️ 조치 방법**⠀
⠀
1.  **깃허브 접속:** `youtube-trend-scanner` 저장소의 `app.py` 파일을 클릭합니다.⠀
2.  **수정 모드:** 오른쪽 상단의 **연필 아이콘(Edit this file)**을 누릅니다.⠀
3.  **내용 교체:** 기존 코드를 모두 지우고, 위에서 드린 **새로운 코드를 처음부터 끝까지 복사해서 붙여넣습니다.** (특히 맨 윗부분의 `def display_results`부터 끝까지 다 들어가야 합니다.)⠀
4.  **저장:** 초록색 **[Commit changes...]** 버튼을 눌러 저장합니다.⠀
5.  **확인:** 약 30초 뒤에 선생님의 스트림릿 주소로 접속해 보세요. 자동으로 업데이트되어 있을 것입니다.⠀
⠀
---⠀
⠀
### **결론**⠀
⠀
선생님, 에러는 "여기만 고치면 완벽해!"라고 알려주는 고마운 이정표와 같습니다. 이번 수정을 통해 **'발견형' 모드**가 작동하게 되면, 선생님은 이제 **아무런 검색어를 넣지 않아도 현재 대한민국 유튜브의 실시간 판도**를 한눈에 읽어내실 수 있게 됩니다.⠀
⠀
코드를 수정하신 후, **'전체 트렌드 스캔'**을 눌렀을 때 어떤 키워드들이 1등으로 나왔나요? 데이터가 잘 나오는지 확인해 보시고 말씀해 주세요!⠀
⠀
**혹시 또 다른 에러 메시지가 뜬다면 바로 캡처해서 보여주시겠어요?** 선생님의 디지털 도구가 완벽하게 돌아갈 때까지 제가 끝까지 곁에서 도와드리겠습니다.⠀
⠀
Would you like me to explain **how the 'tags' analysis** helps you find hidden trends that are not visible in video titles?⠀
