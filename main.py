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
import webapp2
import urllib2
from google.appengine.api import urlfetch

class MainHandler(webapp2.RequestHandler):
	def get(self, method):
		if method in ["Browse", "Push", "Config","Account", "Describe", "Search", "Report", "Preset", "Tune", R]:
			url = "http://opml.radiotime.com/" + method + ".ashx?"
			get = {}
			for i in self.request.GET.items():
				get[i[0]] = i[1]
					
			if method != "Tune" or (len(self.request.get("c")) > 0 and method == "Tune"):
				self.response.headers['Content-Type'] = 'application/json'
			else:
				self.response.headers['Content-Disposition'] = 'attachment;filename=Tune.m3u'
				try:
					del get["render"]
				except KeyError, e:
					pass

			for i in get.keys():
				url = url + i + "=" + get[i] + "&"

			result = urlfetch.fetch(url)
			if result.status_code == 200:
				ret = result.content.replace("opml.radiotime.com", self.request.headers["Host"])
				self.response.write(ret)


		else:
			self.response.write('error')

class ErrorHandler(webapp2.RequestHandler):
	def get(self, method):
		self.response.write('error')

app = webapp2.WSGIApplication([
    ('/(.*).ashx', MainHandler),
    ('/(.*)', ErrorHandler),
], debug=False)
