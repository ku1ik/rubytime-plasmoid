import urllib2

class RubytimeSession:

  def __init__(self, username, passwd):
    self.url = 'rt.llp.pl'
    self.username, self.password = username, passwd
    pass

  def get_activities(self):
    print self.make_request('/activities')
    pass

  def make_request(self, path):
    passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
    passman.add_password(None, self.url + path, self.username, self.password)
    # because we have put None at the start it will always
    # use this username/password combination for  urls
    # for which `theurl` is a super-url
    authhandler = urllib2.HTTPBasicAuthHandler(passman)
    # create the AuthHandler
    opener = urllib2.build_opener(authhandler)
    urllib2.install_opener(opener)
    # All calls to urllib2.urlopen will now use our handler
    # Make sure not to include the protocol in with the URL, or
    # HTTPPasswordMgrWithDefaultRealm will be very confused.
    # You must (of course) use it when fetching the page though.
    pagehandle = urllib2.urlopen('http://' + self.url)
    # authentication is now handled automatically for us
    return pagehandle.read()
  