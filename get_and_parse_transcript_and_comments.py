#Get and Parse Comments


import sys
import nltk
from youtube_transcript_api import YouTubeTranscriptApi

from collections import defaultdict
import ast
from comment_downloader import *




def get_comments(video_id):
	
	d_main(video_id, "unparsed_comments.txt", 400)
        #d_main downloads user comments for the passed video id upto 400 comments and stores them in unparsed_comments.txt
	
	f=open("unparsed_comments.txt")
	g= [line.strip("\n") for line in f ]
	if g== []:
		return None
	else:
		all_text= []
		for l in g:
			k=ast.literal_eval(l)
			all_text.append(k["text"])

			#comments=" ".join(all_text)

			#list_comments= comments.split()
		k = open("comments.txt", "w")
		#print("\n".join(all_text))
		k.write( "\n".join(all_text) )
		#writes into comments.txt as a string
		
		k.close()
		return(all_text)
	#return(all_text)
  	

  		


def get_transcript(video_id):
	#s1="2DG3pMcNNlw"
	#id="stXgn2iZAAY"
	#s2="LfKLV6rmLxE"
	try:
		output= YouTubeTranscriptApi.get_transcript(video_id)

		print(output)

		l=[]


		for e in output:
			l.append(e['text'])


		print(l)
		#transcript=" ".join(l)

		#list_transcript= transcript.split( )

		#print(list_transcript)

		return(l)
  	



	except:
  		print("An exception occurred")
  		return(None)
	




if __name__=="__main__":

	video_id=sys.argv[1]

	get_comments(video_id)

	get_transcript(video_id)

	
	

