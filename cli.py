from backend.video_maker import VideoMaker
import argparse

def main():
	parser = argparse.ArgumentParser(description="Make a video compilation from a subreddit.")
	subparsers = parser.add_subparsers(dest="action", help="Pass an action as first argument (compilation, post, comments, multiple_posts, multiple_comments)")
	
	auto_compilation_parser = subparsers.add_parser("auto_compilation", help="Generates a compilation video")
	auto_compilation_parser.add_argument("subreddit", type=str, help="What subreddit to use")
	auto_compilation_parser.add_argument("--listing", type=str, help="What listing to use (hot, top etc.)", default="top")
	auto_compilation_parser.add_argument("--limit", type=int, help="How many videos to compile", default=12)
	auto_compilation_parser.add_argument("--timeframe", type=str, help="What timeframe to use (day, week etc)", default="day")
	auto_compilation_parser.add_argument("--width", type=int, help="Width of the outputted video", default=1280)
	auto_compilation_parser.add_argument("--height", type=int, help="Height of the outputted video", default=720)
	auto_compilation_parser.add_argument("--drive", type=bool, help="Save the video to google drive or not", default=False)

	manual_compilation_parser = subparsers.add_parser("manual_compilation", help="Generates a compilation video from custom urls")
	manual_compilation_parser.add_argument("--urls", nargs="+", help="File path with urls to videos", default=[], required=True)
	manual_compilation_parser.add_argument("--subreddit", type=str, help="What subreddit to use", default="TikTokCringe")
	manual_compilation_parser.add_argument("--width", type=int, help="Width of the outputted video", default=1280)
	manual_compilation_parser.add_argument("--height", type=int, help="Height of the outputted video", default=720)
	manual_compilation_parser.add_argument("--drive", type=bool, help="Save the video to google drive or not", default=False)

	post_parser = subparsers.add_parser("post", help="Generates a video from a reddit post")
	post_parser.add_argument("url", type=str, help="The url to the reddit post (required)")
	post_parser.add_argument("--drive", type=bool, help="Save the video to google drive or not", default=False)

	comments_parser = subparsers.add_parser("comments", help="Generates a video from title and comments")
	comments_parser.add_argument("url", type=str, help="The url to the reddit post (required)")
	comments_parser.add_argument("--comments", type=int, help="Amount of comments to include", default=5)
	comments_parser.add_argument("--drive", type=bool, help="Save the video to google drive or not", default=False)
	
	multiple_posts_parser = subparsers.add_parser("multiple_posts", help="Generates videos from scraped posts")
	multiple_posts_parser.add_argument("subreddit")
	multiple_posts_parser.add_argument("--listing", type=str, help="What listing to use (hot, top etc.)", default="top")
	multiple_posts_parser.add_argument("--limit", type=int, help="How many videos to compile", default=5)
	multiple_posts_parser.add_argument("--timeframe", type=str, help="What timeframe to use (day, week etc)", default="day")
	multiple_posts_parser.add_argument("--drive", type=bool, help="Save the video to google drive or not", default=False)
	
	multiple_comments_parser = subparsers.add_parser("multiple_comments", help="Generates videos from scraped posts with comments")
	multiple_comments_parser.add_argument("subreddit")
	multiple_comments_parser.add_argument("--listing", type=str, help="What listing to use (hot, top etc.)", default="top")
	multiple_comments_parser.add_argument("--limit", type=int, help="How many videos to compile", default=5)
	multiple_comments_parser.add_argument("--timeframe", type=str, help="What timeframe to use (day, week etc)", default="day")
	multiple_comments_parser.add_argument("--comments", type=int, help="Amount of comments to include", default=5)
	multiple_comments_parser.add_argument("--drive", type=bool, help="Save the video to google drive or not", default=False)

	args = parser.parse_args()

	video_maker = VideoMaker()

	if args.action == "auto_compilation":
		video_maker.make_compilation([], args.width, args.height, subreddit=args.subreddit, listing=args.listing, limit=args.limit, timeframe=args.timeframe, drive=args.drive)
	elif args.action == "manual_compilation":
		video_maker.make_compilation(args.urls, args.width, args.height, subreddit=args.subreddit, listing="", limit=0, timeframe="", drive=args.drive)
	elif args.action == "post":
		video_maker.make_post_video(args.url, args.drive)
	elif args.action == "comments":
		video_maker.make_comment_video(args.url, args.comments, args.drive)
	elif args.action == "multiple_posts":
		video_maker.make_multiple_post_videos(args.subreddit, args.listing, args.limit, args.timeframe, args.drive)
	elif args.action == "multiple_comments":
		video_maker.make_multiple_comments_videos(args.subreddit, args.listing, args.limit, args.timeframe, args.comments, args.drive)

if __name__ == "__main__":
	main()