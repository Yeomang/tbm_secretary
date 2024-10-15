import streamlit as st
import requests
import json
import time

# 기본 페이지 설정
st.set_page_config(
    page_title="TBM 비서"
)

# 상단에 고정된 제목
st.markdown(
    "<h1 style='text-align: center; font-weight: 600; color: #333;'>🛠️ TBM 비서</h1>",
    unsafe_allow_html=True,
)

# 사내 미르 API 기본 설정
API_KEY = "app-JSc3XRPolsEQ0kxWiIJpNoJc"
BASE_URL = "https://mir-api.gscaltex.co.kr/v1"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# 미르 Workflow 실행 파라미터 입력
query = ""
user_id = "tbmsec_streamlit"
response_mode = "streaming"  # 스트리밍 모드로 고정


# 저장된 작업허가서 설정
saved_permits = ["(#1598983) 203EM-104D OH Fan Motor 부착", "(#1563910) HOU SRU 616C-104C Resin Unloading 및 Cleaning", "(#1565118) 25G-931B Pump SUC' Strainer Cleaning", "(#1675221) 정유4팀 D조 담당구역 Pump Drain 16Point 나사산 가공"]
saved_permits_overview = {
    "(#1598983) 203EM-104D OH Fan Motor 부착": "- 작업제목: 203EM-104D O/H Fan Motor 부착\n- 작업유형 및 종류: 일반 Maintenance / 비방폭 전기기계기구 , 장비 사용 , 차량출입\n- 작업일시: 2024-09-15 08:00 ~ 17:00\n- 지역관계팀: 방향족생산2팀\n- 작업장소: 203 ( 203EM-104D )\n- 작업인원: 4명",
    "(#1563910) HOU SRU 616C-104C Resin Unloading 및 Cleaning": "- 작업제목: HOU SRU 616C-104C Resin Unloading 및 Cleaning\n- 작업유형 및 종류: 일반 Maintenance\n- 작업일시: 2024-08-27 08:00 ~ 17:00\n- 지역관계팀: HOU SRU팀\n- 작업장소: 616 Utility ( 616C-104C )\n- 작업인원: 8명",
    "(#1565118) 25G-931B Pump SUC' Strainer Cleaning": "- 작업제목: 25G-931B Pump SUC' Strainer Cleaning\n- 작업유형 및 종류: 일반 Maintenance / 비방폭 전기기계기구 / Filter/Strainer Cleaning\n- 작업일시: 2024-09-17 10:00 ~ 17:00\n- 지역관계팀: 수처리운영팀\n- 작업장소: 방향족저장탱크 ( 25G-931B )\n- 작업인원: 2명",
    "(#1675221) 정유4팀 D조 담당구역 Pump Drain 16Point 나사산 가공": "- 작업제목: 정유4팀 D조 담당구역 Pump Drain 16Point 나사산 가공\n- 작업유형 및 종류: 일반 Maintenance / 그라인딩, 비방폭 전기기계기구\n- 작업일시: 2024-10-16 08:00 ~ 17:00\n- 지역관계팀: 정유4팀\n- 작업장소: 72UNIT\n- 작업인원: 3명"
}
# 모드별 작업허가서와 sample_code 매핑 딕셔너리
beginner_permit_to_sample = {
    "(#1598983) 203EM-104D OH Fan Motor 부착": "sample2_beginner",
    "(#1563910) HOU SRU 616C-104C Resin Unloading 및 Cleaning": "sample3_beginner",
    "(#1565118) 25G-931B Pump SUC' Strainer Cleaning": "sample4_beginner",
    "(#1675221) 정유4팀 D조 담당구역 Pump Drain 16Point 나사산 가공": "pilot_beginner"
}

advanced_permit_to_sample = {
    "(#1598983) 203EM-104D OH Fan Motor 부착": "sample2_advanced",
    "(#1563910) HOU SRU 616C-104C Resin Unloading 및 Cleaning": "sample3_advanced",
    "(#1565118) 25G-931B Pump SUC' Strainer Cleaning": "sample4_advanced",
    "(#1675221) 정유4팀 D조 담당구역 Pump Drain 16Point 나사산 가공": "pilot_advanced"
}

# 최종 답변 결과 변수 설정
text_output = ""



# 세션 상태 초기화 함수
def reset_session_state():
    st.session_state.pop("selected_mode", None)
    st.session_state.pop("selected_permit", None)
    st.session_state.pop("uploaded_file", None)


# 모드별 제목 스타일 설정
def display_mode_title(title):
    # 배경색과 투명도 설정
    background_color = "rgba(255, 193, 7, 0.15)"  # 연한 노란색 투명
    icon = "🌱"
    if title == "숙련자 모드":
        background_color = "rgba(76, 175, 80, 0.15)"  # 연한 초록색 투명
        icon = "🔥"
    elif title == "연습 모드":
        background_color = "rgba(33, 150, 243, 0.15)"  # 연한 하늘색 투명
        icon = "🎓"

    st.markdown(f"""
        <div style="background-color:{background_color}; padding:15px 20px; border-radius:10px; margin-top:20px;">
            <h2 style="text-align: center; font-weight: 500; color: #333;">{icon} {title}</h2>
        </div>
        """, unsafe_allow_html=True)




# 노드 상태 메시지 업데이트 함수
def process_event(event_data, status, expander):
    global text_output
    try:
        # 스트리밍된 이벤트 데이터를 JSON 형식으로 변환
        event = json.loads(event_data)
        
        # 전체 이벤트 데이터 출력 (모든 이벤트 로그)
        # st.write("Streaming Event Data:", event)  # 전체 이벤트 출력

        # node 관련 이벤트 처리
        if event.get("event") in ["node_started", "node_finished"]:
            node_data = event.get("data", {})
            title = node_data.get("title", "Unknown Title")
            index = node_data.get("index", "N/A")
            start_time = node_data.get("created_at", 0)
            end_time = node_data.get("finished_at", start_time)
            duration = (end_time - start_time)  # 소요 시간 계산 (s)

            # 각 노드 상태 업데이트
            if event["event"] == "node_started":
                status.update(label=f"[Step {index}] **{title}** - 진행 중", state="running")
            elif event["event"] == "node_finished":
                expander.write(f"[Step {index}] **{title}** - 완료 (소요시간: {duration:.1f} s)")
                status.update(
                    label=f"[Step {index}] **{title}** - 완료 (소요시간: {duration:.1f} s)",
                    state="complete"
                )

        # workflow_finished 이벤트에서 outputs의 text를 따로 출력
        if event.get("event") == "workflow_finished":
            data = event.get("data", {})
            outputs = data.get("outputs", {})
            text_output = outputs.get("result", "No text output available")

    except json.JSONDecodeError:
        if "ping" not in event_data:
            st.write("JSON 디코딩 오류 발생:", event_data)





def home():
    option = st.selectbox(
        '🔍 모드 선택',
        index=None,
        placeholder="모드를 선택하세요",
        options=("초심자 모드", "숙련자 모드", "연습 모드"),
        label_visibility="collapsed",
    )

    if st.button("➡️ 다음으로"):
        reset_session_state()  # 모드 이동 전 세션 초기화
        if option: 
            st.session_state["selected_mode"] = option
            st.session_state["page"] = "mode_page"
            st.rerun()
        else: 
            st.warning("⚠️ 모드를 선택해 주세요.")





def mode_page():
    if "selected_mode" in st.session_state:
        selected_mode = st.session_state["selected_mode"]
        display_mode_title(selected_mode)
        st.divider()

        if selected_mode == "초심자 모드":
            area_input = st.container()
            area_status = st.empty()

            action = area_input.radio("📄 작업허가서 옵션을 선택하세요", ("저장된 작업허가서 선택", "새로운 작업허가서 업로드"), label_visibility="collapsed")

            if action == "저장된 작업허가서 선택":
                selected_permit = area_input.selectbox("📑 작업허가서 선택", options=saved_permits, index=None, placeholder="저장된 작업허가서 선택하세요", label_visibility="collapsed")
                
                if selected_permit:
                    # 선택한 작업허가서에 해당하는 개요 정보 출력
                    overview = saved_permits_overview.get(selected_permit, "개요 정보를 찾을 수 없습니다.")
                    area_input.info(f"{overview}")

                    # 선택한 작업허가서에 따라 query(sample code) 지정
                    sample_code = beginner_permit_to_sample.get(selected_permit, "")
                    
                    # Script(대본) 생성 버튼 클릭 시
                    if area_input.button("Script(대본) 생성"):

                        # Workflow 시작 시간을 기록
                        start_time = time.time()

                        # Workflow 실행 요청
                        payload = {
                            "inputs": {
                                "query": query,
                                "choose_sample": sample_code  # 선택한 작업허가서에 해당하는 sample_code를 choose_sample로 전달
                            },
                            "response_mode": response_mode,
                            "user": user_id
                        }
                        response = requests.post(f"{BASE_URL}/workflows/run", headers=HEADERS, data=json.dumps(payload), stream=True)

                        # 모든 노드의 진행 상태를 표시할 단일 expander
                        expander = area_status.expander("전체 진행 상태 보기", expanded=False)
                        with area_status.status("Workflow 실행 중...", expanded=False) as status:
                            # 스트림 데이터 처리
                            if response.status_code == 200:
                                for line in response.iter_lines():
                                    if line:  # 빈 줄 무시
                                        event_data = line.decode("utf-8").replace("data: ", "")
                                        process_event(event_data, status, expander)
                                    time.sleep(0.1)  # 간격 조절 (옵션)
                                
                                # 워크플로우 완료 시간을 기록하고 총 소요 시간을 계산
                                end_time = time.time()
                                total_duration = end_time - start_time
                                status.update(label=f"**Script(대본) 생성 완료!** (총 소요시간: {total_duration:.2f} s)", state="complete", expanded=False)
                            else:
                                st.write("Workflow 실행 요청에 실패했습니다.")
                                st.write(f"상태 코드: {response.status_code}")
                                st.write(f"응답 메시지: {response.text}")

                        # 텍스트 포맷을 유지하며 최하단에 최종 결과 출력
                        st.divider()
                        output = text_output.replace("\n", "<br>")
                        st.markdown(output, unsafe_allow_html=True)
                        
            
            elif action == "새로운 작업허가서 업로드":
                # 새로운 작업허가서를 업로드할 수 있는 파일 업로더
                # uploaded_file = st.file_uploader("📤 새로운 작업허가서를 업로드하세요", type=["pdf", "docx", "xlsx"])
                # 업로드된 파일 처리 (예: 업로드 확인 메시지)
                # if uploaded_file is not None:
                #     st.success(f"✅ {uploaded_file.name}이(가) 성공적으로 업로드되었습니다.")

                # 준비중 안내
                st.error(f"⚠️ 현재 해당 기능은 준비중입니다.")



        elif selected_mode == "숙련자 모드":

            action = st.radio("📄 작업허가서 옵션을 선택하세요", ("저장된 작업허가서 선택", "새로운 작업허가서 업로드"), label_visibility="collapsed")

            if action == "저장된 작업허가서 선택":
                selected_permit = st.selectbox("📑 작업허가서 선택", options=saved_permits, index=None, placeholder="저장된 작업허가서 선택하세요", label_visibility="collapsed")
                
                if selected_permit:
                    overview = saved_permits_overview.get(selected_permit, "개요 정보를 찾을 수 없습니다.")
                    st.info(f"{overview}")
                    
                    # if st.button("Script(대본) 생성"):
                        
            
            elif action == "새로운 작업허가서 업로드":
                # 새로운 작업허가서를 업로드할 수 있는 파일 업로더
                # uploaded_file = st.file_uploader("📤 새로운 작업허가서를 업로드하세요", type=["pdf", "docx", "xlsx"])
                # 업로드된 파일 처리 (예: 업로드 확인 메시지)
                # if uploaded_file is not None:
                #     st.success(f"✅ {uploaded_file.name}이(가) 성공적으로 업로드되었습니다.")

                # 준비중 안내
                st.error(f"⚠️ 현재 해당 기능은 준비중입니다.")





        elif selected_mode == "연습 모드":
            # 연습 모드 관련 내용 추가
            st.error(f"⚠️ 현재 연습 모드 기능은 준비중입니다.")

        st.divider()
        # 처음으로 버튼 추가
        if st.button("처음으로"):
            reset_session_state()  # 처음으로 돌아갈 때 세션 초기화
            st.session_state["page"] = "home"
            st.rerun()




# 페이지 전환 로직
if "page" not in st.session_state:
    st.session_state["page"] = "home"

if st.session_state["page"] == "home":
    home()
elif st.session_state["page"] == "mode_page":
    mode_page()
