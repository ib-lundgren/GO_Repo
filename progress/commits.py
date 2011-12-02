from packages import feedparser

url = "https://github.com/ib-lundgren/GO_Repo/commits/master.atom"

def get_commits():
   feed = feedparser.parse(url)
   if len(feed.entries) < 10:
      c = len(feed.entries)
   else:
      c = 10

   commits = []

   for i in range(c):
      u = feed.entries[i].updated
      time = u[:10] + " " + u[11:17]
      commits.append({ "updated" : time, 
                       "title" : feed.entries[i].title, 
                       "url" : feed.entries[i].links[0]["href"]})

   return commits
   
   
