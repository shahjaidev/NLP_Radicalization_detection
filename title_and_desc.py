from bs4 import BeautifulSoup
import requests
import csv
import pafy


csv_file = open('Titles_and_Descriptions.csv','w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Title', 'Description'])

f=open("video_ids.txt")

for line_str in f:
	line= line_str.split("---")
	video_id= line[0]
	#comments=get_comments(video_id)
	#transcript=get_transcript(video_id)
	video_str= "https://www.youtube.com/watch?v=" + video_id
	pafy_video = pafy.new(video_str)
	title= pafy_video.title
	description= pafy_video.description 
	csv_writer.writerow( [title, description] )

csv_file.close()
f.close()


