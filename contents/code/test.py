import urllib2
import base64

realm, url, username, password = "Application", "http://localhost:4000/activities", "dev1", "password"
#realm, url, username, password = "BLOGZ", "http://localhost:4567/posts", "kill", "karnuf"
#realm, url, username, password = None, "http://rt.llp.pl/activities", "mkulik", "solnahej123"

def one():
  try:
    passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
    passman.add_password(None, url, username, password)
    # because we have put None at the start it will always
    # use this username/password combination for  urls
    # for which `theurl` is a super-url
    authhandler = urllib2.HTTPBasicAuthHandler(passman)
    # create the AuthHandler
    opener = urllib2.build_opener(authhandler)
    opener.open(url).read()
    #urllib2.install_opener(opener)
    # All calls to urllib2.urlopen will now use our handler
    # Make sure not to include the protocol in with the URL, or
    # HTTPPasswordMgrWithDefaultRealm will be very confused.
    # You must (of course) use it when fetching the page though.
    #pagehandle = urllib2.urlopen(url)
    # authentication is now handled automatically for us
    #print pagehandle.read()
    print "one: success"
  except urllib2.HTTPError, e:
    print "one: failed"

def two():
  try:
    auth_handler = urllib2.HTTPBasicAuthHandler()
    auth_handler.add_password(realm, url, username, password)
    opener = urllib2.build_opener(auth_handler)
    handle = opener.open(url)
    handle.read()
    print "two: success"
  except urllib2.HTTPError, e:
    print "two: failed"

def three():
  try:
    #data = urllib.urlencode(values)
    base64string = base64.encodestring('%s:%s' % (username, password))[:-1]
    authheader =  "Basic %s" % base64string
    req = urllib2.Request(url)
    req.add_header("Authorization", authheader)
    response = urllib2.urlopen(req)
    print "three: success"
    response.read()
  except urllib2.HTTPError, e:
    print "three: failed"

#one()
#two()
three()