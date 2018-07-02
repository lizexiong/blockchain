# -*- coding:utf-8 -*-


import json
import settings
import subprocess

class ConfigureInitial(object):
	def __init__(self,trading,guard_ip,guard_port, quote_address=None,deal_address=None,mysql_address=None,):
		self.trading = trading
		self.guard_ip = guard_ip
		self.guard_port = guard_port
		self.quote_redis = quote_address
		self.deal_redis = deal_address
		self.mysql_address = mysql_address
		self.config_content_dict = ""


	def open_file(self,configfile):
		self.configcontent = open(configfile)
		config_content_dict = json.loads(self.configcontent.read())
		return config_content_dict

	def gw_rest(self):
		self.config_content_dict = self.open_file(settings.gw_rest)

		self.config_content_dict['market_list'].extend(self.trading)

		if self.quote_redis != None:
			for single in self.trading:
				self.config_content_dict['redis_server_quote_group'][single] = [[self.quote_redis,6379,""],[self.quote_redis,6379,""]]
				self.config_content_dict['guard_servers'][single] = "tcp://" + self.guard_ip + ":"  + self.guard_port
		if self.deal_redis != None:
				self.config_content_dict['redis_server_quote_group'][single] = [[self.quote_redis,6379,""],[self.quote_redis,6379,""]]

		self.close_new_file(settings.gw_rest)

	def post_mc(self):
		self.config_content_dict = self.open_file(settings.post_mc)

		self.config_content_dict['redis_server_quote_group'].clear()
		if self.quote_redis != None:
			for single in self.trading:
				self.config_content_dict['redis_server_quote_group'][single] = [self.quote_redis, 6379, ""]

		self.close_new_file(settings.post_mc)

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

	def market_list(self,):

		del self.config_content_dict['market_list'][:]
		for single in self.trading:
			self.config_content_dict['market_list'].append(single)

	def redis_change(self,):
		if self.deal_redis != None:
			self.config_content_dict['redis_server_address_deal'] = self.deal_redis
		if self.quote_redis != None:
			self.config_content_dict['redis_server_address_quote'] = self.quote_redis

	def close_new_file(self,configfile):
		new_file = open(configfile + ".txt" ,'w+')
		new_file.write(json.dumps(self.config_content_dict,sort_keys=True, indent=4,))
		self.configcontent.close()
			

obj = ConfigureInitial(['AAAAAA','BBBBBB'],'1.1.1.1','8888','2.2.2.2',)
obj.gw_rest()
obj.post_mc()
obj.quote()
obj.guard()