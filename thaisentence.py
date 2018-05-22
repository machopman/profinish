# -*- coding: utf-8 -*-
from __future__ import absolute_import,unicode_literals
import os
import codecs
#templates_dir = os.path.join(os.path.dirname(pythainlp.__file__), 'corpus')
template_file = os.path.join('thaisentence.txt')

def data():
	with codecs.open(template_file, 'r',encoding='utf8') as f:
		lines = f.read().splitlines()
	return lines

