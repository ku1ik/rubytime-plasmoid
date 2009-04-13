import urllib
import urllib2
import base64
import simplejson


class RubytimeSession:

  def __init__(self, url, username, passwd):
    self.url, self.username, self.password = url, username, passwd
    pass

  def getProjects(self):
    return self.makeRequest('/projects.json')

  def getActivities(self):
    return self.makeRequest('/activities.json')

  def addActivity(self, activity):
    data = urllib.urlencode({ 'activity[date]': activity['date'], 'activity[project_id]': activity['project_id'],
                              'activity[hours]': activity['hours'], 'activity[comments]': activity['comments'] })
    return self.makeRequest('/activities.json', data)

  def makeRequest(self, path, data=None):
    base64string = base64.encodestring('%s:%s' % (self.username, self.password))[:-1]
    authheader =  "Basic %s" % base64string
    if data:
      req = urllib2.Request(self.url + path, data)
    else:
      req = urllib2.Request(self.url + path)
    req.add_header("Authorization", authheader)
    try:
      status, content = True, simplejson.JSONDecoder().decode(urllib2.urlopen(req).read())
    except urllib2.HTTPError, e:
      if e.code == 201:
        status, content = True, None
      elif e.code == 400:
        status, content = False, simplejson.JSONDecoder().decode(e.fp.read())
      else:
        raise e
    #except Exception, e:
    #  return None
    return [status, content]

if __name__ == "__main__":
  session = RubytimeSession("http://localhost:4000", "dev1", "password")
#  print session.getActivities()
#  print session.getProjects()
  print session.addActivity({ 'date': '2009-04-14', 'project_id': 1, 'hours': '31.5', 'comments': 'blaa' })
  