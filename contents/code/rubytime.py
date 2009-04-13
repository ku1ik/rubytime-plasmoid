import urllib
import urllib2
import base64
import simplejson

class RubytimeSession:

  def __init__(self, url, username, passwd):
    self.url, self.username, self.password = url, username, passwd
    pass

  def getProjects(self):
    jsonData = self.makeRequest('/projects.json')
    try:
      return simplejson.JSONDecoder().decode(jsonData)
    except ValueError:
      return []

  def getActivities(self):
    jsonData = self.makeRequest('/activities.json')
    try:
      return simplejson.JSONDecoder().decode(jsonData)
    except ValueError:
      return []

  def addActivity(self, date, project_id, hours, comments):
    data = urllib.urlencode({ 'activity[date]': date, 'activity[project_id]': project_id, 'activity[hours]': hours,
                              'activity[comments]': comments })
    try:
      self.makeRequest('/activities', data)
    except urllib2.HTTPError, e:
      return e.code == 201
    except Exception, e:
      return False

  def makeRequest(self, path, data=None):
    base64string = base64.encodestring('%s:%s' % (self.username, self.password))[:-1]
    authheader =  "Basic %s" % base64string
    if data:
      req = urllib2.Request(self.url + path, data)
    else:
      req = urllib2.Request(self.url + path)

    req.add_header("Authorization", authheader)
    return urllib2.urlopen(req).read()

  def _makeRequest(self, path):
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
    pagehandle = urllib2.urlopen(self.url + path)
    # authentication is now handled automatically for us
    return pagehandle.read()

if __name__ == "__main__":
  session = RubytimeSession("http://localhost:4000", "dev1", "password")
  print session.getActivities()
#  print session.getProjects()
#  print session.addActivity(date='2009-04-14', project_id=1, hours='6.5', comments='blaa')
  