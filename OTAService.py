from flask import Flask, abort, request, helpers
import handleDB

app = Flask(__name__)


@app.route("/")
def index():
    return "hello"


@app.route('/getlastversion', methods=['POST'])
def getlastvrsion():
    """
    获取最新版本接口

    请求方式 :   POST
    请求参数 :   Body:imei
    返回结果 :   版本号或IMEI被禁止
    返回类型 :   String
    错误说明 :   如果缺少参数，返回 404
                 如果IMEI不在数据库中，返回 405
    """
    imei = request.form.get('imei')
    if imei is None:
        abort(404)
    enable = handleDB.handleSqlite3().compareIMEI(imei)
    if enable == 'True':
        lastversion = handleDB.handleSqlite3().getLastVersion()
        handleDB.handleSqlite3().closeDB()
        return lastversion
    elif enable == 'False':
        return 'IMEIForbidden'
    else:
        abort(405)


@app.route('/getdownfile')
def getdownfile():
    """
    根据给定的版本号，返回下载地址链接

    请求方式 :   GET
    请求参数 :   headers:version
    返回结果 :   下载地址
    返回类型 :   String
    错误说明 :   如果缺少版本号或版本号错误，返回 404
    """
    versionlist = handleDB.handleSqlite3().getAllVersion()
    version = request.headers.get('version')
    if version in versionlist:
        downfiletuple = handleDB.handleSqlite3().getDownFile(version)
        handleDB.handleSqlite3().closeDB()
        return helpers.send_from_directory(downfiletuple[0], downfiletuple[1], as_attachment=True)
    abort(404)

if __name__ == '__main__':
    app.run('0.0.0.0', 8080)
