#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
import tumblrlib
from google.appengine.ext.webapp import template

class DjangoHandler2(webapp.RequestHandler):
	def get(self):
		from google.appengine.ext.webapp import template
		import os
		template_values = {"tumblrr": "itsallabeautifullie"}
		fname = os.path.join(os.path.dirname(__file__), 'template.tpl')
		output = template.render(fname, template_values) 

class QRPageHandler(webapp.RequestHandler):
	def get(self):
		if self.request.get('person'):
			tg=self.request.get('person')
		else:
			tg='itsallabeautifullie'
		t=''
		params={'num':49}
		postar=tumblrlib.get_posts(tg,t,params)
		page=tumblrlib.make_html_header('QR Page')
		page+='<a href="/"> Go Back </a><br>'
		k=0
		l=0
		for p in postar:
			if l==3 and k==3:
				page+="<img src='https://chart.googleapis.com/chart?cht=qr&chs=120x120&chl=http://%s.tumblr.com'></img>" %tg
				l+=1
				k+=1
				continue
			else:
				page+="<img src='https://chart.googleapis.com/chart?cht=qr&chs=120x120&chl=%s'></img>" % p.url
				k+=1
			if k==7:
				page+='<br>'
				k=0
				l+=1
		page += tumblrlib.make_html_footer()
		self.response.out.write(page)
    	
    	
  
class TumblrHandler(webapp.RequestHandler):
    def get(self):
    	if self.request.get('person'):
    		tg=self.request.get('person')
    	else:
    		tg='itsallabeautifullie'
    	if self.request.get('tagzor'):
    		t=self.request.get('tagzor')
    	else:
    		t=''
    	if self.request.get('sorter')=='answer':
    		params={}
    	elif self.request.get('sorter') and self.request.get('sorter')!='answer':
    		s=self.request.get('sorter')
    		params={'type':s}
    	else:
    		params={}
    	if t=='':
    		tt='noting in particular'
    	else:
    		tt=t
    	postses=tumblrlib.get_posts(tg,t,params)

    	t1 = template.Template('You are searching the tumblr {{ tum_name }} for {{search_kind}}')
    	c1 = template.Context({"tum_name": tg, "search_kind": tt})
    	output = t1.render(c1)

    
    	
    	if self.request.get('sorter')=='answer':
    		page = tumblrlib.make_html_header(output)
    		page+=self.genForm()
    		page+='Want to see this blog as a <a href="/qrpage.html?person=%s">QR</a> page?' % tg
    		if p.what_sort=='answer':
    				page += p.makeHTML()
    		page += tumblrlib.make_html_footer()
    	else:
    		try:	
    			page = tumblrlib.make_html_header(output)
    			page+=self.genForm()  
    			page+='Want to see this blog as a <a href="/qrpage.html?person=%s">QR</a> page?' % tg
    			for p in postses:
    				page += p.makeHTML()
    			page += tumblrlib.make_html_footer()
    		except:
    			page= '\n\n\n\n<br><br>Hey, something isn\'t working... It\'s tumblr\'s fault though! Try again soon.\n\n\n'
    	self.response.out.write(page)
        
    def genForm(self):
    	if self.request.get('person'):
    		tg=self.request.get('person')
    	else:
    		tg='itsallabeautifullie'
    	if self.request.get('tagzor'):
    		t=self.request.get('tagzor')
    	else:
    		t=''
    	formstring='<form action=\'/\' method=\'get\'>'
    	formstring+='Whoya looking for? (Defaults to my friend) <input type="text" value="%s" name="person" />' %tg
    	formstring+='<br> Something specific you\'re looking for? (optional)<input value="%s" type="text" name="tagzor" />' %t
    	formstring+='<br>And what sorta things ya wanna see? <select name=\'sorter\' id=\'sorter\'>'
    	formstring+='<option value=\'\'> Everything </option>'
    	formstring+='<option value=\'quote\'> Quote </option>'
    	formstring+='<option value=\'answer\'> Q&A </option>'
    	formstring+='<option value=\'link\'> Link </option>'
    	formstring+='<option value=\'regular\'> Regular </option>'
    	formstring+='<option value=\'photo\'> Photo </option>'
    	formstring+='</select><input type=\'submit\' value=\'DO IT\' /> </form>'
    	return formstring    
        


def main():
    application = webapp.WSGIApplication([('/', TumblrHandler),
    																		('/templated2.html', DjangoHandler2),
    																		('/qrpage.html', QRPageHandler)
    																		],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
