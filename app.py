from flask import Flask, render_template, redirect, url_for, session, request
import sqlite3

app = Flask(__name__)
app.secret_key = 'pause-test-secret-key' 
DATABASE = 'data.db' 

# --- (신규) DB 초기화 함수 ---
def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS counts (
            type TEXT PRIMARY KEY,
            count INTEGER NOT NULL DEFAULT 0
        )
    ''')
    types = ['ghost', 'dopamine', 'soloplayer', 'humanlatte', 'muscler', 'hotnevi', 'total']
    for t in types:
        c.execute("INSERT OR IGNORE INTO counts (type, count) VALUES (?, 0)", (t,))
    conn.commit()
    conn.close()

result_data = {
    'ghost': {
        'image': 'ghost.jpg', 
        'description': """당신은 ‘완전한 고요함’을 통해 회복하는 사람!\n
사람 사이의 소음, 쏟아지는 메시지로부터\n잠시 멀어져야 나에게 집중할 수 있습니다.\n
이 유형은 고요함의 안정과 내면의 잔잔함을\n가장 소중하게 여깁니다.\n
그래서 종종 ‘잠수했다’는 오해를 받기도 하지만,\n그 시간은 다시 일어설 힘을 얻는\n리셋의 시간입니다.\n
당신에게 쉼은 고요한 방, 조용한 핸드폰,\n그리고 나 자신입니다.\n
아무것도 하지 않아도 괜찮아요.\n그 자체로 이미 충분히 ‘쉬고’ 있으니까요."""
    },
    'dopamine': {
        'image': 'dopamine.jpg',
        'description': """당신은 ‘디지털 콘텐츠’를 통해 회복하는 사람!\n
온라인 세상에서 얻을 수 있는 도파민이\n에너지가 됩니다.\n
유튜브, 넷플릭스, SNS 속에서 수많은 콘텐츠와\n밈을 섭렵하며 모르는 게 없을 정도입니다.\n
이 유형은 도파민 터지는 미디어와 유행을\n가장 소중하게 여깁니다.\n
휴식 시간이 생기면 집에서 밀린 드라마와 영화를\n정주행하며 혼자만의 시간을 즐기곤 합니다.\n
그래도 종종 창밖을 바라보거나 일어나서\n스트레칭하는 시간이 필요합니다."""
    },
    'soloplayer': {
        'image': 'soloplayer.jpg',
        'description': """당신은 ‘나만의 취미’를 통해 회복하는 사람!\n
혼자 있는 시간이 외롭지 않고,\n오히려 가장 만족스러운 순간입니다.\n
이 유형은 손으로 무언가를 만들고,\n나만의 흐름에 몰입할 때 에너지를 얻습니다.\n
책을 읽고, 요리하고, 그림을 그리고, 악기를 연주하며,\n세상과의 연결보다 나만의 창조적인 시간을\n더 소중히 여깁니다.\n
당신에게 쉼은 좋아하는 취미,\n그리고 집중의 순간입니다.\n
나만의 색깔로 채운 시간이\n당신을 회복하게 합니다. 🎨✨"""
    },
    'humanlatte': {
        'image': 'humanlatte.jpg',
        'description': """당신은 ‘따듯한 관계’를 통해 회복하는 사람!\n
혼자 있는 시간도 좋지만,\n당신의 쉼은 사람 사이의 소통에서 옵니다.\n
이 유형은 대단한 활동보다, 서로의 존재만으로\n편안한 순간을 가장 소중히 여깁니다.\n
카페 창가에 앉아 친구와 이야기를 나누고,\n함께하는 웃음과 공감으로 에너지를 얻습니다.\n
당신에게 쉼은 따뜻한 분위기, 편안한 대화,\n그리고 함께 있는 시간입니다.\n
조용하지만 깊은 정서적 유대가\n당신을 회복하게 합니다."""
    },
    'muscler': {
        'image': 'muscler.jpg',
        'description': """당신은 ‘사람과의 에너지 교류’를 통해 회복하는 사람!\n
움직일수록, 웃을수록, 함께할수록\n에너지가 차오릅니다.\n
이 유형은 사람들과 몸으로 부딪치며\n생생한 현장감 속에서 스트레스를 해소합니다.\n
보드게임과 방탈출을 즐기고, 스포츠를 통한\n경쟁과 협동에서 진짜 즐거움을 느낍니다.\n
당신에게 쉼은 함께 웃고 뛰는 시간, 팀워크의 쾌감,\n그리고 지속적인 유대감입니다.\n
사람 사이의 활력은\n당신을 더 강하고 생기 있게 만듭니다. 🔥"""
    },
    'hotnevi': {
        'image': 'hotnevi.jpg',
        'description': """당신은 ‘새로운 경험’을 통해 회복하는 사람!\n
세상의 흥미로운 곳을 찾아 나서는 것이\n곧 당신의 휴식입니다.\n
이 유형은 사람들과 어울리고, 그 순간을\n기록하고 공유하며 에너지를 얻는 타입입니다.\n
요즘 뜨는 맛집, 전시회, 축제, 여행지\n어디든 당신의 발길이 닿습니다.\n
즐거운 순간을 사진과 영상으로 남기며,\n세상과 활발하게 소통합니다.\n
당신에게 쉼은 새로운 장소와 추억,\n함께 웃는 사람들입니다.\n
나만의 장소가 넓혀질수록,\n당신을 더 생기있게 만듭니다. ✨📸"""
    }
}

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
    session['answers'] = {} 
    return render_template('index.html')

@app.route('/question/<int:q_id>')
def question(q_id):
    if q_id < 1 or q_id > len(questions):
        return redirect(url_for('index'))
    current_question = questions[q_id - 1]
    user_answers = session.get('answers', {})
    selected_option_index = user_answers.get(str(q_id))
    
    return render_template('question.html', question=current_question, 
                           current_q_id=q_id, total_questions=len(questions),
                           selected_option_index=selected_option_index)

@app.route('/answer/<int:q_id>/<int:option_index>')
def answer(q_id, option_index):
  try:
      _ = questions[q_id - 1]['options'][option_index]
  except IndexError:
      return redirect(url_for('index'))
  
  if 'answers' in session:
      answers = session['answers'].copy()
      answers[str(q_id)] = option_index 
      session['answers'] = answers
  
  next_q_id = q_id + 1
  if next_q_id > len(questions):
      return redirect(url_for('loading'))
  else:
      return redirect(url_for('question', q_id=next_q_id))

@app.route('/loading')
def loading():
    try:
        return render_template('loading.html')
    except:
        return redirect(url_for('calculate_result'))


@app.route('/calculate_result')
def calculate_result():
    if 'answers' not in session or len(session['answers']) < len(questions):
        return redirect(url_for('index'))
        
    user_answers = session['answers']
    
    final_scores = {'in': 0, 'out': 0, 'static': 0, 'dynamic': 0, 'online': 0, 'offline': 0}
    
    for q_id_str, option_index in user_answers.items():
        q_id = int(q_id_str)
        try:
            tags = questions[q_id - 1]['options'][option_index].get('tags', [])
            for tag in tags:
                if tag in final_scores:
                    final_scores[tag] += 1
        except IndexError:
            continue
    
    scores = final_scores
    
    type_map_by_key = {
        'AAA': 'ghost', 'AAB': 'dopamine', 'ABA': 'soloplayer', 
        'BAA': 'humanlatte', 'BBA': 'muscler', 'BBB': 'hotnevi'
    }

    place_key = 'A' if scores['in'] >= scores['out'] else 'B'
    activity_key = 'A' if scores['static'] >= scores['dynamic'] else 'B'
    digital_key = 'A' if scores['offline'] >= scores['online'] else 'B'
    
    key = place_key + activity_key + digital_key
    final_type_name = type_map_by_key.get(key)
    
    if final_type_name is None:
        dynamic_score = scores['dynamic']
        online_score = scores['online']
        
        if dynamic_score >= online_score:
            digital_key = 'A'
        else:
            digital_key = 'B'
            
        key = place_key + activity_key + digital_key
        final_type_name = type_map_by_key.get(key, 'ghost') 
    
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("UPDATE counts SET count = count + 1 WHERE type = ?", (final_type_name,))
        c.execute("UPDATE counts SET count = count + 1 WHERE type = 'total'")
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"DB Error: {e}") 

    return redirect(url_for('result', type_name=final_type_name))


@app.route('/result/<string:type_name>')
def result(type_name):
    if type_name not in result_data:
        return redirect(url_for('index'))
    
    data = result_data[type_name]
    
    total_count = 1
    type_count = 1
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("SELECT count FROM counts WHERE type = 'total'")
        total_count = c.fetchone()[0]
        c.execute("SELECT count FROM counts WHERE type = ?", (type_name,))
        type_count = c.fetchone()[0]
        conn.close()
    except Exception:
        pass
    
    type_percent = "0.0%"
    if total_count > 0:
         type_percent = f"{(type_count / total_count * 100):.1f}%"
    
    # result.html이 없는 경우를 대비해 임시로 index.html 렌더링
    # (실제로는 Step 3에서 만든 result.html이 있어야 함)
    try:
        return render_template('result.html', 
                            data=data,
                            total_count=total_count,
                            type_percent=type_percent)
    except:
         return f"Result: {type_name}, Description: {data['description']}"

if __name__ == '__main__':
    # init_db() 
    app.run(debug=True)
