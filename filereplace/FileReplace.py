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


		self._gw_rest = settings.gw_rest
		self._post_mc = settings.post_mc
		self._post_mc_trade = settings.post_mc_trade
		self._deal = settings.deal
		self._guard = settings.guard
		self._quote = settings.quote
		self._swirlyd = settings.swirlyd

	# def open_file(self,configfile):
	# 	return open(configfile)
    #
	# def close_file(self,configfile):
	# 	self.open_file()

	def gw_rest(self):
		configcontent = open(self._gw_rest,'r+')

		self.config_content_dict = json.loads(configcontent.read(),)
		self.config_content_dict['market_list'].extend(self.trading)

		if self.quote_redis != None:
			for single in self.trading:
				self.config_content_dict['redis_server_quote_group'][single] = [[self.quote_redis,6379,""],[self.quote_redis,6379,""]]
				self.config_content_dict['guard_servers'][single] = "tcp://" + self.guard_ip + ":"  + self.guard_port
		if self.deal_redis != None:
				self.config_content_dict['redis_server_quote_group'][single] = [[self.quote_redis,6379,""],[self.quote_redis,6379,""]]

		self.close_new_file(self._gw_rest)
		configcontent.close()



	def post_mc(self):

		configcontent = open(self._post_mc,'r+')

		self.config_content_dict = json.loads(configcontent.read(),)

		if self.quote_redis != None:
			for single in self.trading:
				self.config_content_dict['redis_server_quote_group'][single] = [self.quote_redis, 6379, ""]

		self.close_new_file(self._post_mc)
		configcontent.close()

	def deal(self):
		configcontent = open(self._deal,'r+')

		self.config_content_dict = json.loads(configcontent.read())

		





	def close_new_file(self,configfile):
		new_file = open(configfile + ".txt" ,'w+')
		new_file.write(json.dumps(self.config_content_dict,sort_keys=True, indent=4,))

			


obj = ConfigureInitial(['BTCZX','ETHZX'],'10.10.01.1','123','192.168.10.1')
obj.gw_rest()
obj.post_mc()