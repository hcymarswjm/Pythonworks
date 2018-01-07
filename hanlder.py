import web
import datetime
import tornado
import dbconn
import json
class BaseReqHandler(tornado.web.RequestHandler):
    def db_cursor(self, autocommit=True):
        return dbconn.SimpleDataCursor(autocommit=autocommit)


from tornado.options import define,options
define("port",default=8888,help="run on the given port",type=int)

class IndexHandler(BaseReqHandler):
    def get(self):
        self.render('pages/base.html')
class IndexHandlerT(BaseReqHandler):
    def get(self):
        self.render('pages/teacher.html')

class teacherhandler(BaseReqHandler):
    def get(self):
        with self.db_cursor() as cur:
            sql='''    
                SELECT t.tsn ,t.tname,c.csn,c.cname,c.time,c.site
    FROM course as c
    LEFT JOIN teacher as t on c.teacher_sn=t.tsn;'''
            cur.execute(sql)
            items = cur.fetchall()
            data=[]
            s="["
            s1=''
            for item in items:
                a=list(item)
                s1+='{"tsn":"'+str(a[0])+'","tname":"'+str(a[1])+'","csn":"'+str(a[2])+'","cname":"'+str(a[3])+'","time":"'+str(a[4])+'","site":"'+str(a[5])+'"},'
            s2=s+s1+"]"
            self.write(s2)
        #data='[{"tsn":"7","tname":"8","csn":"91","cno":"19","cname":"25","time":"f","site":"fd"},{"tsn":"7","tname":"8","csn":"91","cno":"19","cname":"25","time":"f","site":"fd"}]'

    
    def post(self):
        jsd=json.loads(self.request.body)
        with self.db_cursor() as dc:
            #sql ='''select distinct tsn from teacher order by tsn;'''
            #dc.execute(sql)
            #sn=dc.fetchall()
            #if jsd('tsn') not in sn:
                #sql1='''INSERT INTO teacher(tsn,tname) VALUES(%s,%s);'''
                #dc.execute(sql1,[jsd('tsn'),jsd('tname')])
            sql2 = '''
            INSERT INTO course 
                (csn,cname,time,site,teacher_sn)
                VALUES(%s,%s,%s,%s,%s);
            '''
            dc.execute(sql2, (jsd['csn'],jsd['cname'],jsd['time'],jsd['site'],jsd['tsn']))
    
    def delete(self,sn):
        with self.db_cursor() as cur:
            sql1='DELETE FROM schedule WHERE course_sn=%s'
            cur.execute(sql1, (sn,))
            sql2 = "DELETE FROM course WHERE csn= %s"
            cur.execute(sql2, (sn,))

class teacherhandler_q(BaseReqHandler):
    def get(self,sn):
        with self.db_cursor() as cur:
            sql='''    
                SELECT t.tsn ,t.tname,c.csn,c.cname,c.time,c.site
    FROM course as c
    LEFT JOIN teacher as t on c.teacher_sn=t.tsn
    where c.teacher_sn=%s;'''
            cur.execute(sql,(sn,))
            items = cur.fetchall()
            data=[]
            s="["
            s1=''
            for item in items:
                a=list(item)
                s1+='{"tsn":"'+str(a[0])+'","tname":"'+str(a[1])+'","csn":"'+str(a[2])+'","cname":"'+str(a[3])+'","time":"'+str(a[4])+'","site":"'+str(a[5])+'"},'
            s2=s+s1+"]"
            print(s2)
            self.write(s2)
        #datae='[{"tsn":"7","tname":"8","csn":"91","cno":"19","cname":"25","time":"f","site":"fd"}]'

    def post(self):
        jsd=json.loads(self.request.body)
        with self.db_cursor() as dc:
            sql = ''' 
            UPDATE course SET 
            cname=%s,time=%s, site=%s,teacher_sn=%s
            WHERE csn=%s;
            '''
            dc.execute(sql, (jsd['cname'],jsd['time'],jsd['site'],jsd['tsn'],jsd['csn']))
class IndexHandlerS(BaseReqHandler):
    def get(self):
        self.render('pages\student.html')
class studenthandler(BaseReqHandler):
    def get(self):
        with self.db_cursor() as cur:
            sql='''    
                SELECT s.ssn,s.sname,c.csn,c.cname,c.time,c.site,t.tname
                 FROM schedule as sd
                 INNER JOIN course as c on sd.course_sn=c.csn
                 INNER JOIN teacher as t  on c.teacher_sn=t.tsn
                INNER JOIN student as s on sd.student_sn=s.ssn;'''
            cur.execute(sql)
            items = cur.fetchall()
            data=[]
            s="["
            s1=''
            for item in items:
                a=list(item)
                s1+='{"ssn":"'+str(a[0])+'","sname":"'+str(a[1])+'","csn":"'+str(a[2])+'","cname":"'+str(a[3])+'","time":"'+str(a[4])+'","site":"'+str(a[5])+'","tname":"'+str(a[6])+'"},'
            s2=s+s1+"]"
            self.write(s2)
    
    def post(self):
        jsd=json.loads(self.request.body)
        with self.db_cursor() as dc:
            #sql ='''select distinct ssn from student order by ssn;'''
            #dc.execute(sql)
            #sn=dc.fetchall()
            sql2 = '''
            INSERT INTO schedule 
                (student_sn,course_sn)
                VALUES(%s,%s);
            '''
            dc.execute(sql2, (jsd['ssn'],jsd['csn']))
   
    def delete(self,ssn,csn):
        with self.db_cursor() as cur:
            sql = "DELETE FROM schedule WHERE student_sn= %s and course_sn=%s"
            cur.execute(sql, (ssn,csn))
        print("====")
			
class studenthandler_q(BaseReqHandler):
    def get(self,sn):
        with self.db_cursor() as cur:
            sql='''    
                SELECT s.ssn,s.sname,c.csn,c.cname,c.time,c.site,t.tname
                 FROM schedule as sd
                 INNER JOIN course as c on sd.course_sn=c.csn
                 INNER JOIN teacher as t  on c.teacher_sn=t.tsn
                INNER JOIN student as s on sd.student_sn=s.ssn
                where s.ssn=%s;'''
            cur.execute(sql,(sn,))
            items = cur.fetchall()
            data=[]
            s="["
            s1=''
            for item in items:
                a=list(item)
                s1+='{"ssn":"'+str(a[0])+'","sname":"'+str(a[1])+'","csn":"'+str(a[2])+'","cname":"'+str(a[3])+'","time":"'+str(a[4])+'","site":"'+str(a[5])+'","tname":"'+str(a[6])+'"},'
            s2=s+s1+"]"
            self.write(s2)
        datae='[{"ssn":"7","sname":"8","csn":"91","cno":"19","cname":"25","time":"f","site":"fd","tname":"56"}]'        
