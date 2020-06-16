from flask import Flask, request, render_template, redirect, url_for, abort, session

import game
import json

import dbdb

app = Flask(__name__)

app.secret_key = b'aaa!111/'

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/hello/')
def hello():
    return 'Hello, World!'

@app.route('/hello/<name>')
def helloovar(name):
    character = game.set_charact(name)
    return render_template('gamestart.html', data=character)

@app.route('/gamestart')
def gamestart():
    with open("static/save.txt", "r", encoding='utf-8') as f:
        data = f.read()
        character = json.loads(data)
        print(character['items'])
    return ("{} 이 {}아이템을 사용 해서 이겼다.".format(character["name"], character["items"][0]))

@app.route('/input/<int:num>')
def input_num(num):
    if num == 1:
        with open("static/save.txt", "r", encoding='utf-8') as f:
            data = f.read()
            character = json.loads(data)
            print(character['items'])
        return ("{} 이 {}아이템을 사용 해서 이겼다.".format(character["name"], character["items"][0]))    
    elif num == 2:
        return "퉁퉁이에게 패배했다."
    elif num == 3:
        return "도망갔다."
    else:
        return "없어요"

    # return 'Hello, {}!'.format(name)

# 로그인
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        id = request.form['id']
        pw = request.form['pw']
        print (id,type(id))
        print (pw,type(pw))
        # id와 pw가 db 값이랑 비교 해서 맞으면 맞다 틀리면 틀리다
        ret = dbdb.select_user(id, pw)
        print(ret[2])
        if ret !=None:
            session['user'] = id
            return redirect(url_for ('index'))
        else:
            return redirect(url_for ('login'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

# 회원 가입
@app.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'GET':
        return render_template('join.html')
    else:
        id = request.form['id']
        pw = request.form['pw']
        name = request.form['name']
        print (id,type(id))
        print (pw,type(pw))
        ret = dbdb.check_id(id)
        if ret != None:
            return '''
                    <script>
                    alert('다른 아이디를 사용하세요');
                    location.href='/join';
                    </script>
            '''
        # id와 pw가 db 값이랑 비교 해서 맞으면 맞다 틀리면 틀리다
        dbdb.insert_user(id, pw, name)
        return redirect(url_for('login'))

@app.route('/form')
def form():
    return render_template('test.html')

@app.route('/method', methods=['GET', 'POST'])
def method():
    if request.method == 'GET':
        return 'GET 으로 전송이다.'
    else:
        num = request.form['num']
        name = request.form['name']
        print(num, name)
        dbdb.insert_data(num, name)
        return 'POST 이다. 학번은: {} 이름은: {}'.format(num, name)

@app.route('/getinfo')
def getinfo():
    if 'user' in session:
        ret = dbdb.select_all()
        print(ret[4])
        return render_template('getinfo.html', data=ret)
        
    return redirect(url_for('login'))


@app.route('/naver')
def naver():
    return redirect("https:/www.naver.com/")
    # return render_template("naver.html")

@app.route('/kakao')
def daum():
    return redirect("https:/www.daum.net/")

@app.route('/urltest')
def url_test():
    return redirect(url_for("naver"))

@app.route('/move/<site>')
def move_site(site):
    if site == 'naver':
        return redirect(url_for("naver"))
    elif site == 'daum':
        return redirect(url_for("daum"))
    else:
        abort(404)
        # return '없는 페이지 입니다.'

@app.errorhandler(404)
def page_not_found(error):
    return "페이지가 없습니다. URL을 확인 하세요", 404

@app.route('/img')
def img():
    return render_template("image.html")

if __name__ == '__main__':
    with app.test_request_context():
        print(url_for('daum'))
    app.run(debug=True)