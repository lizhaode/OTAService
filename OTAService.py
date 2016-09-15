
from flask import Flask
from flask import request
import handleDB

app = Flask(__name__)


@app.route('/getlastversion',methods=['POST'])
def getlastvrsion():
    try:
        imei = request.form['imei']
        enable = handleDB.handleSqlite3().compareIMEI(imei)
        if enable == 'True':
            lastversion = handleDB.handleSqlite3().getLastVersion()
            handleDB.handleSqlite3().closeDB()
            return lastversion
        elif enable == 'False':
            return 'False'
        else:
            return None
    except Exception as e:
        print(e)
        return e


if __name__ == '__main__':
    app.run('0.0.0.0',8080)
