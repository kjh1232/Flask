from flask import Flask, render_template, request, session, url_for, redirect, flash
import pymysql.cursors

app = Flask(__name__)

DATABASE = {
    'host' : 'localhost',
    'user' : 'root',
    'password' : '123456',
    'db' : 'DATA',
    'charset' : 'utf8',
    #'cursorclass' : pymysql.cursors.DictCursor
}


@app.route('/')
def new_user():
    return render_template('user.html')


# 로그인
@app.route('/user_info', methods = ['POST', 'GET'])
def user_info():
    if request.method == 'POST':
        
        id = request.form['id']
        pwd = request.form['pwd']
        
        connection = pymysql.connect(**DATABASE)
    
        if len(id) == 0 or len(pwd) == 0:
            return '아이디, 비밀번호를 모두 입력해주세요!' + render_template('user.html')
    
        else:
            cursor = connection.cursor()
            sql = "select id, pwd from member where id = %s"
            cursor.execute(sql, (id, ))
            rows = cursor.fetchall()
            cursor.close()
            connection.close()
            
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
    connection = pymysql.connect(**DATABASE)
    # 로그인 한 회원만 게시판 들어갈 수 있는 권한이 있다.
    if session.get('id') is None:
        flash("로그인을 하세요.")
        return redirect(url_for('user_info')) 
    
    else:  
        cur = connection.cursor()
        cur.execute("select name,context,title from my_table")
        
        rows = cur.fetchall()
        #print(rows)
        print("DB:")
        for i in range(len(rows)):
                print(rows[i][0] +':'+ rows[i][2])
        return render_template('board1.html', contents=rows)

 
 
# 게시글 상세확인
@app.route('/post', methods=['GET','POST'])
def post():

    connection = pymysql.connect(**DATABASE)
    
    cursor = connection.cursor()
    cursor.execute("select name,context,title from my_table")
    data = cursor.fetchall()
        
    return render_template('post.html', hang=data)

     

# 게시판 버튼
@app.route('/list')
def list():
    return redirect(url_for('board'))
        
     
 
 
# 게시글 작성
@app.route('/add', methods = ['GET', 'POST'])
def add():
    
    if session.get('id') is None:
        flash("로그인을 하세요.")
        return redirect(url_for('user_info')) 
    
    else:
        if request.method == 'POST':
            id = session['id']
            context = request.form['context']
            title = request.form['title']
            
            
            ### 3주차 추가한 부분 ##
            if len(context) == 0:
                return "내용을 입력해주세요!" + render_template('add.html')
        
            else:
                
                connection = pymysql.connect(**DATABASE)
                try:
                
                    with connection.cursor() as cur:
                        sql = "INSERT INTO my_table (name,context,title) VALUES (%s, %s, %s)"
                        cur.execute(sql, (id,context,title))
                        connection.commit()
                except:
                    connection.rollback()
                finally : 
                    connection.close()
                    return redirect(url_for('board'))
        else:
            return render_template('add.html')
        
            
 
 
 
 
# 게시글 업데이트
@app.route("/update/<uname>,<ucontext>", methods=["GET","POST"])
def update(uname,ucontext):

    
    if session.get('id') is None:
        flash("로그인을 하세요.")
        return redirect(url_for('user_info')) 
    
    else:
        id = session['id']
        
        
        connection = pymysql.connect(**DATABASE)
        
        if(id==uname):
            if request.method == "POST":
                # name = request.form["name"]
                context = request.form["context"]
                title = request.form["title"]
                
                
                        
                if len(id) == 0 or len(context) == 0:
                    with connection.cursor() as cur:
                        sql = "SELECT * FROM my_table WHERE name= %s"
                        cur.execute(sql,(id))
                        row = cur.fetchall()
                        
                    return "내용을 입력해주세요!" + render_template('update.html',hang=row)
                        
                else:
                    with connection.cursor() as cur:
                        
                        sql = "UPDATE my_table SET name=%s, context=%s, title=%s WHERE name=%s and context=%s"
                        cur.execute(sql,(uname,context,title,id,ucontext))
                        connection.commit()
                         
                        
                    return redirect(url_for('board'))  
                        
            else:
                # 밑에 기존 내용 보여주는 코드
                cursor = connection.cursor()
                cursor.execute("select name,context,title from my_table")
                data = cursor.fetchall()
                
                return render_template("update.html", hang=data)
                ###### --> data 변수에 저장된 select값을 update.html파일의 hang변수에 매칭한다. (할당한다.) #######
                
        else:
            flash("수정권한이 없습니다.")
            return redirect(url_for('board')) 
    


 
 

# 게시글 삭제
@app.route("/delete/<uname>,<ucontext>")
def delete(uname,ucontext):
    
    if session.get('id') is None:
        flash("로그인을 하세요.")
        return redirect(url_for('user_info')) 
    
    else:
        id = session['id']
        
        connection = pymysql.connect(**DATABASE)
        
        if (id==uname):
            with connection.cursor() as cur:
                sql = "DELETE FROM my_table WHERE name=%s and context=%s"
                cur.execute(sql,(id,ucontext))
                connection.commit()
    
                return redirect(url_for('board'))
            
        else:
            flash("삭제권한이 없습니다.")
            return redirect(url_for('board'))  

    
        



app.secret_key = 'sample_secret_key'




if __name__ == '__main__':
    app.run(debug=True) 

