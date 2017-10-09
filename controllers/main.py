import tornado.web
import re
from utils.ipcenter import exec_query_ip, exec_count_api, exec_count_ip

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        # print(self.request.remote_ip)
        # 获取本次本IP访问次数
        remote_ip = self.request.remote_ip
        if not remote_ip:
            remote_ip = "获取不到您的IP"
        count_ip_info = exec_count_ip(remote_ip)
        if count_ip_info['status']:
            count_ip = count_ip_info['data']
        else:
            count_ip = {'ip_count': 0, 'ip': '获取不到您的IP'}

        # 获取API总共请求次数
        count_api_info = exec_count_api()
        if count_api_info['status']:
            count_api = count_api_info['data']['total_visits']
        else:
            count_api = '统计出错'
        self.render('main.html', count_api=count_api, count_ip=count_ip)

class IPFreeHandler(tornado.web.RequestHandler):
    def get(self):
        ret = {'status': 'true', 'message': '', 'data': '', 'query_ip': '', 'code': 200}
        query_ip = self.get_argument("query_ip", None)
        callback = self.get_argument('callback', None)
        if query_ip and re.match(r'^(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}$', query_ip):
            ret['query_ip'] = query_ip
            ip_info = exec_query_ip(query_ip)
            if ip_info['status']:
                ret['message'] = '查询成功'
                ret['data'] = ip_info['data']
                # 增加一次统计
                exec_count_api(action='update')
            else:
                ret['code'] = 502
                ret['status'] = 'false'
                ret['message'] = '数据库查询失败'
        else:
            ret['code'] = 403
            ret['status'] = 'false'
            ret['message'] = '请输入正确格式IP地址'

        if callback:
            ret_data = callback + "({_ret})".format(_ret=str(ret))
        else:
            ret_data = 'ipFreeData' + "({_ret})".format(_ret=str(ret))
        # print(ret_data)
        return self.write(ret_data)

