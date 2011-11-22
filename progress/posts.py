#!/usr/bin/env python
from google.appengine.api import urlfetch
from django.utils import simplejson as json
from StringIO import StringIO

def get_posts():	
   key = "AIzaSyBCrbEsJI3o-gxnBrmShcqWWaJXP9jQj7o"
   user = "117412220796828368178"
   url = "https://www.googleapis.com/plus/v1/people/%s/activities/public?key=%s" % (user, key)

   result = urlfetch.fetch(url)
   j = json.loads(result.content)
   posts = []
   for item in j["items"]:
      if item["verb"] == "post":
	actor = item["actor"]["displayName"]
	img = item["actor"]["image"]["url"]
	updated = item["updated"][:10] + " " + item["updated"][11:17]
	content = item["object"]["content"]
	url = item["actor"]["url"]
	posts.append({"actor":actor, "img":img, "url":url, "updated":updated, "content":content})
   return posts

if __name__ == "__main__":
	print posts()
