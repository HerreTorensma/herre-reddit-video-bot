# from backend.video_maker import VideoMaker

# video_maker = VideoMaker()

# video_maker.make_image_compilation(1280, 720, "LiminalSpace", "top", 10, "day", False, "music/Controlled_Chaos.mp3", 3.0)

# from backend.scraper import Scraper
# from backend.text_formatter import TextFormatter

# scraper = Scraper()
# page = scraper.get_post_json("https://www.reddit.com/r/offmychest/comments/ze4xj5/is_it_a_red_flag_my_boyfriend_watches_andrew_tate/.json")
# post_data = scraper.get_post_data(page)

# text_formatter = TextFormatter()
# content_lines, formatted_content = text_formatter.format_content([post_data], 50, 5)
# lines, screens = text_formatter.format_text(post_data["body"], 50, 5)

# print(lines)

# print(screens)

from backend.video_maker import VideoMaker

video_maker = VideoMaker()
video_maker.make_transparant_post_video("https://www.reddit.com/r/BestofRedditorUpdates/comments/ze44cz/woman_wants_her_nephews_out_of_her_life_nov_27_22/", False)