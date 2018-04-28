'''
Created on Mar 26, 2018

@author: alfred
'''
import pymysql

class DBModule(object):
    '''
    this is class is meant to perform tasks with mysql databases
    '''

    def __init__(self, **kwargs):
        conn = self.getConnection(kwargs['user'],kwargs['pswd'],kwargs['host'],kwargs['db'])
        if conn:
            self.conn,self.cursor = conn
    
    def getConnection(self, user=None, pswd=None, host=None, db=None):    
        if not user and not user:
            print("no user or host")
            return False,_
        if not db:
            print("no database or schema")
            return False
        try:
            connection = pymysql.connect(host=host, user=user, password=pswd, db=db)
            cursor = connection.cursor()
        except:
            print('Failed to create connection')
            return False
        return connection,cursor
    
    def selectStuff(self,query):
        #try:
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        #except:
         #   print("Haha things went wrong")
         #   return False
        tray = []
        for result in results:
            hold = []
            for item in result:
                hold.append(str(item))
            tray.append(hold)
        return tray
    
    def selectOne(self,query):
        #try:
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        #except:
        return result

    def insertToDB(self,query):
        self.cursor.execute(query)
        self.conn.commit()
    
    def __quit__(self):
        self.cursor.close()
        self.conn.close()


def main():
    query = 'select inst_id, date_downloaded, amount from trans where date(date_downloaded) = "%s" '
    date =  "2012-10-30"
    model = DBModule(host='localhost',user='root',pswd='carrot24',db='transflow')
    result = model.selectStuff(query%date)
    for item in result:
        print(item)

if __name__=="__main__":
    main()
