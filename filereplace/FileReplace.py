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

		if self.quote_redis != None:
			for single in self.trading:
				self.config_content_dict['redis_server_quote_group'][single] = [self.quote_redis, 6379, ""]

		self.close_new_file(settings.post_mc)

	def deal(self):
		self.config_content_dict = self.open_file(settings.deal)

		# for single in self.trading:
		# 	if len(self.trading) < 1:
		# 		self.config_content_dict['market_list'] = single
		# 	else:
		# 		self.config_content_dict['market_list'].append(single)
		self.market_list(self.trading)
		self.redis_change()
		# if self.deal_redis != None:
		# 	self.config_content_dict['redis_server_address_deal'] = self.deal_redis
		
		self.close_new_file(settings.deal)

	def quote(self):
		self.config_content_dict = self.open_file(settings.quote)

		for single in self.trading:
			if len(self.trading) < 1:
				self.config_content_dict['market_list'] = single
			else:
				self.config_content_dict['market_list'].append(single)

		if self.deal_redis != None:
			self.config_content_dict['redis_server_address_deal'] = self.deal_redis
		if self.quote_redis != None:
			self.config_content_dict['redis_server_address_quote'] = self.quote_redis

		self.close_new_file(settings.quote)

	def guard(self):
		self.config_content_dict = self.open_file(settings.guard)

		for single in self.trading:
			if len(self.trading) < 1:
				self.config_content_dict['market_list'] = single
			else:
				self.config_content_dict['market_list'].append(single)


	def market_list(self,trading):
		for single in self.trading:
			if len(self.trading) < 1:
				self.config_content_dict['market_list'] = single
			else:
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
			

obj = ConfigureInitial(['BTCZX','ETHZX'],'10.10.01.1','123','192.168.10.1','8.8.8.8')
# obj.gw_rest()
# obj.post_mc()
obj.deal()
# obj.quote()