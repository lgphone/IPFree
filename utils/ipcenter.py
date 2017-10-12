#!/usr/bin/python3
import pymysql.cursors
from config import DB_CONF


class DB():
    def init_conn(self):
        self.conn = pymysql.connect(host=DB_CONF['host'],
                                    user=DB_CONF['user'],
                                    password=DB_CONF['password'],
                                    db=DB_CONF['db'],
                                    charset=DB_CONF['charset'],
                                    cursorclass=pymysql.cursors.DictCursor)

    def re_conn(self):
        while 1:
            try:
                if self.conn.ping():
                    return self.conn
            except Exception as e:
                print('连接错误:{_e} 重新连接'.format(_e=e))
                self.init_conn()
                return self.conn

    def close_conn(self):
        if self.conn.ping():
            self.conn.close()

DBdrive = DB()

def exec_query_ip(ip='127.0.0.1'):
    ret = {'status': True,
           'data': ''}
    query_sql = "SELECT * FROM `aiwen_free_district_v2.0.1` WHERE minip <= INET_ATON(%s) ORDER BY minip DESC LIMIT 1"
    try:
        with DBdrive.re_conn().cursor() as cursor:
            cursor.execute(query_sql, (ip,))
            result = cursor.fetchone()
            ret['data'] = result
    except Exception as e:
        print('error', e)
        ret['status'] = False
    finally:
        return ret

def exec_count_ip(ip='127.0.0.1'):
    ret = {'status': True,
           'data': ''}

    query_sql = "SELECT * FROM `user_ip_count` WHERE ip = %s"
    update_sql = "UPDATE `user_ip_count` SET ip_count=ip_count+1 where ip = %s"
    insert_sql = "INSERT INTO user_ip_count(ip,ip_count) VALUES (%s,%s)"
    try:
        with DBdrive.re_conn().cursor() as cursor:
            cursor.execute(query_sql, (ip,))
            result = cursor.fetchone()
            #print(result)
            if result:
                cursor.execute(update_sql, (ip,))
                cursor.execute(query_sql, (ip,))
                result = cursor.fetchone()
                DBdrive.re_conn().commit()
            else:
                cursor.execute(insert_sql, (ip, 1))
                cursor.execute(query_sql, (ip,))
                result = cursor.fetchone()
                DBdrive.re_conn().commit()
            ret['data'] = result
    except Exception as e:
        print('error', e)
        ret['status'] = False
    finally:
        return ret

def exec_count_api(action='query'):
    ret = {'status': True,
           'data': ''}
    update_sql = "UPDATE `total_visits` SET total_visits=total_visits+1"
    query_sql = "SELECT * FROM `total_visits`"
    try:
        with DBdrive.re_conn().cursor() as cursor:
            if action == 'query':
                cursor.execute(query_sql)
                result = cursor.fetchone()
                ret['data'] = result
            else:
                cursor.execute(update_sql)
                DBdrive.re_conn().commit()
    except Exception as e:
        print('error', e)
        ret['status'] = False
    finally:
        return ret
