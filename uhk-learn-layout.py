#! /usr/bin/python3
# encoding: utf-8
#

import argparse
#from inputimeout import inputimeout
#import json
#from functools import reduce, partial
#import copy
import re
#import os
import sys
#from datetime import datetime
#from enum import Enum, auto	

# def timedinput():
# 	try:
# 		s= inputimeout(timeout= 5)
# 	except Exception:
# 		return None
# 	if args.debug:
# 		print("read: '"+s+"'")
# 	return s

class Keymap:
	def __init__(self):
		self.keymap= {}		# a list of layers

	def add(self, keyid, keychar, layer):
		if not layer in self.keymap:
			self.keymap[layer]= {}
		if args.debug:
			print(f"adding keyid {keyid} char '{keychar}' to layer '{layer}'")
		self.keymap[layer][int(keyid)]= keychar

	def layers(self):
		return self.keymap.keys

	def getlayer(self, layer):
		return self.keymap[layer] if layer in self.keymap else None

def showkeyrow(row, base, shift, altgr, ids):
	if altgr==None:
		multiplier= 9 if not args.compact else 8
	else:
		multiplier= 11 if not args.compact else 9
	print(f"R{row}: ", end='')
	if row>1 and row<4:
		print(' '*multiplier, end='')
	for i in ids:
		if i not in base or i not in shift:
			continue
		if altgr==None:
			if args.compact:
				print(f" [ {base[i]:1.1}{shift[i]:1.1} ] ", end='')
			else:
				print(f" [ {base[i]:1.1}/{shift[i]:1.1} ] ", end='')
		else:
			if args.compact:
				print(f" [ {base[i]:1.1}{shift[i]:1.1}{altgr[i]:1.1} ] ", end='')
			else:
				print(f" [ {base[i]:1.1}/{shift[i]:1.1}/{altgr[i]:1.1} ] ", end='')
	print("")

def generateoutput(keymap):
	base= keymap.getlayer('-')
	shift= keymap.getlayer('+')
	altgr= keymap.getlayer('*')

	showkeyrow(1, base, shift, altgr, ( 64, 65, 66, 67, 68, 69, 70, 0, 1, 2, 3, 4, 5 ))
	showkeyrow(2, base, shift, altgr, ( 72, 73, 74, 75, 77, 14, 7, 8, 9, 10, 11, 12, 13 ))
	showkeyrow(3, base, shift, altgr, ( 79, 80, 81, 82, 84, 21, 15, 16, 17, 18, 19 ))
	showkeyrow(4, base, shift, altgr, ( 86, 87, 88, 89, 90, 91, 22, 23, 24, 25, 26 ))

def generatecanonicalmapid(keymap):
	base= keymap.getlayer('-')
	shift= keymap.getlayer('+')
	altgr= keymap.getlayer('*')

	ids= ( 64, 65, 66, 67, 68, 69, 70, 0, 1, 2, 3, 4, 5, 
		   72, 73, 74, 75, 77, 14, 7, 8, 9, 10, 11, 12, 13,
		   79, 80, 81, 82, 84, 21, 15, 16, 17, 18, 19,
		   86, 87, 88, 89, 90, 91, 22, 23, 24, 25, 26 )

	s_noaltgr= '/'.join(map(lambda i: f"{base[i]:1.1}{shift[i]:1.1}", ids))
	if args.printcanonical:
		print(s_noaltgr)

	if altgr:
		s_altgr= '/'.join(map(lambda i: f"{base[i]:1.1}{shift[i]:1.1}{altgr[i]:1.1}", ids))
		if args.printcanonical:
			print(s_altgr)
		s= s_altgr
	else:
		s= s_noaltgr

	return s

canonicalstrings= {
	"DE-International": '''^° /1! /2"²/3§³/4$ /5% /6& /7/{/8([/9)]/0=}/ß?\/´` /qQ@/wW /eE€/rR /tT /zZ /uU /iI /oO /pP /üÜ /+*~/#' /aA /sS /dD /fF /gG /hH /jJ /kK /lL /öÖ /äÄ /<>|/yY /xX /cC /vV /bB /nN /mMµ/,; /.: /-_ ''',
	"DE": '''^°/1!/2"/3§/4$/5%/6&/7//8(/9)/0=/ß?/´`/qQ/wW/eE/rR/tT/zZ/uU/iI/oO/pP/üÜ/+*/#'/aA/sS/dD/fF/gG/hH/jJ/kK/lL/öÖ/äÄ/<>/yY/xX/cC/vV/bB/nN/mM/,;/.:/-_''',
	"US": '''`~/1!/2@/3#/4$/5%/6^/7&/8*/9(/0)/-_/=+/qQ/wW/eE/rR/tT/yY/uU/iI/oO/pP/[{/]}/\|/aA/sS/dD/fF/gG/hH/jJ/kK/lL/;:/'"/\|/zZ/xX/cC/vV/bB/nN/mM/,</.>//?''',
	"US-noAltGr": '''`~`/1!1/2@2/3#3/4$4/5%5/6^6/7&7/8*8/9(9/0)0/-_-/=+=/qQq/wWw/eEe/rRr/tTt/yYy/uUu/iIi/oOo/pPp/[{[/]}]/\|\/aAa/sSs/dDd/fFf/gGg/hHh/jJj/kKk/lLl/;:;/'"'/\|\/zZz/xXx/cCc/vVv/bBb/nNn/mMm/,<,/.>.//?/''',
	"US-International": '''`~ /1!¡/2@²/3#³/4$¤/5%€/6^¼/7&½/8*¾/9(‘/0)’/-_¥/=+×/qQä/wWå/eEé/rR®/tTþ/yYü/uUú/iIí/oOó/pPö/[{«/]}»/\|¬/aAá/sSß/dDð/fF /gG /hH /jJ /kK /lLø/;:¶/'"´/\| /zZæ/xX /cC©/vV /bB /nNñ/mMµ/,<ç/.> //?¿''',
	"US-Colemak-International": '''`~~/1!¡/2@º/3#ª/4$¢/5%€/6^ħ/7&ð/8*þ/9(‘/0)’/-_–/=+×/qQä/wWå/fFã/pPø/gG˛/jJđ/lLł/uUú/yYü/;:ö/[{«/]}»/\|*/aAá/rR`/sSß/tT´/dD¨/hHˇ/nNñ/eEé/iIí/oOó/'"õ/-_–/zZæ/xX^/cCç/vVœ/bB˘/kK˚/mM¯/,<¸/.>˙//?¿''',
	"US-Colemak": '''`~/1!/2@/3#/4$/5%/6^/7&/8*/9(/0)/-_/=+/qQ/wW/fF/pP/gG/jJ/lL/uU/yY/;:/[{/]}/\|/aA/rR/sS/tT/dD/hH/nN/eE/iI/oO/'"/-_/zZ/xX/cC/vV/bB/kK/mM/,</.>//?''',
	"US-Dvorak": '''`~/1!/2@/3#/4$/5%/6^/7&/8*/9(/0)/[{/]}/'"/,</.>/pP/yY/fF/gG/cC/rR/lL//?/=+/\|/aA/oO/eE/uU/iI/dD/hH/tT/nN/sS/-_/\|/;:/qQ/jJ/kK/xX/bB/mM/wW/vV/zZ''',
	"US-Dvorak-noAltGr":
	'''`~`/1!1/2@2/3#3/4$4/5%5/6^6/7&7/8*8/9(9/0)0/[{[/]}]/'"'/,<,/.>./pPp/yYy/fFf/gGg/cCc/rRr/lLl//?//=+=/\|\/aAa/oOo/eEe/uUu/iIi/dDd/hHh/tTt/nNn/sSs/-_-/\|\/;:;/qQq/jJj/kKk/xXx/bBb/mMm/wWw/vVv/zZz''',
	"UK": '''`¬/1!/2"/3£/4$/5%/6^/7&/8*/9(/0)/-_/=+/qQ/wW/eE/rR/tT/yY/uU/iI/oO/pP/[{/]}/#~/aA/sS/dD/fF/gG/hH/jJ/kK/lL/;:/'@/\|/zZ/xX/cC/vV/bB/nN/mM/,</.>//?''',
	"UK-International": '''`¬¦/1! /2" /3£ /4$€/5% /6^ /7& /8* /9( /0) /-_ /=+ /qQ /wW /eEé/rR /tT /yY /uUú/iIí/oOó/pP /[{ /]} /#~\/aAá/sS /dD /fF /gG /hH /jJ /kK /lL /;: /'@ /\| /zZ /xX /cC /vV /bB /nN /mM /,< /.> //? '''
}

def canonicaltomapname(canstring):
	for name, canonical in canonicalstrings.items():
		if canonical == canstring:
			return name
	return None

def processline(line, keymap):
	res= re.match(r"^\-(?P<layer>[\+\-\*])(?P<keyid>[0-9]+)\-(?P<keychar>[^ ]*)(?P<spaces>.*)$", line)
	if res:
		keymap.add(res.group('keyid'), res.group('keychar'), res.group('layer'))
		return True
	if re.match(r"^\-\-\-\-\- ", line):
		return False
	return None

def main():
	global args

	parser= argparse.ArgumentParser(description='determine the host layout from the output of the "learn_layout" macro run on a UHK')
	parser.add_argument('--debug', dest='debug', action='store_true', default=False, 
						help='show debugging information for developers')
	parser.add_argument('--generate-macro', dest='macro', action='store_true', default=False, 
						help='generate learn_hostmap macro for UHK Agent. Paste the generated macro code into a macro command, and bind it to a key. Execute the macro (by tapping the key), and feed the output into this script to learn the host keymap.')
	parser.add_argument('--use-altgr', dest='usealtgr', action='store_true', default=False, 
						help='use AltGr combinations in macro (in addition to standard keypress and shift-keypress)')
	parser.add_argument('--macrodelay', dest='macrodelay', action='store_true', default=False,
						help='insert delays into the macro (so it runs a bit slower)')
	parser.add_argument('--print-canonical', dest='printcanonical', action='store_true', default=False, 
						help='print the canoncial string(s) for this keymap')
	parser.add_argument('--canonical', dest='canonical', action='store_true', default=False, 
						help='show the canonical name for this keymap')
	parser.add_argument('--showmap', dest='showmap', action='store_true', default=False, 
						help='show the keyboard layout')
	parser.add_argument('--compact', dest='compact', action='store_true', default=False, 
						help='show a compact version of the keyboard layout')
	parser.add_argument('--input', dest='inputfile', action='store', default=None, 
						help='read input from this file')

	args= parser.parse_args()

	if not args.canonical and not args.showmap:
		args.showmap= True

	if args.macro:
		printMacro()
		return

	if args.debug:
		print('Debug output will be generated.')
	
	if args.debug:
		print('Starting to read input...')

	running= True
	keymap= Keymap()

	if args.inputfile:
		file= open(args.inputfile, 'r', encoding= 'utf-8')
	else:
		file= sys.stdin

	for line in file:
		if processline(line, keymap)==False:
			break

	if args.debug:
		print('done reading input.')

	file.close()

	if args.canonical:
		canstring= generatecanonicalmapid(keymap)
		name= canonicaltomapname(canstring)
		if name:
			print("Canonical keymap name: "+name)

	if args.showmap:
		generateoutput(keymap)

def spacedNumber(num):
	if args.debug:
		for c in str(num):
			print("char: "+c)
		
	return ' '.join(list(str(num)))

def printMacro():
	if args.macrodelay:
		print("setReg 0 100")
	print("tapKeySeq keypadPlus keypadPlus keypadPlus keypadPlus keypadPlus space B E G I N space keypadPlus keypadPlus keypadPlus keypadPlus keypadPlus space space enter")
	if args.macrodelay:
		print("delayUntil #0")
	for k_pair in (
		( 64, 'graveAccentAndTilde' ),
		( 65, '1' ),
		( 66, '2' ),
		( 67, '3' ),
		( 68, '4' ),
		( 69, '5' ),
		( 70, '6' ),
		( 0, '7' ),
		( 1, '8' ),
		( 2, '9' ),
		( 3, '0' ),
		( 4, 'minusAndUnderscore' ),
		( 5, 'equalAndPlus' ),
		( 72, 'q' ),
		( 73, 'w' ),
		( 74, 'e' ),
		( 75, 'r' ),
		( 77, 't' ),
		( 14, 'y' ),
		( 7, 'u' ),
		( 8, 'i' ),
		( 9, 'o' ),
		( 10, 'p' ),
		( 11, 'openingBracketAndOpeningBrace' ),
		( 12, 'closingBracketAndClosingBrace' ),
		( 13, 'backslashAndPipe' ),
		( 79, 'a' ),
		( 80, 's' ),
		( 81, 'd' ),
		( 82, 'f' ),
		( 84, 'g' ),
		( 21, 'h' ),
		( 15, 'j' ),
		( 16, 'k' ),
		( 17, 'l' ),
		( 18, 'semicolonAndColon' ),
		( 19, 'apostropheAndQuote' ),
		( 86, 'backslashAndPipeIso' ),
		( 87, 'z' ),
		( 88, 'x' ),
		( 89, 'c' ),
		( 90, 'v' ),
		( 91, 'b' ),
		( 22, 'n' ),
		( 23, 'm' ),
		( 24, 'commaAndLessThanSign' ),
		( 25, 'dotAndGreaterThanSign' ),
		( 26, 'slashAndQuestionMark' )
	):
		( k_id, k_name ) = k_pair
		print("tapKeySeq keypadMinus keypadMinus "+spacedNumber(k_id)+" keypadMinus "+k_name+" space space enter")
		print("tapKeySeq keypadMinus keypadPlus "+spacedNumber(k_id)+" keypadMinus LS-"+k_name+" space space enter")
		if args.usealtgr:
			print("tapKeySeq keypadMinus keypadAsterisk "+spacedNumber(k_id)+" keypadMinus RA-"+k_name+" space space enter")
			print("tapKeySeq keypadMinus keypadSlash "+spacedNumber(k_id)+" keypadMinus RAS-"+k_name+" space space enter")
		if args.macrodelay:
			print("delayUntil #0")

	print("tapKeySeq keypadMinus keypadMinus keypadMinus keypadMinus keypadMinus space E N D space keypadMinus keypadMinus keypadMinus keypadMinus keypadMinus space space enter")

if __name__ == '__main__':
	main()
