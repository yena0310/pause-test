from flask import Flask, render_template, redirect, url_for, session, request

app = Flask(__name__)
# 세션(session) 기능을 사용하기 위해 시크릿 키가 반드시 필요합니다.
app.secret_key = 'pause-test-secret-key' 

# --- 질문 9개 데이터 ---
# (중요: 6가지 유형 'dopamine', 'ghost', 'hotnevi', 'humanlatte', 'muscler', 'soloplayer'로 type을 맞춰주세요)
questions = [
    { # 1
        'id': 1,
        'text': "드디어 휘몰아치던 일을 끝내고\n휴식 시간이 생겼다...\n뭐하고 쉴까?",
        'options': [
            {'text': "오늘만은 도파민의 노예!😵‍💫\n밀렸던 드라마, 영화, 유튜브를 본다.", 'tags': ['in', 'static', 'online']},
            {'text': "오늘이 날이다.\n만나지 못했던 친구와 당장 만난다.", 'tags': ['out', 'dynamic', 'offline']}
        ]
    },
    { # 2
        'id': 2,
        'text': "슬슬 바람의 온도가 바뀌는 계절,\n옷장에도 새로운 옷이 필요하다!\n당신의 선택은?",
        'options': [
            {'text': "옷은 피부로 먼저 느껴야 하는 법👗\n매장에서 직접 가서 '이거다!' 싶은\n순간의 감을 믿는다.", 'tags': ['out', 'offline']},
            {'text': "장바구니에 후보들을 모아놓고,\n별점과 후기를 분석하며\n최적의 상품을 찾아낸다🧐", 'tags':['in', 'online']}
        ]
    },
    { # 3
        'id': 3,
        'text': "모처럼 아무 약속 없는 주말 오후,\n오늘은 집에 있기로 했다.\n뭘 할까?",
        'options': [
            {'text': "푹신한 침대와 한 몸이 되어,\n스마트폰을 들고 유튜브 알고리즘이\n이끄는 여행을 떠난다.", 'tags': ['static', 'online']},
            {'text': "그동안 미뤄뒀던 요리를 하거나🍳,\n새로 산 레고 조립을 시작하는 등\n손으로 무언가를 만들어본다.", 'tags': ['dynamic', 'offline']}
        ]
    },
    { # 4
        'id': 4,
        'text': "집 가는 길,\n지하철에서 우연히 동창을 봤다...",
        'options': [
            {'text': "눈 마주쳐도 못 본 척…😒\n괜히 피곤해질까 봐 멀리 피한다.", 'tags': ['in', 'static']},
            {'text': '"야 너 여기서 뭐 해!”\n바로 인사하고 근황토크를 시작한다.', 'tags': ['out', 'dynamic']}
        ]
    },
    { # 5
        'id': 5,
        'text': "쉬는 날 아침,\n눈 뜨자마자 하는 일은?",
        'options': [
            {'text': "나 자는 사이에 무슨 일 없었나…?\n핸드폰부터 켜고 세상 돌아가는 걸\n봐야 마음이 놓인다.", 'tags': ['static', 'online']},
            {'text': "창문 열고 햇살 확인!☀️️\n오늘은 나만의 속도로 시작한다.", 'tags': ['dynamic', 'offline']}
        ]
    },
    { # 6
        'id': 6,
        'text': "미래에 대한 고민으로\n요즘 머리가 복잡하다...",
        'options': [
            {'text': "시간이 약이다.💊\n일부러 아무것도 하지 않고\n그냥 흐르게 두면 괜찮아진다.", 'tags': ['static']},
            {'text': "더 생각할수록 머리만 아프다.\n일단 몸을 움직이자!🏃🏻‍♀️", 'tags': ['dynamic', 'offline']}
        ]
    },
    { # 7
        'id': 7,
        'text': "이 휴식 시간의 온도, 습도, 분위기...\n모두 완벽하다!\n지금 이 순간을 어떻게 남겨둘까?",
        'options': [
            {'text': "오늘 일기에 적어놔야지…📝\n이 순간을 즐기며 기억 속에 남겨둔다.", 'tags': ['static']},
            {'text': "바로 사진으로 남겨 인스타그램에 업로드!📸\n친구들에게 공유한다.", 'tags': ['dynamic', 'online']}
        ]
    },
    { # 8
        'id': 8,
        'text': "내일부터 황금 연휴 시작!\n내가 가장 하고 싶은 것은?",
        'options': [
            {'text': "카페에서 미뤄뒀던 책 읽기,\n낮잠 자기, 노래 들으면서 멍때리기.\n나의 조용한 시간을 아무도 방해할 수 없다.", 'tags': ['static']},
            {'text': "이 귀한 시간을 낭비할 수는 없지!✈️\n바로 여행을 떠나거나 산과 바다,\n미뤄뒀던 액티비티를 한다.", 'tags': ['dynamic']}
        ]
    },
    { # 9
        'id': 9,
        'text': "새로운 취미를\n가져보고 싶다는 생각이 들었다.\n어떤 방식으로 배울까?",
        'options': [
            {'text': "온라인 클래스나 유튜브 영상을 보며\n차근차근 시작한다.\n나에게 온전히 집중하는 시간!", 'tags': ['in', 'online']},
            {'text': "오프라인 원데이 클래스나 동호회에 나간다.\n새로운 취미도 가지고,\n새로운 사람들과도 친해지니 일석이조!", 'tags': ['out', 'offline']}
        ]
    }
]


@app.route('/')
def index():
    # --- (수정) Request 3: 'scores' 대신 'answers'를 초기화 ---
    # 사용자가 각 질문(q_id)에 몇 번째(option_index)를 답했는지 저장
    session['answers'] = {} 
    return render_template('index.html')


# <int:q_id>는 URL의 숫자를 q_id라는 정수 변수로 받겠다는 의미
@app.route('/question/<int:q_id>')
def question(q_id):
    if q_id < 1 or q_id > len(questions):
        return redirect(url_for('index'))
    current_question = questions[q_id - 1]
    
    # --- (신규) Request 3: 이전에 선택한 답변이 있다면 템플릿에 전달 ---
    user_answers = session.get('answers', {})
    selected_option_index = user_answers.get(str(q_id)) # q_id를 문자열 키로 사용
    
    # question.html 템플릿에 '질문 데이터'와 '현재 질문 번호'를 전달
    return render_template('question.html', question=current_question, 
                           current_q_id=q_id, total_questions=len(questions))


# --- (수정) Request 3: 답변 저장 로직 변경 ---
@app.route('/answer/<int:q_id>/<int:option_index>')
def answer(q_id, option_index):
  # 1. 유효한 질문/답변인지 확인
  try:
      _ = questions[q_id - 1]['options'][option_index]
  except IndexError:
      return redirect(url_for('index'))
  
  # 2. (수정) 점수를 누적하는 대신, '답변'을 세션에 기록
  if 'answers' in session:
      answers = session['answers'].copy()
      # 키를 문자열로 저장 (JSON 호환)
      answers[str(q_id)] = option_index # 예: {'1': 0, '2': 1, ...}
      session['answers'] = answers
  
  # 3. 다음 질문으로 이동
  next_q_id = q_id + 1
  if next_q_id > len(questions):
      return redirect(url_for('loading'))
  else:
      return redirect(url_for('question', q_id=next_q_id))

# --- (신규) 로딩 페이지 (Step 3에서 추가) ---
@app.route('/loading')
def loading():
    # (주의: loading.html 파일이 templates 폴더에 있어야 함)
    return render_template('loading.html')

# --- (수정) Request 3: 결과 계산 로직 변경 ---
@app.route('/calculate_result')
def calculate_result():
    if 'answers' not in session or len(session['answers']) < len(questions):
        # 모든 질문에 답하지 않았으면 첫 페이지로
        return redirect(url_for('index'))
        
    user_answers = session['answers'] # 예: {'1': 0, '2': 1, ...}
    
    # --- (신규) Request 3: 저장된 답변을 기반으로 최종 점수 계산 ---
    final_scores = {'in': 0, 'out': 0, 'static': 0, 'dynamic': 0, 'online': 0, 'offline': 0}
    
    # 모든 질문(1~9)을 순회
    for q_id_str, option_index in user_answers.items():
        q_id = int(q_id_str)
        # 해당 질문/답변의 태그를 가져옴
        try:
            tags = questions[q_id - 1]['options'][option_index].get('tags', [])
            for tag in tags:
                if tag in final_scores:
                    final_scores[tag] += 1
        except IndexError:
            continue # (혹시 모를 오류 방지)
    
    scores = final_scores # (이름만 변경)

    key_map = { 'in': 'A', 'out': 'B', 'static': 'A', 'dynamic': 'B', 'offline': 'A', 'online': 'B' }

    # (지금은 임시 텍스트 출력)
    return f"최종 점수: {scores}"
    # (최종: return redirect(url_for('result', type_name='soloplayer')))

if __name__ == '__main__':
  app.run(debug=True)