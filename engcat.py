import streamlit as st
from openai import OpenAI

client = OpenAI(
    api_key=st.secrets["OPEN_AI_KEY"]
)

st.title(" < 지피티가 떠먹여주는 영어 표현 >")
st.markdown("#### 공부는 지피티가 다 할게...🤖❔영어 표현은 누가 가져갈래 👍🍯")
st.write("")
st.markdown(" 광고 ✖️  데일리 과제 ✖️  프리미엄 구독 ✖️ 인앱 구매 ✖️ 앱다운로드 ✖️ 전문 강사 ✖️ 일타 강사 ✖️" )
st.markdown(" - 수동태인지, 동명사인지, 대명사인지 알고 싶지 않고요...🙅‍♂️")
st.markdown(" - Life is 실전 🌈 내가 실제로 사용할 수 있는 표현만 알고 싶다고요!!🔥 ")
st.markdown("- 🙆‍♂️ 내가 원하는 영어 표현만 언제든 빠르고 간편하게 찾아보자")
st.write("")
st.success("내가 한국어로 매일 사용하고 있는 표현들...어떻게 영어로도 자연스럽게 얘기하지?")
st.success("친구와 대화할 때, MZ세대(=GenZ)인 사촌동생에게 문자 보낼 때, 직장 상사에게 이메일을 보내야 할 때 어떠한 표현이 적절할까?")
st.markdown(" - - - - - - - -")
st.write("")
st.markdown(" ###### 궁금한 표현 & 대상 & 소통 방식을 입력하고 상황별 맞춤 영어 표현 5가지를 배워보세요.  ")
st.markdown(" ###### 모르는 단어를 검색하고 싶을 때는 '단어 검색' 탭으로 이동하세요.  ")
st.write("")

tab_expression, tab_vocab = st.tabs(["영어 표현 검색", "단어 검색"])

with tab_expression: 
    auto_complete = st.toggle(label="예시로 채우기")
    example =  {
        "expression": " 이 디저트 존맛탱이다 ",
        "type" : "대화",
        "partner" : "친구",
    }

    def generate_prompt(expression, partner, type):
        prompt = f"""
    {expression} 표현에 대해 일상 생활 속 활용도가 높은 영어 표현 5가지와 설명을 한국어로 작성해주세요.
    무엇보다 {expression} 표현을 {partner}와 {type}로 소통할 때 사용하려고 한다는 점을 반드시 참고해주세요.
    {type}이 '문자'라면 이모지도 함께 사용해서 작성해주세요.
    각 표현을 나열할 대 앞에 숫자를 붙여서 구분을 해주세요.
    ---
    표현: {expression}
    타입: {type}
    대상: {partner}
    ---
        
        """.strip()
        return prompt


    def request_chat_completion(prompt):
        response = client.chat.completions.create(
            # model = "gpt-4-1106-preview",
            model = "gpt-3.5-turbo",
            messages = [
                {"role": "system", "content": "당신은 미국인이고 한국어와 영어에 능통한 영어 강사입니다."},
                {"role": "user", "content": prompt}
            ],
            stream=True
        )
        return response

    def print_streaming_response(response):
        message = ""
        placeholder = st.empty()
        for chunk in response:
            delta = chunk.choices[0].delta
            if delta.content:
                message += delta.content
                placeholder.markdown(message + "▌")
        placeholder.markdown(message)
        
  

    with st.form("form_1"):
        expression = st.text_input(
                "표현을 입력해주세요",
                value=example["expression"] if auto_complete else "",
                placeholder=example["expression"],
                                )
        
        col1, col2 = st.columns(2)
        with col1:
            types = ['대화','문자', '이메일']
            type = st.selectbox('소통 방식 선택', types)
            value=example["type"] if auto_complete else "",
            placeholder=example["type"]
            
        with col2:
            partners = ['친구','Gen-Z', '애인', '직장 상사']
            partner = st.selectbox('대상 선택', partners)
            value=example["partner"] if auto_complete else "",
            placeholder=example["partner"]
        
        submit = st.form_submit_button("제출하기")
        
        if submit:
            if not expression:
                st.error("표현을 입력해주세요.")
            elif not type:
                st.error("소통 방식을 선택해주세요.")
            elif not partner:
                st.error("대상을 선택해주세요.")
            else:
                prompt = generate_prompt(
                    expression=expression,
                    type=type,
                    partner=partner,
                )
                response = request_chat_completion(prompt)
                print_streaming_response(response)
                

with tab_vocab:        
    st.markdown("표현들 중에 의미를 모르겠거나 알쏭달쏭한 단어가 나왔나요?")
    st.markdown("모르는 단어를 영어 사전이 되어버린 지피티에게 물어보세요")


    auto_complete = st.toggle(label="예시 보기")
    example =  {
        "vocab": "dessert"
    }

    def generate_prompt(vocab):
        prompt = f"""
    {vocab} 단어의 의미와 설명을 작성해주세요.

    ---
    질문: {vocab}
    ---
        
        """.strip()
        return prompt

    def request_chat_completion(prompt):
        response = client.chat.completions.create(
            # model = "gpt-4-1106-preview",
            model = "gpt-3.5-turbo",
            messages = [
                {"role": "system", "content": "당신은 영한, 한영 사전입니다."},
                {"role": "user", "content": prompt}
            ],
            stream=True
        )
        return response

    def print_streaming_response(response):
        message = ""
        placeholder = st.empty()
        for chunk in response:
            delta = chunk.choices[0].delta
            if delta.content:
                message += delta.content
                placeholder.markdown(message + "▌")
        placeholder.markdown(message)
        
    with st.form("form_2"):
        vocab = st.text_input(
                "단어를 입력 후 제출하기를 눌러주세요",
                value=example["vocab"] if auto_complete else "",
                placeholder=example["vocab"],
                                )
        submit = st.form_submit_button("제출하기")
        
        if submit:
            if not vocab:
                st.error("단어를 입력해주세요.")
            else:
                prompt = generate_prompt(
                    vocab=vocab
                )
                response = request_chat_completion(prompt)
                print_streaming_response(response)
        
st.markdown("----")
st.markdown("데이터 분석&서비스 개발 과정 중인 감자🥔의 미니 프로젝트(생성 AI 서비스 개발) 결과물입니다...")