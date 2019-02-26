# -*- coding:utf-8 -*-

import itchat
import urllib.request
import json

itchat.auto_login(hotReload=True) 

#小冰的微信username
MapName = '@40ac8c5b82141cb51f50d05b78f0ef75'
#保存发送人微信UserName
global My_USER_NAME
My_USER_NAME = ''

#给公众号发送消息
def send_gzh(str):
	#返回完整的公众号列表
	mps = itchat.get_mps()
	#按公众号名称查找,返回为列表
	mps = itchat.search_mps(name='小冰')
	#发送方法和上面一样
	userName = mps[0]['UserName']
	itchat.send(str,toUserName = userName)

#获取聊天机器人接口返回数据
def get_reply_text(str):
	# 发送到web服务器的表单数据
	formdata = {
	"key" : "free",
	"appid" : "0",
	"msg" : str
	}

	#使用青云客智能聊天机器人API：http://api.qingyunke.com/，没有微软小冰好用
	url = "http://api.qingyunke.com/api.php?"

	# 经过urlencode转码
	params = urllib.parse.urlencode(formdata)
	response =urllib.request.urlopen(url + params)
	jsonData = response.read();

	#print(json.loads(jsonData)['content'])
	return json.loads(jsonData)['content']

#添加isMpChat=True 接收公众号信息 	
@itchat.msg_register(itchat.content.TEXT, isMpChat=True)
def get_gzh_text(msg):
    global My_USER_NAME
    print('%s: %s' % (msg['Type'], msg['Text']), msg['FromUserName'])	
	#return msg['Text']
    #itchat.send(msg['Text'],toUserName = My_USER_NAME)
    print("保存的username"+ My_USER_NAME)
    itchat.send(msg['Text'], My_USER_NAME)
    #return msg['Text'] 如果return消息内容将会和公众号一直聊天

#接收好友消息
@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
	# msg.text这是接收到的信息，send自定义发送内容
	# msg.user.send("小新智能机器人自动回复:" + msg.text)
	print("接收到的消息:" + msg['FromUserName'])
	replyText = ''
	#方式一：通过接口获取数据
	''' 
		replyText = get_reply_text(str = msg.text)
		msg.user.send("小新智能机器人自动回复:\n 上班时间将由智能机器人自动给您回复，如有急事请及时电话联系！" + replyText)
	'''
	
	#方式二：通过微软小冰获取数据,属于异步消息
	send_gzh(str = msg.text)
	#replyText = get_gzh_text(msg)
	print("接收到的消息:replyText" + replyText)
	global My_USER_NAME
	My_USER_NAME = msg['FromUserName']
	msg.user.send("小新智能机器人自动回复:\n 上班时间将由智能机器人自动给您回复，如有急事请及时电话联系！")
	print("智能回复消息:" + msg.text)
	print("---------------------------------------------")
    # return msg.text

#itchat.auto_login()
itchat.run()

''' 
python 微信智能聊天机器人流程

	方案一:
	a.接收发送人消息、username等内容，保存username到全局变量
	b.吧接收到的内容发送给小冰
	c.接收小冰返回的消息，转发到好友
	注意:普通开发者足够使用，未做压力测试，消息太多可能会串发消息，需要修改把My_USER_NAME修改成队列
	
	方案二:
	a.接收发送人消息、username等内容，
	b.调用接口，解析数据
	c.转发到好友

'''

