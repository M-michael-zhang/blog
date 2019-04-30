import datetime
import json
import os

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, create_engine
import random
import string

from Model.Model import Article, Subject, GeneralSubject, Comment, InnerComment, Liked, Disliked

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@123.207.233.171:3306/blogs"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_POOL_SIZE']=100
app.config['SQLALCHEMY_MAX_OVERFLOW']=20

db = SQLAlchemy(app)
# db = create_engine("mysql://root:root@123.207.233.171:3306/Huang", pool_size=100, max_overflow=20)


@app.route('/')
def main():
    return render_template('main.html')

if __name__ == '__main__':
    app.run()

@app.route('/getArticles',methods=['GET', 'POST'])
def getArticless():
    articles = Article.query.all()
    count = Article.query.count()
    # return 'Hello World!'
    # return json.dumps(t, ensure_ascii=False)
    result = []
    for article in articles:
        article.time=article.time.strftime("%Y-%m-%d %H:%M:%S")
        result.append(article.to_json())
    # dict={}
    # dict['success'] = "true"
    # dict['articles']=result
    return jsonify(result), 200

@app.route('/addArticles',methods=['GET', 'POST'])
def addArticles():
    subject = request.args.get("subject")
    title = request.args.get("title")
    author = request.args.get("author")
    content = request.args.get("content")
    filename = request.args.get("filename")
    time = datetime.datetime.now()
    a =Article(None, subject,title, author, content, time,filename)
    db.session.add(a)
    db.session.commit()
    return "Successful insertion"

@app.route('/getArticlesById',methods=['GET', 'POST'])
def getArticlesById():
    id = request.args.get("id")
    articles = Article.query.filter(Article.id == id).all()
    result = []
    for article in articles:
        article.time=article.time.strftime("%Y-%m-%d %H:%M:%S")
        result.append(article.to_json())
    return jsonify(result), 200

@app.route('/getArticlesByTitle',methods=['GET', 'POST'])
def getArticlesByTitle():
    title= request.args.get("title")
    articles = Article.query.filter(Article.title == title).all()
    result = []
    for article in articles:
        article.time=article.time.strftime("%Y-%m-%d %H:%M:%S")
        result.append(article.to_json())
    return jsonify(result), 200

@app.route('/getArticlesByAuthor',methods=['GET', 'POST'])
def getArticlesByAuthor():
    author = request.args.get("author")
    articles = Article.query.filter(Article.author == author).all()
    result = []
    for article in articles:
        article.time=article.time.strftime("%Y-%m-%d %H:%M:%S")
        result.append(article.to_json())
    return jsonify(result), 200


@app.route('/getArticlesBySubject',methods=['GET', 'POST'])
def getArticlesBySubject():
    subject = request.args.get("subject")
    articles = Article.query.filter(Article.subject == subject).all()
    result = []
    for article in articles:
        article.time=article.time.strftime("%Y-%m-%d %H:%M:%S")
        result.append(article.to_json())
    return jsonify(result), 200


# subects操作

@app.route('/getSubjects',methods=['GET', 'POST'])
def getSubjects():
    articles = Subject.query.all()
    result = []
    for article in articles:
        result.append(article.to_json())
    return jsonify(result), 200

@app.route('/getSubjectsById',methods=['GET', 'POST'])
def getSubjectsById():
    sid = request.args.get("sid")
    articles = Subject.query.filter(Subject.sid == sid).all()
    result = []
    for article in articles:
        result.append(article.to_json())
    return jsonify(result), 200

@app.route('/getSubjectsByGS',methods=['GET', 'POST'])
def getSubjectsByGS():
    generalSubject = request.args.get("gsid")
    articles = Subject.query.filter(Subject.generalSubject == generalSubject).all()
    result = []
    for article in articles:
        result.append(article.to_json())
    return jsonify(result), 200

@app.route('/addSubject',methods=['PUTTER'])
def addSubject():
    gsid = request.args.get("gsid")
    name = request.args.get("name")
    a =Subject(None, name, gsid)
    db.session.add(a)
    db.session.commit()
    return "Successful insertion"

#general subject
@app.route('/getGeneralSubjects',methods=['GET', 'POST'])
def getGeneralSubjects():
    articles = GeneralSubject.query.all()
    result = []
    for article in articles:
        result.append(article.to_json())
    return jsonify(result), 200

#comment
@app.route('/getCommentByArticle',methods=['GET', 'POST'])
def getCommentByArticle():
    aid = request.args.get("aid")
    articles = Comment.query.filter(Comment.aid == aid).all()
    result = []
    for article in articles:
        article.time = article.time.strftime("%Y-%m-%d %H:%M:%S")
        result.append(article.to_json())
    return jsonify(result), 200

@app.route('/addComment',methods=['PUT'])
def addComment():
    aid = request.args.get("aid")
    reader = request.args.get("reader")
    content = request.args.get("content")
    print(content)
    time = datetime.datetime.now()
    a =Comment(None, aid, reader,  content, time)
    db.session.add(a)
    db.session.commit()
    return "Successful insertion"

#inner comment
@app.route('/getInnerCommentByCid',methods=['GET', 'POST'])
def getInnerCommentByCid    ():
    cid = request.args.get("cid")
    articles = Comment.query.filter(Comment.cid == cid).all()
    result = []
    for article in articles:
        article.time = article.time.strftime("%Y-%m-%d %H:%M:%S")
        result.append(article.to_json())
    return jsonify(result), 200

@app.route('/addInnerComment',methods=['PUT'])
def addInnerComment():
    cid = request.args.get("cid")
    reader = request.args.get("reader")
    content = request.args.get("content")
    time = datetime.datetime.now()
    a =InnerComment(None, cid, reader,  content, time)
    db.session.add(a)
    db.session.commit()
    return "Successful insertion"

#liked
@app.route('/getCountLikedByAid',methods=['GET', 'POST'])
def getCountLikedByAid():
    aid = request.args.get("aid")
    data = Liked.query.filter(Liked.aid == aid).all()
    count=0
    for o in data:
        count=count+1
    return jsonify(count), 200

@app.route('/getIsLiked',methods=['GET', 'POST'])
def getIsLiked():
    aid = request.args.get("aid")
    reader = request.args.get("reader")
    data = Liked.query.filter(and_( Liked.aid ==aid,Liked.reader==reader))
    count=0
    for o in data:
        count=count+1
    return jsonify(count), 200

@app.route('/addLiked',methods=['GET', 'POST'])
def addLiked():
    aid = request.args.get("aid")
    reader = request.args.get("reader")
    a = Liked(None, aid, reader)
    db.session.add(a)
    db.session.commit()
    return "liked it success!"

@app.route('/getCountDislikedByAid',methods=['GET', 'POST'])
def getCountDislikedByAid():
    aid = request.args.get("aid")
    data = Disliked.query.filter(Disliked.aid == aid).all()
    count=0
    for o in data:
        count=count+1
    return jsonify(count), 200

@app.route('/getIsDisliked',methods=['GET', 'POST'])
def getIsDisliked():
    aid = request.args.get("aid")
    reader = request.args.get("reader")
    data = Disliked.query.filter(and_( Disliked.aid ==aid,Disliked.reader==reader))
    count=0
    for o in data:
        count=count+1
    return jsonify(count), 200

@app.route('/addDisliked',methods=['GET', 'POST'])
def addDisliked():
    aid = request.args.get("aid")
    reader = request.args.get("reader")
    a = Disliked(None, aid, reader)
    db.session.add(a)
    db.session.commit()
    return "disliked it success!"
#file上传下载
@app.route('/upload',methods=['GET', 'POST'])
def upload():
    fs = request.files["articlePDF"]
    name = ''.join(random.sample(string.ascii_letters + string.digits, 15))
    name=name+".pdf"
    fs.save(os.path.join("static/document", name))
    return name

#页面跳转

@app.route('/subject/')
def subject():
    if request.method == 'GET':
        return render_template('subject.html')
    else:
        pass

@app.route('/article/')
def article():
    if request.method == 'GET':
        return render_template('article.html')
    else:
        pass

@app.route('/newArticle/')
def newArticle():
    if request.method == 'GET':
        return render_template('newArticle.html')
    else:
        pass

@app.route('/donation/')
def donation():
    if request.method == 'GET':
        return render_template('donation.html')
    else:
        pass

@app.route('/search/')
def search():
    if request.method == 'GET':
        return render_template('search.html')
    else:
        pass

@app.route('/detail/')
def detail():
    if request.method == 'GET':
        return render_template('detail.html')
    else:
        pass