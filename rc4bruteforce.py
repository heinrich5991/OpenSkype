#!/usr/bin/python

from FluxCapacitor import Seed, Skype_RC4_Expand_IV, skype_crc, RC4_Context, RC4_crypt
from utils import *
import sys

class Rambo:
	def __init__(self, cipher_hex, crc):
		self.cipher = hexstr2bytestr(cipher_hex)
		self.crc = crc

	def crack(self, start=0x00000000, stop=0xFFFFFFFF):
		finalseed = start

		last_write = 0
		crc_correct = False
		give_up = False

		while (not crc_correct) and (not give_up):
			rc4context = RC4_Context()
			Skype_RC4_Expand_IV(finalseed, rc4context)
			plaintext = RC4_crypt(self.cipher, rc4context)
			crc = long2hex(skype_crc(plaintext))
			crc_correct = crc == self.crc
			if not crc_correct:
				if finalseed < stop:
					finalseed += 1
					if finalseed-last_write > 10000:
						open('currentfinalseed','w').write(long2hex(finalseed))
						print long2hex(finalseed)
						last_write = finalseed
				else:
					open('currentfinalseed','w').write(long2hex(finalseed))
					print 'tried all keys without success. giving up ...'
					give_up = True
				
		if not give_up:
			print long2hex(finalseed)+' - cracked'
#			print '\tcrc:\t'+crc
#			print '\tplaintext:\n\t\t'+str2hex(plaintext)
#			open('finalseed','w').write(long2hex(finalseed))
			return plaintext

if __name__ == '__main__':

#	bruteforce = Rambo(cipher_hex = 'ca5f4abe629bebf39df2152facca17', crc = 'b0a81c91') # PAYLOAD; correct finalseed=0x768df200
#	bruteforce = Rambo(cipher_hex = 'dccb580bc50d5f944fbf65f5671dd2', crc = 'b0a81c91') # RESEND; false positive @ 0x202ec8b5

	bruteforce = Rambo(cipher_hex = 'f5017ed1b028a803d1d98d3697d69ec0043c99f00c141dd6e28098e2dcc0c38db442a49fd5bc4b96cc42aa176542743845412c4bc2ab0411f21f52936c702e499648d43d3a0679fb', crc = '75012AAF')

	if sys.argv[1] == '0':
		bruteforce.crack(start = 0x00000000, stop = 0x40000000)
	elif sys.argv[1] == '1':
		bruteforce.crack(start = 0x40000000, stop = 0x80000000)


