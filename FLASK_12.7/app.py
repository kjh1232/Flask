from flask import Flask, render_template, request, session, url_for, redirect, flash
import sqlite3 

app = Flask(__name__)


@app.route('/')
def new_user():
    return render_template('user.html')



@app.route('/user_info', methods = ['POST', 'GET'])
def user_info():
    if request.method == 'POST':
        
        id = request.form['id']
        pwd = request.form['pwd']
    
        if len(id) == 0 or len(pwd) == 0:
            return '아이디, 비밀번호를 모두 입력해주세요!' + render_template('user.html')
    
        else:
            con = sqlite3.connect("member.db")
            cursor = con.cursor()
            sql = "select id, pwd from member where id = ?"
            cursor.execute(sql, (id, ))
            rows = cursor.fetchall()
            cursor.close()
            con.close()
            
            for rs in rows:
                print(rs)
                if id == rs[0] and pwd == rs[1]:
                    
                    session['logFlag'] = True
                    session['id'] = id
                
                    return render_template('main.html')
            
                else:
                    return '존재하지 않습니다. 다시 입력해주세요!' + render_template('user.html')       
            
                
    return '존재하지 않습니다. 다시 입력해주세요!' + render_template('user.html')
            


@app.route('/logout')
def logout():
    session.clear()
    return render_template('user.html')





### 게시글 ####

# 게시판
@app.route('/board', methods = ['GET', 'POST'])
def board():
    # 로그인 한 회원만 게시판 들어갈 수 있는 권한이 있다.
    if session.get('id') is None:
        flash("로그인을 하세요.")
        return redirect(url_for('user_info')) 
    
    else:  
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        cur.execute("select * from Board")
        ###############################
        rows = cur.fetchall()
        print("DB:")
        for i in range(len(rows)):
                print(rows[i][1] + ':' + rows[i][2])
        return render_template('board1.html', contents=rows)
    ####### --> rows 변수에 저장된 select값들을 board1.html파일의 contents변수에 매칭한다. (할당한다.)  
    ####### ---> 즉, board1.html의 contents값 = rows 값(select) ########
 
 
 
# 게시글 작성
@app.route('/add', methods = ['GET', 'POST'])
def add():
    
    if session.get('id') is None:
        flash("로그인을 하세요.")
        return redirect(url_for('user_info')) 
    
    else:
        if request.method == 'POST':
            id = session['id']
            # name = request.form['name']
            context = request.form['context']
            
            ### 3주차 추가한 부분 ##
            if len(context) == 0:
                return "내용을 입력해주세요!" + render_template('add.html')
        
            else:
                try:
                
                    with sqlite3.connect("database.db") as con:
                        cursor = con.cursor()
                        cursor.execute(f"INSERT INTO Board (name, context) VALUES ('{id}', '{context}')")
                        con.commit()
                except:
                    con.rollback()
                finally : 
                    con.close()
                    return redirect(url_for('board'))
        else:
            return render_template('add.html')
        
            
 
 
 
 
# 게시글 업데이트
# /update/<uid> -> 해당 uid를 넣어서 주소창 생성 : 해당 uid에 관한 내용의 페이지가 나옴
@app.route("/update/<uid>,<uname>", methods=["GET","POST"])
def update(uid,uname):
    # update(uid) : uid데이터를 서버 측으로 전달
    # post방식으로 넘어가면
    
    if session.get('id') is None:
        flash("로그인을 하세요.")
        return redirect(url_for('user_info')) 
    
    else:
        id = session['id']
        
        if(id==uname):
            if request.method == "POST":
                # name = request.form["name"]
                context = request.form["context"]
                        
                if len(id) == 0 or len(context) == 0:
                    con = sqlite3.connect("database.db")
                    cursor = con.cursor()
                    cursor.execute(f"SELECT * FROM Board WHERE num='{uid}'")
                    row = cursor.fetchall()
                    return "내용을 입력해주세요!" + render_template('update.html',hang=row)
                        
                else:
                    with sqlite3.connect("database.db") as con:
                        cursor = con.cursor()  
                        cursor.execute(f"UPDATE Board SET name='{id}', context='{context}' WHERE num='{uid}' and name='{id}'")
                        con.commit()
                
                    return redirect(url_for('board'))  
                        
            else:
                # 밑에 기존 내용 보여주는 코드
                con = sqlite3.connect("database.db")
                cursor = con.cursor()
                cursor.execute(f"SELECT * FROM Board WHERE num='{uid}'")
                ###########################
                data = cursor.fetchall()
                return render_template("update.html", hang=data)
                ###### --> data 변수에 저장된 select값을 update.html파일의 hang변수에 매칭한다. (할당한다.) #######
                
        else:
            flash("수정권한이 없습니다.")
            return redirect(url_for('board')) 
    


 
 

# 게시글 삭제
@app.route("/delete/<uid>,<uname>")
def delete(uid,uname):
    
    if session.get('id') is None:
        flash("로그인을 하세요.")
        return redirect(url_for('user_info')) 
    
    else:
        id = session['id']
        
        if (id==uname):
        # 들어온 uid 값이랑 name이랑 delete 연산하고 반영
            with sqlite3.connect("database.db") as con:
                
                cursor = con.cursor()
                
                cursor.execute(f"DELETE FROM Board WHERE num='{uid}' and name='{id}' ")
                con.commit()
    
                return redirect(url_for('board'))
            
        else:
            flash("삭제권한이 없습니다.")
            return redirect(url_for('board'))  

    
        



app.secret_key = 'sample_secret_key'




if __name__ == '__main__':
    app.run(debug=True) 

