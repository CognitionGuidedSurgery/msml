#######################################################################
## TIny Template ENgine
##
## Titen aims to be a very small and fast template engine, and yet be
## expressive enough for all template needs.
##
## Authors: <revcompgeek@gmail.com>
#######################################################################

import re,types
import string
from string import strip
from cgi import escape

def titen(text="",file=""):
	"""Parses a string or file object and returns a function that can
	   be called to evaluate the template."""
	if type(file) != str:
		return _parse(file.read())
	elif len(file) > 0:
		return _parse(open(file).read())
	else:
		return _parse(text)
		
_titen_globals = {'__builtins__':dict([(f.__name__,f) for f in [range,int,float,bool,ord,str,hex,min,max,abs,string.upper,string.lower,string.strip,string.capwords]] + [('True',True),('False',False)])}

_pyvar = r"([a-zA-Z][a-zA-Z0-9_]*)"
_pyexpr = r"((?:[^}\"]*\"(?:[^\"]|\\\")*\"|[^}\"])+)"

def _eval(expr,l): return eval(expr,_titen_globals,l)

def _print(text): return text
_print.re = re.compile(r"([^{]+)")

def _brace_escape(): return '{'
_brace_escape.re = re.compile(r"\{\{")

def _replace(c,expr):
	if c == '$':
		def do_replace(l):
			return str(_eval(expr,l))
		return do_replace
	elif c == '%':
		def do_replace(l):
			return escape(str(_eval(expr,l)))
		return do_replace
	raise Exception("BAD!!!")
_replace.re = re.compile(r"\{([$%])\s*" + _pyexpr + r"\s*\}")

def _if(expr,f,else_part=None):
	def do_if(l):
		if _eval(expr,l):
			return f(l)
		elif else_part:
			return else_part(l)
		return ""
	return do_if
_if.re = re.compile(r"\{\s*(el)?if\s+" + _pyexpr + r"\s*\}")
_if.needs_end = True
_if.takes_else = True
_if.has_el = True

def _if_exists(var,f,e=None):
	def do_ifexists(l):
		if l.has_key(var):	return f(l)
		elif e:				return e(l)
		return ""
	return do_ifexists
_if_exists.re = re.compile(r"\{\s*(el)?if\s+exists\s+" + _pyvar + r"\s*\}")
_if_exists.needs_end = True
_if_exists.takes_else = True
_if_exists.has_el = True

def _for(var,expr,f,e=None):
	def do_for(l):
		s = ""
		for val in _eval(expr,l):
			l[var] = val
			s += f(l)
		else:
			if e: return e(l)
		return s
	return do_for
_for.re = re.compile(r"\{\s*for\s+" + _pyvar + "\s+in\s+" + _pyexpr + r"\s*\}")
_for.needs_end = True
_for.takes_else = True

def _else(f): return f
_else.re = re.compile(r"\{\s*(el)se\s*\}")
_else.needs_end = True
_else.has_el = True

def _do_list(list):
	if len(list) == 1 and type(list[0]) == types.FunctionType: return list[0]
	def do_list(l):
		s = ""
		for item in list:
			if type(item) == str:
				s += item
			else:
				s += item(l)
		return s
	return do_list

def _def(func_name,params,f):
	if params == None:
		params = []
	else:
		params = map(strip,params.split(","))
	def add_func(l):
		def exec_func(*values):
			for i in range(len(params)):
				if i < len(values):
					l[params[i]] = values[i]
				else:
					l[params[i]] = ""
			return f(l)
		l[func_name]=exec_func
		return ""
	return add_func
_def.re = re.compile(r"\{\s*def\s+([a-zA-Z_][a-zA-Z0-9_]*)(?:\(([a-zA-Z_][a-zA-Z0-9_]*(?:\s*,\s*[a-zA-Z_][a-zA-Z0-9_]*)*)?\))?\}")
_def.needs_end = True

def _include(raw,filename):
	if raw:
		return open(filename).read()
	else:
		return _parse(open(filename).read())
_include.re = re.compile(r"\{\s*include\s+(?:(raw)\s+)?([a-zA-Z0-9-_./\\]+)\s*\}")

def _import(filename):
	f = _include(filename)
	def do_import(l): # Can anyone think of a better way to do this?
		f(l)
		return ""
	return do_import
_import.re = re.compile(r"\{\s*import\s+([a-zA-Z0-9-_./\\]+)\s*\}")

def _comment(): return None
_comment.re = re.compile(r"\{#[^}]*\}")

def _parse(text):
	until_brace = re.compile(r"[^{]+")
	end_templ = re.compile(r"\{\s*end[^}]*\}") # { end }
	
	blocks = [_print,_brace_escape,_replace,_else,_if_exists,_if,_for,_def,_import,_include,_comment]
	
	stack = [[]]
	def addText(txt):
		if len(stack[-1]) > 0 and type(stack[-1][-1]) == str:
			stack[-1][-1].append(txt)
		else:
			stack[-1].append(txt)
	while len(text) > 0:
		matched = 0
		if len(text) == 0:
			break
		
		m = end_templ.match(text)
		if m: #end
			if len(stack) == 1:
				raise Exception("Need {for}, {if}, {elif} or {else} before {end}")
			text = text[m.end():]
			stack[-2][1].extend([_do_list(stack.pop(-1))])
			while type(stack[-1]) == tuple:
				fn = stack.pop(-1)
				t = fn[0](*fn[1])
				if t != None:
					if type(stack[-1]) == list:
						stack[-1].extend([t])
					else:
						stack[-1][1].extend([t])
			continue
		for b in blocks:
			m = b.re.match(text)
			if m:
				text = text[m.end():]
				if hasattr(b,'needs_end') and b.needs_end:
					if m.group(1) == "el":
						if len(stack) < 2:
							raise Exception("Need {if} before {elif} or {else}")
						if not hasattr(stack[-2][0],'takes_else'):
							raise Exception("{else} in bad location")
						stack[-2][1].extend([_do_list(stack.pop(-1))])
					if hasattr(b,'has_el'):
						stack.extend([ (b,list(m.groups()[1:])),[] ])
					else:
						stack.extend([ (b,list(m.groups())),[] ])
				else:
					t = b(*m.groups())
					if t != None: stack[-1].extend([ t ])
				matched = 1
				break
		if matched == 0:
			m = re.compile("\{[^}]*\}").match(text)
			s = m.group(0) if m else ""
			raise Exception("No matches for {0}".format(s))
		
	if len(stack) != 1:
		raise Exception("Not enough {end}")
	f = _do_list(stack[0])
	def titen_render(template_locals={},**template_locals2):
		template_locals.update(template_locals2)
		try:
			return f(template_locals)
		except Exception,e:
			return str(e.__class__.__name__) + ": " + str(e)
	return titen_render
