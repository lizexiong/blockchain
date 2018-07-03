# -*- coding:utf-8 -*-

import os
import json
import settings
import subprocess
import traceback	#函数调用者

class ConfigureInitial(object):
	def __init__(self,trading,guard_ip,guard_port, quote_address=None,deal_address=None,mysql_address=None,env='other'):
		self.trading = trading
		self.guard_ip = guard_ip
		self.guard_port = guard_port
		self.quote_redis = quote_address
		self.deal_redis = deal_address
		self.mysql_address = mysql_address
		self.env = env
		self.config_content_dict = ""

	def open_file(self,configfile):
		self.configcontent = open(configfile)
		config_content_dict = json.loads(self.configcontent.read())
		return config_content_dict

	def gw_rest(self):
		if self.env == "gw":
			self.config_content_dict = self.open_file(settings.gw_rest_path + settings.gw_rest)
		else:
			self.config_content_dict = self.open_file(settings.gw_rest)

		self.config_content_dict['market_list'].extend(self.trading)

		if self.guard_ip or self.guard_port:
			for single in self.trading:
				self.config_content_dict['guard_servers'][single] = "tcp://" + self.guard_ip + ":"  + self.guard_port

		self.gw_redis()

		self.close_new_file(settings.gw_rest)

	def post_mc_trade(self):
		self.config_content_dict = self.open_file(settings.post_mc_trade)

		self.config_content_dict['redis_server_quote_group'].clear()

		self.gw_redis()

		self.close_new_file(settings.post_mc_trade)

	def deal(self):
		self.config_content_dict = self.open_file(settings.deal)

		self.market_list()
		self.redis_change()

		self.close_new_file(settings.deal)

	def quote(self):
		self.config_content_dict = self.open_file(settings.quote)

		self.market_list()
		self.redis_change()

		self.close_new_file(settings.quote)

	def guard(self):
		self.config_content_dict = self.open_file(settings.guard)

		self.market_list()
		self.redis_change()

		self.config_content_dict['server_endpoint'] = "tcp://*:" + self.guard_port

		self.close_new_file(settings.guard)

	def swirlyd(self):
		self.config_content_dict = self.open_file(settings.swirlyd)

		self.market_list()
		self.redis_change()

		self.close_new_file(settings.swirlyd)


	def market_list(self,):

		del self.config_content_dict['market_list'][:]
		for single in self.trading:
			self.config_content_dict['market_list'].append(single)

	def redis_change(self,):
		caller = traceback.extract_stack()[0][3].split(".")[1].split('(')[0]		#获取哪个对象在调用
		if  caller in ['deal','swirlyd','quote']:
			if self.deal_redis != None:
				self.config_content_dict['redis_server_address_deal'] = self.deal_redis

		if caller in ['swirlyd', 'quote']:
			if self.quote_redis != None:
				self.config_content_dict['redis_server_address_quote'] = self.quote_redis

	def gw_redis(self):
		for single in self.trading:
			if self.quote_redis != None:
				self.config_content_dict['redis_server_quote_group'][single] = [[self.quote_redis,6379,""],[self.quote_redis,6379,""]]
			else:
				self.config_content_dict['redis_server_quote_group'][single] = [[settings.quote_redis,6379,""],[settings.quote_redis,6379,""]]

	def close_new_file(self,configfile):
		new_file = open(configfile.split('.')[0] + ".txt" ,'w+')
		new_file.write(json.dumps(self.config_content_dict,sort_keys=True, indent=4,))
		self.configcontent.close()


	def shell_handler(self,):

		if not os.path.exists("/backup"):
			subprocess.call("sudo mkdir /backup",shell=True)
		try:
			subprocess.call("mkdir /backup/`date '+%Y%m%d-%H:%M'`",shell=True)

			if self.env ==  'other':
				subprocess.call("mv %s %s %s %s   -t /backup/`date '+%%Y%%m%%d-%%H:%%M'`" %(settings.quote, settings.deal,\
																						 settings.guard,settings.swirlyd,) ,shell=True)
				subprocess.call("mv guard.txt %s" %(settings.guard),shell=True)
				subprocess.call("mv quote.txt %s" %(settings.quote),shell=True)
				subprocess.call("mv deal.txt %s" %(settings.deal),shell=True)
				subprocess.call("mv swirlyd.txt %s" %(settings.swirlyd),shell=True)
			elif self.env == "gw":
				subprocess.call("mv %s%s   -t /backup/`date '+%%Y%%m%%d-%%H:%%M'`" %(settings.gw_rest_path,settings.gw_rest,) ,shell=True)
				subprocess.call("mv gw-rest.txt %s%s" %(settings.gw_rest_path,settings.gw_rest),shell=True)
			elif self.env == "test":
				subprocess.call("mv %s %s %s %s %s %s%s  -t /backup/`date '+%%Y%%m%%d-%%H:%%M'`" %(settings.quote, settings.deal,\
																						 settings.guard,settings.swirlyd,settings.gw_rest,\
																								   settings.test_post_mc_trade_path,settings.post_mc_trade) ,shell=True)
				subprocess.call("mv guard.txt %s" %(settings.guard),shell=True)
				subprocess.call("mv quote.txt %s" %(settings.quote),shell=True)
				subprocess.call("mv deal.txt %s" %(settings.deal),shell=True)
				subprocess.call("mv swirlyd.txt %s" %(settings.swirlyd),shell=True)
				subprocess.call("mv %spost-mc.txt %s"%(settings.test_post_mc_trade_path,settings.post_mc_trade),shell=True)
				subprocess.call("mv gw-rest.txt %s" %(settings.gw_rest),shell=True)
		except Exception as e:
			print ("File Error:",str(e))


obj = ConfigureInitial(['AAAAAA','BBBBBB'],'1.1.1.1','8888','2.2.2.2','3.3.3.3',env='gw')
obj.gw_rest()
# obj.post_mc_trade()
# obj.quote()
# obj.guard()
# obj.swirlyd()
# obj.deal()
obj.shell_handler()