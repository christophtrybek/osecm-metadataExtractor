#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Mar 17, 2015

@author: tim
'''
import logging
import swiftclient
import io
from tim.swift.SwiftConfig import swift_url, swift_user, swift_pw

class SwiftBackend(object):
	'''
	classdocs
	'''
	
	def __init__(self):
		'''
		Constructor
		'''
		self.log = logging.getLogger(__name__)
		self.log.debug('initializing...')
		self.authurl = swift_url
		self.user = swift_user
		self.key = swift_pw
		self.swiftC = None
		
		self._assertConnection()
###############################################################################
###############################################################################

	def _getConnection(self):
		return swiftclient.client.Connection(authurl=self.authurl, user=self.user, key=self.key, retries=1, insecure='true')
	
	def _createConnection(self):
		self.log.debug('establishing NEW connection')
		self.swiftC = self._getConnection()
		
	def _verifyConnection(self):
		try:
			self.swiftC.get_auth()
		except:
			return False
		return True
		
	def _assertConnection(self):
		self.log.debug('asserting connection')

		if (not self._verifyConnection()):
			self._createConnection()
			if (not self._verifyConnection()):
				self.log.error('SWIFT connection could not be established')
				raise Exception('SWIFT connection could not be established')
		self.log.debug('connection OK')
			
			
###############################################################################
###############################################################################		  
			
	def printStatus(self):
		self.log.info('status: ') 
		
	def putObject(self, container, name, dataObject):
		self.log.debug('putting file to swift: {}'.format(name))
		self._assertConnection()
		rsp = dict()
		self.swiftC.put_object(container=container, obj=name, contents=dataObject, response_dict=rsp)
		# self.log.debug(rsp)
		
	def getObject(self, container, name):
		self.log.debug('getting file from swift: {}'.format(name))
		self._assertConnection()
		rsp = dict()
		t = self.swiftC.get_object(container=container, obj=name, resp_chunk_size=None, query_string=None, response_dict=rsp, headers=None)
		o = io.BytesIO(t[1])
		# self.log.debug(rsp)
		return o
	
	def deleteObject(self, container, name):
		self.log.debug('deleting file from swift: {}'.format(name))
		self._assertConnection()
		rsp = dict()
		self.swiftC.delete_object(container=container, obj=name, query_string=None, response_dict=rsp)
		
		
		
###############################################################################
###############################################################################			
		
		
		
		
	# Retrieves list of all objects of the specified container
	#@exception_wrapper(404, "requested resource does not exist", log)
	def get_object_list(self, container_name, limit=None, marker=None, prefix=None):
		self.log.debug("Retrieving list of all objects of container: {} with parameter: limit = {}, marker = {}, prefix = {}"
				.format(container_name, limit, marker, prefix))
		self._assertConnection()
		full_listing = limit is None  # bypass default limit of 10.000 of swift-client
		files = self.swiftC.get_container(
			container_name, marker=marker, limit=limit, prefix=prefix,
			full_listing=full_listing)
		return files[1]
	
	
	
			
