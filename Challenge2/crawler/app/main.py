from flask import Blueprint, request, jsonify, make_response ,Flask,_app_ctx_stack, jsonify, url_for
from flask_restful import Api, Resource
import datetime
from worker import Worker
from flask_cors import CORS
from sqlalchemy import Column, DateTime, Integer, MetaData ,String, PrimaryKeyConstraint,ForeignKey
from sqlalchemy.sql.expression import false
from sqlalchemy.sql.sqltypes import Boolean
from config import SessionLocal, engine, SQLALCHEMY_DATABASE_URL
from sqlalchemy.orm import scoped_session 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from sqlalchemy.sql import func
import logging

logging.basicConfig(
     filename='crawler.log',
     level=logging.DEBUG, 
     format= '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
     datefmt='%H:%M:%S'
 )
app = Flask(__name__)
CORS(app)
app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URL
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)

api = Api(app)
class URLs(db.Model):
    __tablename__ = "TBL-crawl-url"
    
    ID = Column(Integer, primary_key=True)
    url = Column(String,index=True)
    level = Column(Integer,index=False)
    create_at = Column(String,index=False)

    def __init__(self,url,level,create_at):
        self.url = url
        self.level = level
        self.create_at = create_at

class Crawler(db.Model):
    __tablename__ = "TBL-crawler"
    ID_session = Column(Integer,primary_key=True)
    url = Column(String, primary_key=True)
    is_internal_url = Column(Boolean)
    __table_args__ = (
        PrimaryKeyConstraint(ID_session, url),
        {},
    )
    def __init__(self,ID_session,url,is_internal_url):
        self.ID_session = ID_session
        self.url = url
        self.is_internal_url = is_internal_url

class UrlsSchema(ma.Schema):
    class Meta:
        fields = ('ID', 'url', 'level','create_at')
class CrawlerInfoSchema(ma.Schema):
    class Meta:
        fields =('url','is_internal_url')


crawlerinfo_schema = CrawlerInfoSchema()
crawlerinfos_schema = CrawlerInfoSchema(many=True)
spider = Worker(5)

class CrawlUrl(Resource):
    def post(self):
        raw_dict =  request.get_json(force=True)
        url = raw_dict['url']
        level =  raw_dict['level']
        nowtime = datetime.datetime.now().strftime("%Y-%m-%d")
        res =  URLs.query.filter(URLs.create_at ==nowtime,URLs.level == level , URLs.url == url).first()
        info = []
        if res is None:
            new_url = URLs(url,level,nowtime)
            try:
                db.session.add(new_url)
                db.session.commit()
            except Exception as e :
                logging.debug("Error insert url :"+str(e))
            ID = new_url.ID
            try:
                internal_url, external_url = spider.Execute(url=url,level=level)
            except Exception as e:
                logging.debug("Error crawler :"+str(e))
            info = []
            for it in internal_url:
                info.append(Crawler(ID_session=ID,url= it,is_internal_url= True))
            for it in external_url:
                info.append(Crawler(ID_session=ID,url= it,is_internal_url=False))
            try:
                db.session.add_all(info)
                db.session.commit()
            except Exception as e:
                logging.debug("Error insert save href :"+str(e))
        else :
            info = Crawler.query.filter(Crawler.ID_session== res.ID).all()
        return crawlerinfos_schema.jsonify(info)

api.add_resource(CrawlUrl,'/api/v1/crawler')

if __name__ == "__main__":
  app.run('0.0.0.0',port=8080)
