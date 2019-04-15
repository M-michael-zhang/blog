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
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@123.207.233.171:3306/blog"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_POOL_SIZE']=100
app.config['SQLALCHEMY_MAX_OVERFLOW']=20

db = SQLAlchemy(app)
# db = create_engine("mysql://root:root@123.207.233.171:3306/blog", pool_size=100, max_overflow=20)


@app.route('/')
def main():
    return render_template('main.html')

if __name__ == '__main__':
    app.run()

@app.route('/getArticles')
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

@app.route('/addArticles')
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
    return "Publish Successfully!"

@app.route('/getArticlesById')
def getArticlesById():
    id = request.args.get("id")
    articles = Article.query.filter(Article.id == id).all()
    result = []
    for article in articles:
        article.time=article.time.strftime("%Y-%m-%d %H:%M:%S")
        result.append(article.to_json())
    return jsonify(result), 200

@app.route('/getArticlesByTitle')
def getArticlesByTitle():
    title= request.args.get("title")
    articles = Article.query.filter(Article.title == title).all()
    result = []
    for article in articles:
        article.time=article.time.strftime("%Y-%m-%d %H:%M:%S")
        result.append(article.to_json())
    return jsonify(result), 200

@app.route('/getArticlesByAuthor')
def getArticlesByAuthor():
    author = request.args.get("author")
    articles = Article.query.filter(Article.author == author).all()
    result = []
    for article in articles:
        article.time=article.time.strftime("%Y-%m-%d %H:%M:%S")
        result.append(article.to_json())
    return jsonify(result), 200


@app.route('/getArticlesBySubject')
def getArticlesBySubject():
    subject = request.args.get("subject")
    articles = Article.query.filter(Article.subject == subject).all()
    result = []
    for article in articles:
        article.time=article.time.strftime("%Y-%m-%d %H:%M:%S")
        result.append(article.to_json())
    return jsonify(result), 200

@app.route('/delArticlesById')
def delArticlesById():
    id = request.args.get("id")
    articles = db.session.query(Article).filter(Article.id == id).all()
    db.session.delete(articles[0])
    db.session.commit()
    return jsonify("The article which id is " +id+ " has been deleted successfully!"),200


# subects operation

@app.route('/getSubjects')
def getSubjects():
    articles = Subject.query.all()
    result = []
    for article in articles:
        result.append(article.to_json())
    return jsonify(result), 200


@app.route('/getSubjectsById')
def getSubjectsById():
    sid = request.args.get("sid")
    articles = Subject.query.filter(Subject.sid == sid).all()
    result = []
    for article in articles:
        result.append(article.to_json())
    return jsonify(result), 200

@app.route('/getSubjectsByGS')
def getSubjectsByGS():
    generalSubject = request.args.get("gsid")
    articles = Subject.query.filter(Subject.generalSubject == generalSubject).all()
    result = []
    for article in articles:
        result.append(article.to_json())
    return jsonify(result), 200

@app.route('/addSubject')
def addSubject():
    gsid = request.args.get("gsid")
    name = request.args.get("name")
    a =Subject(None, name, gsid)
    db.session.add(a)
    db.session.commit()
    return "Successful insertion"

@app.route('/isSameSubject')
def isSameSubject():
    sname = request.args.get("sname")
    subject = Subject.query.filter(Subject.sname == sname).all()
    if not subject:
        return jsonify(0)
    else:
        return jsonify(1)

#general subject
@app.route('/getGeneralSubjects')
def getGeneralSubjects():
    articles = GeneralSubject.query.all()
    result = []
    for article in articles:
        result.append(article.to_json())
    return jsonify(result), 200

@app.route('/getGeneralSubjectById')
def getGeneralSubjectById():
    gid = request.args.get("gid")
    articles = GeneralSubject.query.filter(GeneralSubject.gid == gid).all()
    result = []
    for article in articles:
        result.append(article.to_json())
    return jsonify(result), 200

#comment
@app.route('/getCommentByArticle')
def getCommentByArticle():
    aid = request.args.get("aid")
    articles = Comment.query.filter(Comment.aid == aid).all()
    result = []
    for article in articles:
        article.time = article.time.strftime("%Y-%m-%d %H:%M:%S")
        result.append(article.to_json())
    return jsonify(result), 200

@app.route('/addComment')
def addComment():
    aid = request.args.get("aid")
    reader = request.args.get("reader")
    content = request.args.get("content")
    time = datetime.datetime.now()
    a =Comment(None, aid, reader,  content, time)
    db.session.add(a)
    db.session.commit()
    return "Comment Successfully!"

@app.route('/delCommentById')
def delCommentById():
    cid = request.args.get("cid")
    articles = db.session.query(Comment).filter(Comment.cid == cid).all()
    db.session.delete(articles[0])
    db.session.commit()
    return jsonify("The comment which id is " + cid + " has been deleted successfully!"), 200
#inner comment
@app.route('/getInnerCommentByCid')
def getInnerCommentByCid    ():
    cid = request.args.get("cid")
    articles = Comment.query.filter(Comment.cid == cid).all()
    result = []
    for article in articles:
        article.time = article.time.strftime("%Y-%m-%d %H:%M:%S")
        result.append(article.to_json())
    return jsonify(result), 200

@app.route('/addInnerComment')
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
@app.route('/getCountLikedByAid')
def getCountLikedByAid():
    aid = request.args.get("aid")
    data = Liked.query.filter(Liked.aid == aid).all()
    count=0
    for o in data:
        count=count+1
    return jsonify(count), 200

@app.route('/getIsLiked')
def getIsLiked():
    aid = request.args.get("aid")
    reader = request.args.get("reader")
    data = Liked.query.filter(and_( Liked.aid ==aid,Liked.reader==reader))
    count=0
    for o in data:
        count=count+1
    return jsonify(count), 200

@app.route('/addLiked')
def addLiked():
    aid = request.args.get("aid")
    reader = request.args.get("reader")
    a = Liked(None, aid, reader)
    db.session.add(a)
    db.session.commit()
    return "liked it successfully!"

@app.route('/getCountDislikedByAid')
def getCountDislikedByAid():
    aid = request.args.get("aid")
    data = Disliked.query.filter(Disliked.aid == aid).all()
    count=0
    for o in data:
        count=count+1
    return jsonify(count), 200

@app.route('/getIsDisliked')
def getIsDisliked():
    aid = request.args.get("aid")
    reader = request.args.get("reader")
    data = Disliked.query.filter(and_( Disliked.aid ==aid,Disliked.reader==reader))
    count=0
    for o in data:
        count=count+1
    return jsonify(count), 200

@app.route('/addDisliked')
def addDisliked():
    aid = request.args.get("aid")
    reader = request.args.get("reader")
    a = Disliked(None, aid, reader)
    db.session.add(a)
    db.session.commit()
    return "disliked it successfully!"
#file upload and download
@app.route('/upload',methods=['GET', 'POST'])
def upload():
    fs = request.files["articlePDF"]
    name = ''.join(random.sample(string.ascii_letters + string.digits, 15))
    name=name+".pdf"
    fs.save(os.path.join("static/document", name))
    return name

#forward page

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

@app.route('/about/')
def about():
    if request.method == 'GET':
        return render_template('about.html')
    else:
        pass