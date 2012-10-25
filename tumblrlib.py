import urllib
import urllib2
import webbrowser
import simplejson


### Utility functions for generating web pages
def make_html_header(title):
    s = "<html><head>\n<title>%s</title>\n" % title
    s = s + "<link rel='stylesheet' href='assets/hw11.css' type='text/css' />\n"
    s = s + "</head>\n"
    s = s + "<body>\n"
    s=s+'<div id=\'container\'>'
    return s   

def make_html_footer():
  return "\n</div></body></html>"
  
def make_html_link(URL, name):
  return "<div class=\"favSiteDiv\"><a class=\"favSite\" href=\"%s\">%s</a></div>\n" % (URL, name)

def make_html_img(URL):
  return "<div><img class=\"favImg\" src=\"%s\"/></div>\n" % (URL)


### Utility functions for getting and representing data from tumblr
def pretty(obj):
  return simplejson.dumps(obj, sort_keys=True, indent=2)

def safeGet(url):
  try:
    return urllib2.urlopen(url)
  except urllib2.URLError, e:
    if hasattr(e, 'reason'):
      print 'We failed to reach a server.'
      print 'Reason: ', e.reason
      print 'Sorry, tumblr is lame! Try again later!'
    elif hasattr(e, 'code'):
      print 'The server couldn\'t fulfill the request.'
      print 'Error code: ', e.code
      print 'Sorry, tumblr is lame! Try again later!'
    return None

def tumblr_url(targ,params={}):
  teh_url='http://%s.tumblr.com/api/read/json' % (targ)
  params['debug']=1
  url = teh_url + "?" + urllib.urlencode(params)
  return safeGet(url)


def get_posts(targ,tag,params):
  params['tagged']=tag
  result=tumblr_url(targ,params)
  if result is None:
    return 'Sorry, tumblr is lame! Try again later!'
  else:
  	d = simplejson.loads(result.read())
  	post_dicts = d['posts']
  	return [Blog(photo) for photo in post_dicts]

def toHTML(x):
	pass

#Builds the string
class Blog():
  def __init__(self, d):
    if d['slug']:
    	self.title=d['slug'].encode('utf-8')
    else:
    	self.title='No Title'
    self.what_sort=d['type']
    self.timestamp=int(d['unix-timestamp'])
    self.url=d['url']
    self.date=d['date']
    if d['type']=='photo':
    	self.img_url=d['photo-url-400']
    if d['type']=='link':
    	self.link_text=d['link-text']
    	self.link_url=d['link-url']
    if d['type']=='answer':
    	self.teh_ans=d['answer']
    	self.teh_q=d['question']
    if d['type']=='quote':
    	self.qt=d['quote-text'].encode('utf-8')
    	self.qs=d['quote-source'].encode('utf-8')
    if d['type']=='regular':
    	self.txt=d['regular-body'].encode('utf-8')
    if 'photo-caption' in d:
    	self.cap=d['photo-caption'].encode('utf-8')
  
  def __str__(self):
    s = 'Summary: %s\n' % self.title.encode('utf-8')
    s += 'What kind is it?: %s\n' % self.what_sort.encode('utf-8')
    s += 'Date: %s\n' % self.date
    if self.what_sort=='photo':
    	s+='Image URL: %s\n' %self.img_url
    elif self.what_sort=='answer':
    	try:
    		s+='The Question was: %s\nThe Answer was: %s\n' %(self.teh_q,self.teh_ans)
    	except:
    		s+='There\'s some weird stuff in there... Can\'t display.\n'
    return s
    
  def makeHTML(self):
  	s ="<table>"
  	s+="  <tr>\n"
  	s+="    <td>Title:</td>\n"
  	s+="    <td>%s</td>\n" % self.title.encode('utf-8')
  	s+="  </tr>\n"
  	s+="  <tr>\n"
  	s+="    <td>What Kind?:</td>\n"
  	s+="    <td>%s</td>\n" % self.what_sort.encode('utf-8')
  	s+="  </tr>\n"
  	s+="  <tr>\n"
  	s+="    <td>Date:</td>\n"
  	s+="    <td>%s</td>\n" % self.date
  	s+="  </tr>\n"
  	s+="  <tr>\n"
  	if self.what_sort=='photo':
  		s+="  <tr>\n"
  		s+="    <td>Dah Pic:</td>\n"
  		try:
  			s+="    <td><img src='%s'></img></td>\n" % self.img_url
  		except:
  			s+="    <td>Some sort of error, eh?</td>\n"
  		s+="  </tr>\n"
  		s+="  <tr>\n"
  		s+="    <td>Caption:</td>\n"
  		try:
  			s+="    <td>%s</td>\n" % self.cap
  		except:
  			s+="    <td>Whoa! Weird text or something...</td>\n"
  		s+="  </tr>\n"
  	elif self.what_sort=='answer':
  		s+="  <tr>\n"
  		s+="    <td>Question:</td>\n"
  		s+="    <td>%s</td>\n" % self.teh_q.encode('utf-8')
  		s+="  </tr>\n"
  		s+="  <tr>\n"
  		s+="    <td>Answer:</td>\n"
  		try:
  			s+="    <td>%s</td>\n" % self.teh_ans.encode('utf-8')
  		except:
  			s+="    <td>Whoa! Weird text or something...</td>\n"
  		s+="  </tr>\n"
  	elif self.what_sort=='link':
  		s+="  <tr>\n"
  		s+="    <td>What it says:</td>\n"
  		s+="    <td>%s</td>\n" % self.link_text
  		s+="  </tr>\n"
  		s+="  <tr>\n"
  		s+="    <td>The URL:</td>\n"
  		s+="    <td><a href=\'%s\' target=\'_blank\'>%s</a></td>\n" % (self.link_url, self.link_url)
  		s+="  </tr>\n"	
  	elif self.what_sort=='quote':
  		s+="  <tr>\n"
  		s+="    <td>The Quote:</td>\n"
  		try:
  			s+="    <td>%s</td>\n" % self.qt
  		except:
  			s+="    <td>Whoa! Weird text or something...</td>\n"
  		s+="  </tr>\n"
  		s+="  <tr>\n"
  		s+="    <td>From:</td>\n"
  		try:
  			s+="    <td>%s</td>\n" % self.qs
  		except:
  			s+="    <td>Whoa! Weird source or something...</td>\n"
  		s+="  </tr>\n"
  	elif self.what_sort=='regular':
  		s+="  <tr>\n"
  		s+="    <td>Oh, a Blog Post!:</td>\n"
  		try:
  			s+="    <td>%s</td>\n" % self.txt
  		except:
  			s+="    <td>Whoa! Weird text or something...</td>\n"
  		s+="  </tr>\n"
  	s+="  <tr>\n"
  	s+="    <td>QR Code to this post:</td>\n"
  	s+="    <td><div class=\'qr\'><img src='https://chart.googleapis.com/chart?cht=qr&chs=150x150&chl=%s'/></div></td>\n" % self.url
  	s+="  </tr>\n"  	
  	s+= "</table><br>"
  	return s


