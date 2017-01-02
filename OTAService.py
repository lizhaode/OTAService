from flask import Flask, abort, request, helpers
import handleDB

app = Flask(__name__)


@app.route("/")
def index():
    return "hello"


@app.route('/getlastversion')
def getlastvrsion():
    """
    获取最新版本接口

    请求方式 :   GET
    请求参数 :   params:imei
    返回结果 :   版本号或IMEI Forbidden
    返回类型 :   String
    错误说明 :   如果缺少参数，返回 "Need Params"
                 如果参数为空，返回 "IMEI is Empty"
                 如果IMEI不在数据库中，返回 "IMEI Not In Database"
    """
    imei = request.args.get('imei')
    if imei is None:
        return 'Need Params'
    elif imei == '':
        return 'IMEI is Empty'
    enable = handleDB.handleSqlite3().compareIMEI(imei)
    if enable == 'True':
        lastversion = handleDB.handleSqlite3().getLastVersion()
        handleDB.handleSqlite3().closeDB()
        return lastversion
    elif enable == 'False':
        return 'IMEI Forbidden'
    else:
        return 'IMEI Not In Database'


@app.route('/getdownfile')
def getdownfile():
    """
    根据给定的版本号，返回下载地址链接

    请求方式 :   GET
    请求参数 :   params:version
    返回结果 :   下载地址
    返回类型 :   String
    错误说明 :   如果版本号错误，返回 Version Code Wrong
                 如果缺少版本号，返回 Need Params
                 如果版本号为空，返回 Params is Empty
                 如果下载地址对应的文件不存在，返回 404
    """
    versionlist = handleDB.handleSqlite3().getAllVersion()
    version = request.args.get('version')
    if version is None:
        return 'Need Params'
    elif version == '':
        return 'Params is Empty'
    if version in versionlist:
        downfiletuple = handleDB.handleSqlite3().getDownFile(version)
        handleDB.handleSqlite3().closeDB()
        return helpers.send_from_directory(downfiletuple[0], downfiletuple[1], as_attachment=True)
    else:
        return 'Version Code Wrong'
if __name__ == '__main__':
    app.run('0.0.0.0', 8080)
