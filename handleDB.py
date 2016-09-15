import sqlite3
import sys

class handleSqlite3():

    def __init__(self):

        self.mSqlite3 = sqlite3.connect('{}/UpdateInfo.db'.format(sys.path[0]))
        self.mCursor = self.mSqlite3.cursor()

    def closeDB(self):

        self.mCursor.close()
        self.mSqlite3.close()


    def compareIMEI(self,imei):
        """
        比较传入的 IMEI 值，返回是否可以升级信息
        返回值：True
                False
        返回值类型：String
        """

        try:
            value = self.mCursor.execute('select Enable from IMEIList where IMEI=?',[imei]).fetchall()
            if len(value) != 0:
                return value[0][0]
            else:
                print('IMEI不存在数据库中')
        except sqlite3.OperationalError as e:
            print(e)

    def getLastVersion(self):
        """
        返回数据库中最新的版本
        返回值：version
        返回值类型：String
        """

        value = self.mCursor.execute('select Version from UpdateInfo order by Version desc').fetchone()
        if value != None:
            return value[0]
        else:
            print('获取version数据失败')

    def getAllVersion(self):
        """
        返回数据库中所有的版本
        返回值：version
        返回值类型：list
        """
        value = self.mCursor.execute('select Version from UpdateInfo').fetchall()
        if len(value) != 0:
            return value[0]
        else:
            print('获取version数据失败')

    def getDownFile(self,version):
        """
        根据给定的 version 返回下载路径和下载文件
        返回值：filepath,filename
        返回值类型：tuple
        """
        filepath = None
        filename = None
        value = self.mCursor.execute('select FilePath from UpdateInfo where Version=?',[version]).fetchone()
        if value != None:
            filepath = value[0]
        else:
            print('获取filepath数据失败')
        value = self.mCursor.execute('select FileName from UpdateInfo where Version=?',[version]).fetchone()
        if value != None:
            filename = value[0]
        else:
            print('获取filename数据失败')
        if filename != None:
            if filepath != None:
                return (filepath,filename)
