import urllib
import urllib2
import base64
import simplejson
from PyQt4.QtCore import *
from PyKDE4.kdecore import *
from PyKDE4.kio import *

class RubytimeSession:

  def __init__(self, url, username, passwd, applet):
    self.url, self.username, self.password = url, username, passwd
    self.applet = applet
    pass

  def getProjects(self):
    return self.makeRequest('/projects')

  def getActivities(self):
    return self.makeRequest('/activities')

  def addActivity(self, activity):
    data = urllib.urlencode({ 'activity[date]': activity['date'], 'activity[project_id]': activity['project_id'],
                              'activity[hours]': activity['hours'], 'activity[comments]': activity['comments'] })
    return self.makeRequest('/activities', data)

  def makeRequest(self, path, data=None):
    url = (self.url + path).replace("://", "://" + self.username + "@")
    if url.find("?") == -1:
      url += "?auth=basic"
    else:
      url += "&auth=basic"
    print url

    if data:
      pass
    else:
      job = KIO.storedGet(KUrl(url), KIO.Reload, KIO.HideProgressInfo)
    # we want JSON
    job.addMetaData("accept", "application/json, text/javascript, */*")
    job.addMetaData("cookies", "none")
    QObject.connect(job, SIGNAL("result(KJob*)"), self.jobFinished)
    return [False, None]

  def jobFinished(self, job):
    print "job finished"
    err = job.error()
    print job, job.url().path(), err
    print job.errorString()
    print job.errorText()

    if err > 0:
      if err == KIO.ERR_COULD_NOT_CONNECT:
        print "connection problem"
      else:
        print "other error"
        print job.data()
    elif job.isErrorPage():
      print "some error page"
    else:
      print "success"
      print job.data()



  def makeRequest2(self, path, data=None):
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
    return [status, content]

if __name__ == "__main__":
  session = RubytimeSession("http://localhost:4000", "dev1", "password")
  print session.getActivities()
#  print session.getProjects()
#  print session.addActivity({ 'date': '2009-04-14', 'project_id': 1, 'hours': '31.5', 'comments': 'blaa' })
  