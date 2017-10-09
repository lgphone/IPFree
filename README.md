# IPFree
IP地址归属地查询，精确到县级
## 技术结构
* 使用Tornado + pymysql + bootstrap
* 核心数据库使用IP问问数据库
## Demo 地址
[http://ipfree.izhihu.me](http://ipfree.izhihu.me)
## 新增jsonp调用方式
* API地址 http://ipfree.izhihu.me/ipfree?query_ip=123.125.114.5&callback=getIpFree
* query_ip 参数为查询IP
* callback 参数为回调函数名称，如果不指定默认为ipFreeData
* 返回状态 arg.status true 成功 false 失败
* 返回状态码 200 成功 403 IP地址格式不正确 502 后端数据库查询失败，数据库挂了
* 具体返回数据为：    
```getIpFree({'data': {'maxip': 2071819263, 'multiarea': '[{"w":"39.903169","j":"116.391448","p":"北京市","c":"北京市","d":""}]', 'areacode': 'CN', 'user': 'SGGHN', 'minip': 2071818240, 'id': 14897568, 'continent': '亚洲', 'country': '中国'}, 'status': 'true', 'query_ip': '123.125.114.5', 'code': 200, 'message': '查询成功'})```
## 新增统计访问次数及api调用次数显示,需要创建表
* API调用总计
```CREATE TABLE `total_visits` (
  `total_visits` int(255) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;INSERT INTO `total_visits` VALUES ('0');```
* 单用户访问记录
```CREATE TABLE `user_ip_count` (
  `ip` varchar(255) NOT NULL,
  `ip_count` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`ip`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;```
## 运行界面
主界面
![主界面](https://github.com/lgphone/IPFree/blob/master/doc/pic/index.png)
查询界面
![查询界面](https://github.com/lgphone/IPFree/blob/master/doc/pic/query.png)
## 重要！！
* 数据库仅供学习和测试使用
* 感谢IP问问的免费IP库

