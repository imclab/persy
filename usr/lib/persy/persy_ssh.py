#!/usr/bin/env python
# -*- coding: utf-8 -*-

#License
#=======
#persy is free software: you can redistribute it and/or modify it
#under the terms of the GNU General Public License as published by the Free
#Software Foundation, either version 2 of the License, or (at your option) any
#later version.

#persy is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with persy; if not, write to the Free Software
#Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


try:
	import gettext
	#localizations
	LOCALEDIR='/usr/lib/persy/locale'
	#init the localisation
	gettext.install("messages", LOCALEDIR)
except Exception as e:
	print "I have problems initializing the translations (gettext). Will use plain english instead"
	print str(e)

	#check if the _ function is initialized, if not, do a fallback!
	if not _:
		def _(msg):
			"""fallback-function if the original function did not initialize propperly"""
			return msg

try:
	import paramiko
	import os
except ImportError as e:
	print _("You do not have all the dependencies:")
	print str(e)
	sys.exit(1)
except Exception as e:
	print _("An error occured when initialising one of the dependencies!")
	print str(e)
	sys.exit(1)

__author__ = "Dennis Schwertel"
__copyright__ = "Copyright (C) 2009, 2010 Dennis Schwertel"



class PersySSH():
	'''Functions that might be helpful for ssh stuff'''
	def __init__(self, config, log):
		self.config = config
		self.log = log

	def checkSSHAuth(self):
		username=None
		port=22
		client = paramiko.SSHClient()
		client.load_system_host_keys()
		try:
			client.connect(self.config['remote']['hostname'], username=username, port=port)
		except paramiko.PasswordRequiredException as e:
			return False
		except Exception as e:
			return False
		return True

	def localSSHKeysExist(self):
		'''checks if local ssh keys are generated'''
		if not os.path.exists(os.path.join(self.config.getAttribute('LOCALSSHDIR'), 'id_rsa')) and not os.path.exists(os.path.join(self.config.getAttribute('LOCALSSHDIR'), 'id_rsa.pub')):
			return False
		return True


	def createLocalSSHKeys(self, password):
		''' create the local keys '''
		#create public and private keys
		if not os.path.exists(self.config.getAttribute('LOCALSSHDIR')):
			os.makedirs(self.config.getAttribute('LOCALSSHDIR'))
			os.chmod(self.config.getAttribute('LOCALSSHDIR'), 700)

		if not self.localSSHKeysExist():
			callcmd.append('ssh-keygen')
			callcmd.append('-q')
			callcmd.append("-p %s"%password)
			callcmd.append('-f')
			callcmd.append(os.path.join(self.config.getAttribute('LOCALSSHDIR'), 'id_rsa'))
			callcmd.append('-t rsa')
			p = subprocess2.Subprocess2(callcmd)
			os.chmod(os.path.join(self.config.getAttribute('LOCALSSHDIR'), 'id_rsa'), 700)
			os.chmod(os.path.join(self.config.getAttribute('LOCALSSHDIR'), 'id_rsa.pub'), 700)

	def checkRemoteServer(self):
		client = paramiko.SSHClient()
		client.load_system_host_keys()
		try:
			client.connect(self.config['remote']['hostname'])
			stdin1, stdout1, stderr1 = client.exec_command("cd %s && git show" % self.config['remote']['path'])
			stdin1.close()
			client.close()
			if stderr1:
				err = stderr1.read()
				#if something is actually in err
				if not err == '':
					self.log.critical(err)
					return False
		except paramiko.PasswordRequiredException as e:
			self.log.critical(str(e))
			return False
		except Exception as e:
			self.log.critical(str(e))
			return False
		return True

