import requests

class Scraper:
	def __init__(self):
		pass

	def get_subreddit_json(self, subreddit, listing, limit, timeframe):
		try:
			base_url = f"https://www.reddit.com/r/{subreddit}/{listing}.json?limit={limit}&t={timeframe}"
			request = requests.get(base_url, headers = {"User-agent": "yourmom"})
		except:
			print("An Error Occured")
		
		print("Reddit page gotten.")
		
		return request.json()

	def get_post_json(self, url):
		try:
			request = requests.get(url, headers = {"User-agent": "yourmom"})
		except:
			print("An Error Occured")
		
		print("Reddit page gotten.")
		
		return request.json()

	def get_post_urls_from_subreddit(self, page):
		urls = []
		for post in page["data"]["children"]:
			urls.append(post["data"]["url"])
		
		print("Got urls from subreddit.")
		
		return urls

	def get_video_urls_from_subreddit(self, page):
		urls = []
		for post in page["data"]["children"]:
			if "url_overridden_by_dest" in post["data"]:
				urls.append(post["data"]["url_overridden_by_dest"])

		print("Got video urls from subreddit.")
		
		return urls

	def get_video_url_from_post(self, page):
		if "url_overridden_by_dest" in page[0]["data"]["children"][0]["data"]:
			print("Got video url from post.")
			return page[0]["data"]["children"][0]["data"]["url_overridden_by_dest"]

	def get_post_data(self, page):
		post = {
			"author": "",
			"title": "",
			"ups": "",
			"subreddit": "",
			"body": ""
		}
		post["author"] = page[0]["data"]["children"][0]["data"]["author"]
		post["title"] = page[0]["data"]["children"][0]["data"]["title"]
		post["ups"] = page[0]["data"]["children"][0]["data"]["ups"]
		post["subreddit"] = page[0]["data"]["children"][0]["data"]["subreddit"]
		post["body"] = page[0]["data"]["children"][0]["data"]["selftext"]

		print("Got post data.")

		return post

	def get_comments_from_post(self, page, amount):
		comments = []
		for i in range(amount):
			comment = {
				"author": "",
				"body": "",
				"ups": ""
			}
			comment["author"] = page[1]["data"]["children"][i]["data"]["author"]
			comment["body"] = page[1]["data"]["children"][i]["data"]["body"]
			comment["ups"] = page[1]["data"]["children"][i]["data"]["ups"]

			if comment["body"] == "[deleted]" or comment["body"] == "[removed]":
				continue

			comments.append(comment)

		print("Got comments from post.")

		return comments

	def get_images_urls_from_subreddit(self, page):
		urls = []
		for post in page["data"]["children"]:
			if "url_overridden_by_dest" in post["data"]:
				if post["data"]["url_overridden_by_dest"].endswith(".png") or post["data"]["url_overridden_by_dest"].endswith(".jpg"):
					urls.append(post["data"]["url_overridden_by_dest"])

		return urls