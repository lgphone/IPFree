import tornado.web
import re
import json
from models.ipcenter import exec_query_ip

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('main.html')

    def post(self):
        ret = {'status': 'true', 'message': '', 'data': '','code': 200}
        query_ip = self.get_argument("query_ip", None)

        if query_ip and re.match(r'^(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}$', query_ip):
            ip_info = exec_query_ip(query_ip)
            if ip_info['status']:
                ret['message'] = '查询成功'
                ret['data'] = ip_info['data']
            else:
                ret['code'] = 502
                ret['status'] = 'false'
                ret['message'] = '数据库查询失败'
        else:
            ret['code'] = 403
            ret['status'] = 'false'
            ret['message'] = '请输入正确格式IP地址'
        print(ret)
        return self.write(json.dumps(ret))