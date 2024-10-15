import streamlit as st

# 기본 페이지 설정
st.set_page_config(
    page_title="TBM 비서"
)


# 상단에 고정된 제목
st.markdown(
    "<h1 style='text-align: center; font-weight: 600; color: #333;'>🛠️ TBM 비서</h1>",
    unsafe_allow_html=True,
)

# 세션 상태 초기화 함수
def reset_session_state():
    st.session_state.pop("selected_mode", None)
    st.session_state.pop("script_displayed", None)
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

# Script 출력 함수
def display_script(full_script=True):
    # Full Script와 요약 Script 텍스트만 구분
    script_text = """
    1. 건강상태 및 복장 확인
    2. 작업 사항 및 위험 요인 전달
    3. 안전 조치 및 비상 대처 요령
    """ if not full_script else """
    1. 작업자 건강상태, 복장/개인보호구, 장비/공도구 적절성 여부 확인  
        "금일 자신의 건강상태가 양호한지 확인 바랍니다. 건강상태가 좋지 않다면 즉시 관리자에게 보고해주십시오.  
        작업 복장 착용 확인해주시고, 기본 보호구 외에 특히 귀마개와 안전대를 반드시 착용해주시기 바랍니다.  
        사용 장비와 공도구가 적절한지, 작업 가능 상태인지 점검해주십시오. 고소작업이 포함되어 있으니 안전대 부착설비도 확인 바랍니다."

    2. 작업사항에 대한 전달  
        "방향족생산2팀과 협력하여 203EM-104D에서 O/H Fan Motor 부착 작업을 진행합니다.  
        작업 종류는 일반 Maintenance로, 작업 시간은 08:00부터 17:00까지입니다."

    3. 작업위험성평가 및 핵심 위험요인 전달  
        "고소 작업 중 상부 작업자의 추락 위험이 있습니다. 안전대 착용과 함께 걸고리 체결 및 상태를 확인해주시기 바랍니다."  
        "MOTOR 부착 시 부적합한 공구 사용으로 인한 협착 위험이 있습니다. 규격에 맞는 적정 공구를 사용하고 협착 타격방지를 철저히 해주시기 바랍니다."  
        "차량 출입 시 차량에 충돌하여 상해 및 전도 위험이 있습니다. 차량 후진 시 유도원을 배치하고 개인보호구를 착용하며, 사내 운행 속도를 제한해주시기 바랍니다."

    4. 작업 전 안전조치사항에 대한 공유  
        "작업 전 안전조치를 확인해주세요. 금번 작업은 주전원 차단 LOTO, 작업장 기름 하수구 차폐 및 연소물질 제거, 고소작업 시 안전조치 등을 완료하였습니다.  
        작업 시 주의사항으로는 화기 작업자로부터 5m 이내 소화기 비치, 회사 시설물의 임의 조작 및 사용 금지, 폭염 시 온열질환 예방을 위해 매시간 15분 이상 그늘에서 휴식이 필요합니다.  
        또한, 상하동시 작업이 되지 않도록 하부를 정리하고, 안전대 걸고리는 반드시 안전한 곳에 걸고 작업해 주시기 바랍니다."

    5. 사고사례 내용 공유  
        "앞서 얘기한 핵심 위험요인 중 '협착 위험'과 관련된 사고사례 공유드립니다. 2023년 4월 9일 여수공장에서 발생한 사고로, 정유3팀의 판형열교환기 설치 작업 중 크레인으로 구조물 상부에 있는 설치 위치까지 인양한 후 바닥면의 볼트에 너트를 조립하는 과정에서 열교환기에 있는 볼트 부위와 바닥 고정용 너트 사이에 왼손 검지 손가락이 협착되는 사고가 발생했습니다. 이는 판형열교환기 볼트가 바닥 고정용 볼트 홀 바로 위에 매우 가깝게 붙어 있는 구조로 인해 발생한 사고입니다."  
        "사고 예방을 위해 작업 시 적절한 공구 사용과 작업 환경의 안전성을 철저히 확인해주시기 바랍니다."

    6. 작업자에게 질문 또는 제안사항 청취

    7. 비상상황 대처요령 전달  
    "금일 비상대피 장소는 제1대피장소인 남문과 제2대피장소인 동력팀 C/T 옆입니다. 비상상황 발생 시, 신속하게 해당 대피장소로 이동해주시기 바랍니다. 안전을 위해 대피 경로와 대피장소를 사전에 숙지해주시기 바랍니다."

    8. 지적확인 실시  
        "고소 작업 시 상부 작업자의 추락 위험이 있습니다. 안전대 착용과 걸고리 체결 상태를 확인하여 안전을 확보하겠습니다."  
        (리더 선창 팀원 제창) "지적확인 준비!"  
        "위험의 포인트!"  
        "상부 작업자가 추락하여 다친다."  
        "오늘의 목표!"  
        (리더) "안전대 착용 좋아!"  
        (팀원) "걸고리 체결 상태 철저히 확인 좋아 좋아 좋아!"
   """
        
    
    # 줄바꿈을 위한 <br> 태그 적용
    formatted_text = script_text.replace("\n", "<br>")

    # 스타일 적용
    # st.markdown(f"""
    #     <div style="background-color: #f9f9f9; padding: 10px 20px; border-radius: 10px; margin-top: 20px; margin-bottom: 20px; border: 1px solid #ddd;">
    #         <p style="white-space: pre-wrap; font-size: 16px;">{formatted_text}</p>
    #     </div>
    # """, unsafe_allow_html=True)
    # CSS 스타일 정의
    st.markdown(
        """
        <style>
        .custom-container {
            background-color: #f0f2f6; /* 원하는 배경 색상 */
            padding: 20px;
            border-radius: 8px; /* 모서리 둥글게 */
            border: 2px solid #4CAF50; /* 테두리 색상과 두께 */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # 컨테이너 내부에 텍스트 포함
    formatted_output = "**이 텍스트는 테두리가 있는 컨테이너 내부에 표시됩니다**"

    st.markdown(f"""
        <div class="custom-container">
            {formatted_output}
        </div>
        """, unsafe_allow_html=True)



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
            saved_permits = ["작업허가서 A", "작업허가서 B", "작업허가서 C"]
            saved_permits_overview = {
                "작업허가서 A": "- 작업제목: 203EM-104D O/H Fan Motor 부착\n- 작업일시: 2024-09-15 08:00 ~ 17:00\n- 지역관계팀: 방향족생산2팀",
                "작업허가서 B": "- 작업제목: 장비 점검 및 유지보수\n- 작업일시: 2024-09-16 09:00 ~ 18:00\n- 지역관계팀: 장비관리팀",
                "작업허가서 C": "- 작업제목: 배관 검사 및 청소\n- 작업일시: 2024-09-17 10:00 ~ 15:00\n- 지역관계팀: 배관관리팀",
            }

            action = st.radio("📄 작업허가서 옵션을 선택하세요", ("저장된 작업허가서 선택", "새로운 작업허가서 업로드"), label_visibility="collapsed")

            if action == "저장된 작업허가서 선택":
                selected_permit = st.selectbox("📑 작업허가서 선택", options=saved_permits, index=None, placeholder="저장된 작업허가서 선택하세요", label_visibility="collapsed")
                
                if selected_permit:
                    overview = saved_permits_overview.get(selected_permit, "개요 정보를 찾을 수 없습니다.")
                    st.info(f"{overview}")
                    
                    if st.button("Script(대본) 생성"):
                        st.session_state["script_displayed"] = True
            
            elif action == "새로운 작업허가서 업로드":
                # 새로운 작업허가서를 업로드할 수 있는 파일 업로더
                # uploaded_file = st.file_uploader("📤 새로운 작업허가서를 업로드하세요", type=["pdf", "docx", "xlsx"])

                # 업로드된 파일 처리 (예: 업로드 확인 메시지)
                # if uploaded_file is not None:
                #     st.success(f"✅ {uploaded_file.name}이(가) 성공적으로 업로드되었습니다.")

                # 준비중 안내
                st.error(f"⚠️ 현재 해당 기능은 준비중입니다.")

            if st.session_state.get("script_displayed"):
                display_script(full_script=True)


        elif selected_mode == "숙련자 모드":
            saved_permits = ["작업허가서 A", "작업허가서 B", "작업허가서 C"]
            saved_permits_overview = {
                "작업허가서 A": "- 작업제목: 203EM-104D O/H Fan Motor 부착\n- 작업일시: 2024-09-15 08:00 ~ 17:00\n- 지역관계팀: 방향족생산2팀",
                "작업허가서 B": "- 작업제목: 장비 점검 및 유지보수\n- 작업일시: 2024-09-16 09:00 ~ 18:00\n- 지역관계팀: 장비관리팀",
                "작업허가서 C": "- 작업제목: 배관 검사 및 청소\n- 작업일시: 2024-09-17 10:00 ~ 15:00\n- 지역관계팀: 배관관리팀",
            }

            action = st.radio("📄 작업허가서 옵션을 선택하세요", ("저장된 작업허가서 선택", "새로운 작업허가서 업로드"), label_visibility="collapsed")

            if action == "저장된 작업허가서 선택":
                selected_permit = st.selectbox("📑 작업허가서 선택", options=saved_permits, index=None, placeholder="저장된 작업허가서 선택하세요", label_visibility="collapsed")
                
                if selected_permit:
                    overview = saved_permits_overview.get(selected_permit, "개요 정보를 찾을 수 없습니다.")
                    st.info(f"{overview}")
                    
                    if st.button("Script(대본) 생성"):
                        st.session_state["script_displayed"] = True
            
            elif action == "새로운 작업허가서 업로드":
                # 새로운 작업허가서를 업로드할 수 있는 파일 업로더
                # uploaded_file = st.file_uploader("📤 새로운 작업허가서를 업로드하세요", type=["pdf", "docx", "xlsx"])

                # 업로드된 파일 처리 (예: 업로드 확인 메시지)
                # if uploaded_file is not None:
                #     st.success(f"✅ {uploaded_file.name}이(가) 성공적으로 업로드되었습니다.")

                # 준비중 안내
                st.error(f"⚠️ 현재 해당 기능은 준비중입니다.")

            if st.session_state.get("script_displayed"):
                # 숙련자 모드에서는 요약된 스크립트 출력
                display_script(full_script=False)




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
