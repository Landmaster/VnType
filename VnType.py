from tkinter import *
from tkinter import scrolledtext
import sys
import os

#helper to make frame
def makeframe(master, side='top', expand=1, fill='both', **kwargs):
	frm=Frame(master)
	frm.pack(side=side, expand=expand, fill=fill, **kwargs)
	return frm


vn_basevowels = 'a\u0103\xE2e\xEAio\xF4\u01A1u\u01B0y'
def vn_isbasevowel(c): return (len(c)==1) and c.lower() in vn_basevowels

vn_accmap = {
	'1': '\u0301',
	'2': '\u0300',
	'3': '\u0309',
	'4': '\u0303',
	'5': '\u0323'
}
vn_chrmap = {
	'6': '\u0103',
	'7': '\xE2',
	'8': '\xEA',
	'9': '\xF4',
	'0': '\u01A1',
	'[': '\u01B0',
	']': '\u0111'
}
shift_dict = {
	'1': '!',
	'2': '@',
	'3': '#',
	'4': '$',
	'5': '%',
	'6': '^',
	'7': '&',
	'8': '*',
	'9': '(',
	'0': ')',
	'[': '{',
	']': '}'
}

def tinsert(txt, str):
	if txt.tag_ranges('sel'):
		txt.delete('sel.first', 'sel.last')
	txt.insert('insert', str)

class VnType(Frame):
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.pack(expand=1, fill='both')
		self.make_widgets()
	def make_widgets(self):
		frm=makeframe(self, expand=0, padx=10, pady=(10,0))
		l=Label(frm, justify='left', text='1 - s\u1EAFc\n2 - huy\u1EC1n\n3 - h\u1ECFi\n4 - ng\xE3\n5 - n\u1EB7ng\n6 - \u0103\n7 - \xE2\n8 - \xEA\n9 - \xF4\n0 - \u01A1\n[ - \u01B0\n] - \u0111')
		l.pack(side='left')
		frm=makeframe(self, expand=0, padx=10)
		self.vnflag=BooleanVar()
		self.vnflag.set(True)
		self.cb=Checkbutton(frm, variable=self.vnflag, text='Enable VnType', command=self.onVnCheck)
		self.cb.pack(side='left')
		frm=makeframe(self, fill='x', padx=10)
		l=Label(frm, justify='left', text='Note: You can also use \xABCtrl-(Shift)-\u2039key\u203A\xBB or \xABCommand[Mac]/Alt[Other systems]-(Shift)-\u2039key\u203A\xBB to toggle VnType for one character', wraplength=frm.winfo_width())
		l.pack(side='left', fill='x')
		frm.bind('<Configure>', lambda e, l=l: l.config(wraplength=e.width))
		frm=makeframe(self, padx=10, pady=10)
		self.vntext=scrolledtext.ScrolledText(frm,font='TkTextFont')
		self.vntext.pack(expand=1, fill='both')
		self.vntext.focus_set()
		for char in vn_accmap.keys():
			self.vntext.bind(char, lambda e, x=self, y=char: x.onAccent(y))
			self.vntext.bind('<Control-Key-%c>' % char, lambda e, x=self, y=char: tinsert(x.vntext, y))
			self.vntext.bind('<Control-Key-%c>' % shift_dict[char], lambda e, x=self, y=char: tinsert(x.vntext, shift_dict[y]))
			if sys.platform == 'darwin':
				self.vntext.bind('<Command-Key-%c>' % char, lambda e, x=self, y=char: tinsert(x.vntext, y))
				self.vntext.bind('<Command-Key-%c>' % shift_dict[char], lambda e, x=self, y=char: tinsert(x.vntext, shift_dict[y]))
			else:
				self.vntext.bind('<Alt-Key-%c>' % char, lambda e, x=self, y=char: tinsert(x.vntext, y))
				self.vntext.bind('<Alt-Key-%c>' % shift_dict[char], lambda e, x=self, y=char: tinsert(x.vntext, shift_dict[y]))
		for char in vn_chrmap.keys():
			self.vntext.bind(char, lambda e, x=self, y=char: x.onVnChar(y))
			self.vntext.bind(shift_dict[char], lambda e, x=self, y=char: x.onVnChar(y, 1))
			self.vntext.bind('<Control-Key-%c>' % char, lambda e, x=self, y=char: tinsert(x.vntext, y))
			self.vntext.bind('<Control-Key-%c>' % shift_dict[char], lambda e, x=self, y=char: tinsert(x.vntext, shift_dict[y]))
			if sys.platform == 'darwin':
				self.vntext.bind('<Command-Key-%c>' % char, lambda e, x=self, y=char: tinsert(x.vntext, y))
				self.vntext.bind('<Command-Key-%c>' % shift_dict[char], lambda e, x=self, y=char: tinsert(x.vntext, shift_dict[y]))
			else:
				self.vntext.bind('<Alt-Key-%c>' % char, lambda e, x=self, y=char: tinsert(x.vntext, y))
				self.vntext.bind('<Alt-Key-%c>' % shift_dict[char], lambda e, x=self, y=char: tinsert(x.vntext, shift_dict[y]))
		menubar=Menu(self.master)
		commands=Menu(menubar, tearoff=0)
		menubar.add_cascade(label='Commands', underline=0, menu=commands)
		commands.add_checkbutton(label='Enable VnType', variable=self.vnflag, command=self.onVnCheck, accelerator=('Command-n' if sys.platform=='darwin' else 'Control-n'))
		self.master['menu']=menubar
		def f(e,x=self):
			x.vnflag.set(not x.vnflag.get())
			x.onVnCheck()
		self.bind_all(('<Command-n>' if sys.platform=='darwin' else '<Control-n>'),f);
	def onVnCheck(self):
		self.vntext.focus_set()
		if self.vnflag.get():
			for char in vn_accmap.keys():
				self.vntext.bind(char, lambda e, x=self, y=char: x.onAccent(y))
				self.vntext.bind('<Control-Key-%c>' % char, lambda e, x=self, y=char: tinsert(x.vntext, y))
				self.vntext.bind('<Control-Key-%c>' % shift_dict[char], lambda e, x=self, y=char: tinsert(x.vntext, shift_dict[y]))
				if sys.platform == 'darwin':
					self.vntext.bind('<Command-Key-%c>' % char, lambda e, x=self, y=char: tinsert(x.vntext, y))
					self.vntext.bind('<Command-Key-%c>' % shift_dict[char], lambda e, x=self, y=char: tinsert(x.vntext, shift_dict[y]))
				else:
					self.vntext.bind('<Alt-Key-%c>' % char, lambda e, x=self, y=char: tinsert(x.vntext, y))
					self.vntext.bind('<Alt-Key-%c>' % shift_dict[char], lambda e, x=self, y=char: tinsert(x.vntext, shift_dict[y]))
			for char in vn_chrmap.keys():
				self.vntext.bind(char, lambda e, x=self, y=char: x.onVnChar(y))
				self.vntext.bind(shift_dict[char], lambda e, x=self, y=char: x.onVnChar(y, 1))
				self.vntext.bind('<Control-Key-%c>' % char, lambda e, x=self, y=char: tinsert(x.vntext, y))
				self.vntext.bind('<Control-Key-%c>' % shift_dict[char], lambda e, x=self, y=char: tinsert(x.vntext, shift_dict[y]))
				if sys.platform == 'darwin':
					self.vntext.bind('<Command-Key-%c>' % char, lambda e, x=self, y=char: tinsert(x.vntext, y))
					self.vntext.bind('<Command-Key-%c>' % shift_dict[char], lambda e, x=self, y=char: tinsert(x.vntext, shift_dict[y]))
				else:
					self.vntext.bind('<Alt-Key-%c>' % char, lambda e, x=self, y=char: tinsert(x.vntext, y))
					self.vntext.bind('<Alt-Key-%c>' % shift_dict[char], lambda e, x=self, y=char: tinsert(x.vntext, shift_dict[y]))
		else:
			for char in vn_accmap.keys():
				self.vntext.unbind(char)
				self.vntext.bind('<Control-Key-%c>' % char, lambda e, x=self, y=char: x.onAccent(y))
				if sys.platform == 'darwin': self.vntext.bind('<Command-Key-%c>' % char, lambda e, x=self, y=char: x.onAccent(y))
				else: self.vntext.bind('<Alt-Key-%c>' % char, lambda e, x=self, y=char: x.onAccent(y))
			for char in vn_chrmap.keys():
				self.vntext.unbind(char)
				self.vntext.unbind(shift_dict[char])
				self.vntext.bind('<Control-Key-%c>' % char, lambda e, x=self, y=char: x.onVnChar(y))
				self.vntext.bind('<Control-Key-%c>' % shift_dict[char], lambda e, x=self, y=char: x.onVnChar(y, 1))
				if sys.platform == 'darwin':
					self.vntext.bind('<Command-Key-%c>' % char, lambda e, x=self, y=char: x.onVnChar(y))
					self.vntext.bind('<Command-Key-%c>' % shift_dict[char], lambda e, x=self, y=char: x.onVnChar(y, 1))
				else:
					self.vntext.bind('<Alt-Key-%c>' % char, lambda e, x=self, y=char: x.onVnChar(y))
					self.vntext.bind('<Alt-Key-%c>' % shift_dict[char], lambda e, x=self, y=char: x.onVnChar(y, 1))
	def onAccent(self, accent):
		if (vn_isbasevowel(self.vntext.get('sel.first-1c','sel.first')) if self.vntext.tag_ranges('sel') else vn_isbasevowel(self.vntext.get('insert-1c','insert'))):
			tinsert(self.vntext, vn_accmap[accent])
			return 'break' #prevent default
	def onVnChar(self, char, shift=0):
		if shift:
			tinsert(self.vntext, vn_chrmap[char].upper())
		else:
			tinsert(self.vntext, vn_chrmap[char])
		return 'break'
if __name__ == '__main__':
	root=Tk()
	root.title('VnType')
	root.iconname('VnType')
	root.geometry('+0+0')
	main=VnType(root)
	if sys.platform == 'darwin':
		script = 'tell application "System Events" to set frontmost of the first process whose unix id is {pid} to true'.format(pid=os.getpid())
		os.system("/usr/bin/osascript -e '{script}'".format(script=script))
	root.mainloop()