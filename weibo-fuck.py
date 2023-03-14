# -*- coding: utf-8 -*-
import http.client
import mimetypes
from codecs import encode
import json
import os

realname = os.environ.get('REAL_NAME')
email = os.environ.get('EMAIL')
id_num = os.environ.get('ID_NUMBER')
mobile = os.environ.get('MOBILE_PHONE')

conn = http.client.HTTPSConnection("ts.isc.org.cn")
dataList = []
boundary = 'WebKitFormBoundaryS2K5BdawhGxhhoS5'
dataList.append(encode('--' + boundary))
dataList.append(encode('Content-Disposition: form-data; name=body;'))

dataList.append(encode('Content-Type: {}'.format('text/plain')))
dataList.append(encode(''))

dataList.append(encode("{\"complaintedEnterprise1\":\"\",\"complaintedEnterprise2\":\"新浪微博\",\"complaintType\":1,\"complaintSource\":\"0\",\"loginFlag\":true,\"isAllFlag\":true,\"idnumber\":\"" + id_num + "\",\"agentname\":\"" + realname + "\",\"agentmobile\":\"" + mobile + "\",\"sex\":\"1\",\"address\":[\"110000\",\"110105\"],\"email\":\"" + email + "\",\"validateCode\":\"haks\",\"code\":\"\",\"complaintedEnterprise\":\"新浪微博\",\"complaintTwoProblemId\":\"103\",\"complaintThreeProblemId\":\"4b3178facaae4ec1b23d9a2a973f9d2f\",\"complaintOneProblemId\":\"207\",\"complaintBusinessId\":\"213\",\"mblogName\":\"Jon_Showing\",\"mblogLoginName\":\"Jon_Showing\",\"accessArtificialFlag\":\"1\",\"appFlag\":\"1\",\"complaintTitle\":\"有关站方不按自己所定规则直接封禁这件事\",\"problemDetails\":\"原告的新浪微博账号自2009年就已注册，昵称“Jon_Showing”，UID：1444146297，已实名绑定手机号18501947342。至今已发布微博1万6千余条，是分享生活与想法的账号。\\n2022年4月14日上午，原告的微博账号突然不能使用，且未收到任何告知。经原告向“互联网信息服务投诉平台”申诉过后，被告回复称违反了《微博社区公约》第五章，但仍没有指出具体是哪一条、违反了具体什么内容。\\n经查，《微博社区公约》第五章所述是“时政有害信息”，其中规定“时政有害信息的界定呈现、处置原则、处置方式、处置结果规定于《微博投诉操作细则》。”且不论原告所发布内容是否可以认定为“时政有害信息”，单是《微博投诉操作细则》中所约定的处置程序被告都完全没有遵守。\\n第八条“时政有害信息处置结果”规定：\\n“（一）发布时政有害信息的用户，警告并删除相关内容。\\n(二）转发时政有害信息作为讨论对象造成传播的用户，限制展示或屏蔽有关内容，\\n(三）累计发布5条及以上时政有害信息的用户，禁言48小时，并删除相关内容\\n(四）恶意发布时政有害信息的用户，应禁言48小时或以上，直至限制访问。”\\n按照被告方自己所写的规定，处罚应该从“警告并删除相关内容”开始，或至少是“禁言48小时或以上”开始，而不是直接把账号禁止掉。\\n依据《中华人民共和国民法典》第三条，民事主体的人身权利、财产权利以及其他合法权益受法律保护，任何组织或者个人不得侵犯。\\n依据《中华人民共和国民法典》第一百一十三条，民事主体的财产权利受法律平等保护。\\n依据《中华人民共和国民法典》第一百二十七条，法律对数据、网络虚拟财产的保护有规定的，依照其规定。\\n再依据《中华人民共和国民法典》第五百七十七条，当事人一方不履行合同义务或者履行合同义务不符合约定的，应当承担继续履行、采取补救措施或者赔偿损失等违约责任。\\n综上所述，被告无视其制订的所谓《微博投诉操作细则》，在未履行事先告知义务的情况下直接粗暴停止了原告的账号服务，侵犯了原告的数据财产权益。被告应向原告具体指出其封禁做法的理由，是由于哪条内容执行的封禁，详细解释其处罚原因的逻辑链条；如果其理由切实成立，也应该依照其制订的所谓《微博投诉操作细则》，由删除内容或禁言48小时开始处罚。因此，原告要求被告恢复其微博账号“Jon_Showing”（UID：1444146297）的所有功能，并赔礼道歉。\"}"))
dataList.append(encode('--'+boundary+'--'))
dataList.append(encode(''))
body = b'\r\n'.join(dataList)
payload = body
headers = {
  'X-Token': 'OGY3Y2ZlYzIwMjBiNDBiZTlkMmRhZmNhZjA4M2U4MDY=',
  'Cookie': 'wzws_sessionid=gDEyMy4xMTQuMTAwLjI0gjBiMDBkZIEwOGM4NmGgZBB2GA==',
  'Content-type': 'multipart/form-data; boundary={}'.format(boundary)
}
conn.request("POST", "/complainInfoController/saveComplaintInfo", payload, headers)
res = conn.getresponse()
data = res.read()
decoded = data.decode("utf-8")
data_json = json.loads(decoded)
code = data_json['code']
with open('weibo_status.txt', 'w+') as f:
    f.write(data_json['message'])
