
from get_emotions_september import *
from matplotlib import pyplot as plt
import xlsxwriter 
from get_and_parse_comments import get_comments
from get_and_parse_comments import get_transcript


import sys

if __name__=="__main__":
	#print(get_transcript())


	vader_flag= int( sys.argv[1] ) #commandline arguement to activate / deactivate vader
	workbook = xlsxwriter.Workbook('sequence-August 2019 mexico immigration.xlsx') 

	sheet1 = workbook.add_worksheet() 

	f=open("video_ids_mexico_immigration.txt")
	#g=open("output_scores.txt", "w+")
	i=0
	sheet1.write(i, 0, "video id") #video id
				
	sheet1.write(i, 1, "title") #title
	sheet1.write(i, 2, "views") #views
	sheet1.write(i, 3, "channel") #channel
	sheet1.write(i, 4, "Transcript") #channel
	sheet1.write(i, 5, "Comments") #channel


	sheet1.write(i,6,"Transcript_positive")
	sheet1.write(i,7,"Transcript_negative")
	sheet1.write(i,8,"Transcript_fear")
	sheet1.write(i,9,"Transcript_anger")
	sheet1.write(i,10,"Transcript_neutral_surprise")
	sheet1.write(i,11,"Transcript_negative_surprise")
	sheet1.write(i,12,"Transcript_positive_surprise")
	sheet1.write(i,13,"Transcript_sadness")
	sheet1.write(i,14,"Transcript_disgust")
	sheet1.write(i,15,"Transcript_joy")
	sheet1.write(i,16,"Transcript_positive_anticip")
	sheet1.write(i,17,"Transcript_negative_anticip")
	sheet1.write(i,18,"Transcript_neutral_anticip")
	sheet1.write(i,19,"Transcript_positive_trust")
	sheet1.write(i,20,"Transcript_neutral_trust")

	sheet1.write(i,21,"ParallelDots_Transcript_Excited")
	sheet1.write(i,22,"ParallelDots_Transcript_Bored")
	sheet1.write(i,23,"ParallelDots_Transcript_Happy")
	sheet1.write(i,24,"ParallelDots_Transcript_Fear")
	sheet1.write(i,25,"ParallelDots_Transcript_Angry")
	sheet1.write(i,26,"ParallelDots_Transcript_Sad")

	#Watson

	sheet1.write(i,27,"Transcript_Watson_Tentative")
	sheet1.write(i,28,"Transcript_Watson_Analytical")
	sheet1.write(i,29,"Transcript_Watson_Fear")
	sheet1.write(i,30,"Transcript_Watson_Confident")
	sheet1.write(i,31,"Transcript_Watson_Joy")
	sheet1.write(i,32,"Transcript_Watson_Sadness")
	sheet1.write(i,33,"Transcript_Watson_Anger")
	sheet1.write(i,34,"Transcript_Arousal")


#------------------------------------------------#

	#Comments 
	sheet1.write(i,35,"Comments_positive")
	sheet1.write(i,36,"Comments_negative")
	sheet1.write(i,37,"Comments_fear")
	sheet1.write(i,38,"Comments_anger")
	sheet1.write(i,39,"Comments_neutral_surprise")
	sheet1.write(i,40,"Comments_negative_surprise")
	sheet1.write(i,41,"Comments_positive_surprise")
	sheet1.write(i,42,"Comments_sadness")
	sheet1.write(i,43,"Comments_disgust")
	sheet1.write(i,44,"Comments_joy")
	sheet1.write(i,45,"Comments_positive_anticip")
	sheet1.write(i,46,"Comments_negative_anticip")
	sheet1.write(i,47,"Comments_neutral_anticip")
	sheet1.write(i,48,"Comments_positive_trust")
	sheet1.write(i,49,"Comments_neutral_trust")

	sheet1.write(i,50,"ParallelDots_Comments_Excited")
	sheet1.write(i,51,"ParallelDots_Comments_Bored")
	sheet1.write(i,52,"ParallelDots_Comments_Happy")
	sheet1.write(i,53,"ParallelDots_Comments_Fear")
	sheet1.write(i,54,"ParallelDots_Comments_Angry")
	sheet1.write(i,55,"ParallelDots_Comments_Sad")

	sheet1.write(i,56,"Comments_Watson_Tentative")
	sheet1.write(i,57,"Comments_Watson_Analytical")
	sheet1.write(i,58,"Comments_Watson_Fear")
	sheet1.write(i,59,"Comments_Watson_Confident")
	sheet1.write(i,60,"Comments_Watson_Joy")
	sheet1.write(i,61,"Comments_Watson_Sadness")
	sheet1.write(i,62,"Comments_Watson_Anger")
	sheet1.write(i,63,"Comments_Arousal")

	


	i=1
	for line_str in f:
		transcript_li=None
		comments_li= None
		#each line of the file f is a youtube video id
		line= line_str.split("---")
		video_id= line[0]

		comments_li= None#get_comments(video_id)
		transcript_li=get_transcript(video_id)
		try: 
			sheet1.write(i, 0, line[0]) #video id
			sheet1.write(i, 1, line[1]) #title
			sheet1.write(i, 2, str(line[2])) #views
			sheet1.write(i, 3, line[3]) #channel
			sheet1.write(i,4,str(transcript_li)) #transcript
			#sheet1.write(i,5,str(comments_li)) #transcript
		except:
			sheet1.write(i, 0, line[0]) #video id



		pd_Excited_transcript=0
		pd_Bored_transcript=0
		pd_Happy_transcript=0
		pd_Fear_transcript=0
		pd_Angry_transcript=0
		pd_Sad_transcript=0


		if(transcript_li):
		#print(transcript_li)
			
			text_li= segmenter.segment(" ".join(transcript_li) ) #segmenting unpunctuated transcript to sentences as well as possible

			str_text= ". ".join(text_li) #converting into a single string to easily pass to watson tone analyzer
			#print(str_text)
			
			print("Parallel Dots \n")
			transcript_paralleldots_dict=  get_parallel_dots_emo(text_li)
			print(transcript_paralleldots_dict)



			if transcript_paralleldots_dict:
				pd_Excited_transcript = transcript_paralleldots_dict["Excited"]
				pd_Bored_transcript = transcript_paralleldots_dict["Bored"]
				pd_Happy_transcript = transcript_paralleldots_dict["Happy"]
				pd_Fear_transcript = transcript_paralleldots_dict["Fear"]
				pd_Angry_transcript = transcript_paralleldots_dict["Angry"]
				pd_Sad_transcript = transcript_paralleldots_dict["Sad"]

			
			print("IBM WATSON: ")
			sent_by_sent_transcript_li= str_text.split(".")
			watson_transcript_counts= get_watson_tone_counts(sent_by_sent_transcript_li) 
			print(watson_transcript_counts)
			watson_transcript_tone_defaultdict= defaultdict(int,watson_transcript_counts)

			print("\n\n\n")

			print("NRC")

			normalized_counts_transcript, Arousal_transcript= normalized_emotion_counts(sent_by_sent_transcript_li,vader_flag)

			print("Normalized emotion counts: \n")
			print(normalized_counts_transcript)

			
			print("Arousal Score for Transcript: "+ str(Arousal_transcript))

		

		#-----------------------------------------------------------------------------

		#print("COMMENTS: " + "\n")

		if(comments_li):

			for comment in comments_li:
				if comment[-1] not in string.punctuation:
					comment= comment + ". "

			if len(comments_li) > 950:
				comments_li = comments_li[:950]

			print("COMMENT SCORES: " + "\n")

			print("Ibm_watson")
			watson_comments_tone = get_watson_tone_counts(comments_li)

			#'tentative': 0.14960197692307695, 'analytical': 0.1807689538461538, 'fear': 0.009073753846153845, 'confident': 0.04912628461538461, 'joy': 0.10581765384615383, 'sadness': 0.05242818461538461, 'anger': 0.0056241538461538464}
			
			watson_comments_tone_defaultdict= defaultdict(int,watson_comments_tone)

			print(watson_comments_tone)

			print("\n\n\n")

			comments_paralleldots_dict= get_parallel_dots_emo(comments_li)
			print("Parallel Dots")

			if comments_paralleldots_dict:
				pd_Excited_comments= comments_paralleldots_dict["Excited"]

				pd_Bored_comments= comments_paralleldots_dict["Bored"]

				pd_Happy_comments= comments_paralleldots_dict["Happy"]

				pd_Fear_comments= comments_paralleldots_dict["Fear"]

				pd_Angry_comments= comments_paralleldots_dict["Angry"]

				pd_Sad_comments= comments_paralleldots_dict["Sad"]

			print(comments_paralleldots_dict)

			print("NRC")
			normalized_counts_comments, Arousal_comments= normalized_emotion_counts(comments_li,vader_flag)


			print("Normalized emotion counts: \n")
			print(normalized_counts_comments)

			

		if transcript_li is not None:
			
			"""
			normalized_counts, softmaxed_counts= softmaxed_normalized_emotion_counts(transcript, vader_flag)
			print("Transcript normalized emotion counts: \n")
			print(normalized_counts)
			print("\n Transcript Softmaxed emotion counts: \n")
			print(softmaxed_counts)
			"""

			normalized_counts_transcript= defaultdict(int, normalized_counts_transcript)
			sheet1.write(i,6,normalized_counts_transcript["positive"] ) 
			sheet1.write(i,7,normalized_counts_transcript["negative"])
			sheet1.write(i,8,normalized_counts_transcript["fear"])
			sheet1.write(i,9,normalized_counts_transcript["anger"])
			sheet1.write(i,10,normalized_counts_transcript["neutral_surprise"])
			sheet1.write(i,11,normalized_counts_transcript["negative_surprise"])
			sheet1.write(i,12,normalized_counts_transcript["positive_surprise"])
			sheet1.write(i,13,normalized_counts_transcript["sadness"])
			sheet1.write(i,14,normalized_counts_transcript["disgust"])
			sheet1.write(i,15,normalized_counts_transcript["joy"])
			sheet1.write(i,16,normalized_counts_transcript["positive_anticip"])
			sheet1.write(i,17,normalized_counts_transcript["negative_anticip"])
			sheet1.write(i,18,normalized_counts_transcript["neutral_anticip"])
			sheet1.write(i,19,normalized_counts_transcript["positive_trust"])
			sheet1.write(i,20,normalized_counts_transcript["neutral_trust"])

			sheet1.write(i,21, 	pd_Excited_transcript )
			sheet1.write(i,22,	pd_Bored_transcript)
			sheet1.write(i,23, 	pd_Happy_transcript)
			sheet1.write(i,24, 	pd_Fear_transcript)
			sheet1.write(i,25, 	pd_Angry_transcript )
			sheet1.write(i,26, 	pd_Sad_transcript )

			sheet1.write(i,27,	watson_transcript_tone_defaultdict["tentative"] )
			sheet1.write(i,28,	watson_transcript_tone_defaultdict["analytical"] )
			sheet1.write(i,29,	watson_transcript_tone_defaultdict["fear"] )
			sheet1.write(i,30,	watson_transcript_tone_defaultdict["confident"])
			sheet1.write(i,31,	watson_transcript_tone_defaultdict["joy"] )
			sheet1.write(i,32,	watson_transcript_tone_defaultdict["sadness"] )
			sheet1.write(i,33,	watson_transcript_tone_defaultdict["anger"] )
			sheet1.write(i,34,	Arousal_transcript )


		if comments_li is not None:
			"""
			normalized_counts, softmaxed_counts= softmaxed_normalized_emotion_counts(comments,vader_flag)

			print("Comments normalized emotion counts: \n")
			print(normalized_counts)
			print("\n Comments softmaxed emotion counts: \n")
			print(softmaxed_counts)
			"""
			normalized_counts_comments= defaultdict(int, normalized_counts_comments)

			sheet1.write(i,35,normalized_counts_comments["positive"])
			sheet1.write(i,36,normalized_counts_comments["negative"])
			sheet1.write(i,37,normalized_counts_comments["fear"])
			sheet1.write(i,38,normalized_counts_comments["anger"])
			sheet1.write(i,39,normalized_counts_comments["neutral_surprise"])
			sheet1.write(i,40,normalized_counts_comments["negative_surprise"])
			sheet1.write(i,41,normalized_counts_comments["positive_surprise"])
			sheet1.write(i,42,normalized_counts_comments["sadness"])
			sheet1.write(i,43,normalized_counts_comments["disgust"])
			sheet1.write(i,44,normalized_counts_comments["joy"])
			sheet1.write(i,45,normalized_counts_comments["positive_anticip"])
			sheet1.write(i,46,normalized_counts_comments["negative_anticip"])
			sheet1.write(i,47,normalized_counts_comments["neutral_anticip"])
			sheet1.write(i,48,normalized_counts_comments["positive_trust"])
			sheet1.write(i,49,normalized_counts_comments["neutral_trust"])


			sheet1.write(i,50, 	pd_Excited_comments )
			sheet1.write(i,51,	pd_Bored_comments)
			sheet1.write(i,52, 	pd_Happy_comments)
			sheet1.write(i,53, 	pd_Fear_comments)
			sheet1.write(i,54, 	pd_Angry_comments )
			sheet1.write(i,55, 	pd_Sad_comments )

			sheet1.write(i,56, 	watson_comments_tone_defaultdict["tentative"])
			sheet1.write(i,57, 	watson_comments_tone_defaultdict["analytical"] )
			sheet1.write(i,58, 	watson_comments_tone_defaultdict["fear"] )
			sheet1.write(i,59,	watson_comments_tone_defaultdict["confident"])
			sheet1.write(i,60,	watson_comments_tone_defaultdict["joy"] )
			sheet1.write(i,61,	watson_comments_tone_defaultdict["sadness"] )
			sheet1.write(i,62,	watson_comments_tone_defaultdict["anger"] )
			sheet1.write(i,63,	Arousal_comments )

		i=i+1
	
	workbook.close()

	

 




