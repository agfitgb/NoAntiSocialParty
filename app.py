from flask import Flask, render_template, request, jsonify, redirect, url_for
from uuid import uuid4
app = Flask(__name__)

questions = [
    {"id":1, "q":"정부는 복지에 더 많은 예산을 써야 한다.", "w":[1,0]},
    {"id":2, "q":"세금은 부유층에게 더 많이 부과되어야 한다.", "w":[1,0]},
    {"id":3, "q":"시장의 규제는 경제성장을 저해한다.", "w":[-1,0]},
    {"id":4, "q":"민영화는 공공서비스의 질을 높인다.", "w":[-1,0]},
    {"id":5, "q":"노동조합은 노동자의 권리를 보호한다.", "w":[1,0]},
    {"id":6, "q":"기업 규제는 일자리를 감소시킨다.", "w":[-1,0]},
    {"id":7, "q":"이민자는 국가에 긍정적인 영향을 준다.", "w":[1,0]},
    {"id":8, "q":"강력한 국경 통제가 필요하다.", "w":[-1,0]},
    {"id":9, "q":"개인의 자유는 사회적 가치보다 우선한다.", "w":[0,-1]},
    {"id":10, "q":"국가는 도덕적 가치를 강제할 권리가 있다.", "w":[0,1]},
    {"id":11, "q":"사생활 보호는 범죄 예방보다 중요하다.", "w":[0,-1]},
    {"id":12, "q":"법과 질서가 최우선이다.", "w":[0,1]},
    {"id":13, "q":"사형제는 유지되어야 한다.", "w":[0,1]},
    {"id":14, "q":"동성결혼은 허용되어야 한다.", "w":[0,-1]},
    {"id":15, "q":"종교는 공적 영역에서 더 많은 발언권을 가져야 한다.", "w":[0,1]},
    {"id":16, "q":"국방비 지출 증가는 필요하다.", "w":[0,1]},
    {"id":17, "q":"환경 보호는 경제보다 우선시되어야 한다.", "w":[1,0]},
    {"id":18, "q":"정부는 기후변화에 적극 개입해야 한다.", "w":[1,0]},
    {"id":19, "q":"처벌보다는 재활 중심의 사법제도가 바람직하다.", "w":[1,-1]},
    {"id":20, "q":"공공의 안녕을 위해 감시가 정당화될 수 있다.", "w":[0,1]},
    {"id":21, "q":"보건의료는 시장에 맡겨야 한다.", "w":[-1,0]},
    {"id":22, "q":"교육은 국가가 강하게 개입해야 한다.", "w":[1,0]},
    {"id":23, "q":"전통적 성 역할은 중요하다.", "w":[0,1]},
    {"id":24, "q":"마약 범죄에 대한 처벌은 강화되어야 한다.", "w":[0,1]},
    {"id":25, "q":"표현의 자유는 거의 무제한이어야 한다.", "w":[0,-1]},
    {"id":26, "q":"기업의 환경오염은 엄중히 처벌해야 한다.", "w":[1,0]},
    {"id":27, "q":"기본소득은 도입되어야 한다.", "w":[1,0]},
    {"id":28, "q":"군대는 국가의 가장 중요한 기관 중 하나이다.", "w":[0,1]},
    {"id":29, "q":"정부의 역할은 가능한 한 축소되어야 한다.", "w":[-1,0]},
    {"id":30, "q":"시민의 자유를 지키기 위해 국가는 최소한으로 개입해야 한다.", "w":[-1,-1]}
]

# 간단 메모리 세션(테스트용). 배포 시 DB/Redis 권장.
sessions = {}

@app.route('/')
def index():
    return render_template('index.html', total=len(questions))

@app.route('/test')
def test():
    return render_template('test.html', questions=questions, total=len(questions))

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json() or {}
    answers = data.get('answers', [])
    econ = 0
    auth = 0
    for a, q in zip(answers, questions):
        score = (a - 3)  # 1..5 -> -2..+2 (중앙=0)
        econ += q['w'][0] * score
        auth += q['w'][1] * score
    norm_econ = round(econ / len(questions), 3)
    norm_auth = round(auth / len(questions), 3)
    sid = str(uuid4())
    sessions[sid] = {'econ': norm_econ, 'auth': norm_auth, 'raw': answers}
    return jsonify({'id': sid})

@app.route('/result')
def result():
    sid = request.args.get('id')
    if not sid or sid not in sessions:
        return redirect(url_for('index'))
    data = sessions[sid]
    econ = data['econ']
    auth = data['auth']
    x = max(-5, min(5, econ))
    y = max(-5, min(5, auth))
    if x > 0 and y < 0:
        quadrant = '좌파 자유주의자'
        desc = '경제적 평등과 개인의 자유를 중시합니다.'
    elif x > 0 and y > 0:
        quadrant = '좌파 권위주의자'
        desc = '사회적 규범과 정부 개입을 통해 평등을 추구합니다.'
    elif x < 0 and y < 0:
        quadrant = '우파 자유주의자'
        desc = '시장과 개인의 자유를 중시하며 작은 정부를 선호합니다.'
    else:
        quadrant = '우파 권위주의자'
        desc = '안전과 전통적 가치를 중시하며 강한 국가를 선호합니다.'
    return render_template('result.html', quadrant=quadrant, desc=desc, x=x, y=y)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
