##emotion analysis
import json
#from ibm_watson import ToneAnalyzerV3

from watson_developer_cloud import ToneAnalyzerV3

import paralleldots as pd

from deepsegment import DeepSegment

segmenter = DeepSegment('en')

pd.set_api_key( "yGZxjt2pV3Y3V0FizvQGCygybaLHGZRU0rvTNnSLlp8" )

tone_analyzer = ToneAnalyzerV3(
    version='2017-09-21',
    iam_apikey='0DWwlEM6RsPb0nnawbE3Rzbpmrg9OOLcLA5xJOel17wN',
    url='https://gateway-syd.watsonplatform.net/tone-analyzer/api'
)
import string
import sys
import nltk
from youtube_transcript_api import YouTubeTranscriptApi
from nltk.stem.snowball import SnowballStemmer

from nltk.stem import WordNetLemmatizer 

from collections import defaultdict
import numpy as np
import ast

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from get_and_parse_comments import get_comments
from get_and_parse_comments import get_transcript


from collections import defaultdict

def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()



"""
def get_comments_clean_and_organise():
	f=open("comments.txt")
	s=f.read()
	#print(s)
	#s=get_transcript()
	s_lowercase=[]
	sentence=[]
	#s = "".join(" " if x in string.punctuation else x for x in s.lower() )    
	#print(s)
	for line in s: 
		#print(line)
		sentence=[]
		for wrd in line.split():
			sentence.append(wrd.lower() )
			#print(wrd)
		s_lowercase.append(sentence)

	#print(s_lowercase)
	#print(nltk.pos_tag(nltk.word_tokenize(s)))
	#print(s_lowercase)
	
	#print(s_lowercase)
	#print(" ".join(s_lowercase))
	
	return(s_lowercase)
	#return s.split() 
"""
def parse_nrc():
	word_emotion_dict= {}
	f=open("NRC-Emotion-Lexicon-Senselevel-v0.92.txt")
	list_lines= f.readlines()

	emo_dict= {}
	
	for line in list_lines:
		splitted= line.split("--")
		word=splitted[0]

		emo_dict[word]= defaultdict(int)

	#print(emo_dict)
		

	
	
	counter=1
	for line in list_lines:

		
		splitted= line.split("--")
		word=splitted[0]
		#print(word)
		splitted2= splitted[1].split("\t")
		emot_score=splitted2[-1].strip("\n")
		emot=splitted2[-2]
		#print(emot)
		emo_dict[word][emot]= emot_score

		


		if(counter%10==0 and counter>=10):

			#print(emo_dict)
			if( int( emo_dict[word]["positive"] ) >0):
				modified_word=word+"-pos"
				word_emotion_dict[modified_word]=emo_dict[word]
			elif( int( emo_dict[word]["negative"] ) >0):
				modif_word=word +"-neg"
				word_emotion_dict[modif_word]= emo_dict[word]

			else:
				word_emotion_dict[word]= emo_dict[word]
			#emo_dict={}
			
			
		counter=counter+1
		




	#print(word_emotion_dict)

	return(word_emotion_dict)


def read_comments_from_file():
	
	f=open("comments.txt", mode='r',encoding='utf8', newline='\r\n')
	li= f.readlines()
	return(li)




def sentiment_analyzer_scores(sentence):
    score = analyser.polarity_scores(sentence)
    print("{:-<40} {}".format(sentence, str(score)))

def get_emotion_counts_with_vader(li):
	num_words_hit=0
	#emot is a dictionaries where the keys are the words and the value is a dictionary with key asd emotions and values a 1/0
	emot= parse_nrc()
	#t= read_comments_from_file()
	#print(t)
	stemmer = SnowballStemmer("english")
	lemmatizer = WordNetLemmatizer() 

	total_count_dict=defaultdict(int)
	#initialises values with integer 0
	analyser = SentimentIntensityAnalyzer()
	print(li)
	#print(nltk.pos_tag(nltk.word_tokenize(s)))
	f=open("test.txt", 'w')

	for line in li:
		#print(line)
		f.write(line)
		score_dict = analyser.polarity_scores(line)
		if(score_dict["pos"]> score_dict["neg"]):
			sentence_flag=1 #indicates 1 if sentence positive, -1 if negative, 0 if neutral
			print("POSITIVE SENTENCE")
		elif(score_dict["pos"]< score_dict["neg"]):
			sentence_flag=-1
			print("NEGATIVE SENTENCE")
		else:
			sentence_flag=0
			print("NEUTRAL SENTENCE")
		f.write( str(sentence_flag) )
		f.write("\n")
		for wrd in line.split():
			clean_wrd= wrd.strip(string.punctuation)
			lower_wrd= clean_wrd.lower()
			#print(lower_wrd)
			#print(lower_wrd)
			if lower_wrd in emot.keys():
				if(sentence_flag==1):
					modified_word=lower_wrd+"-pos"

					if(emot.get(modified_word, False) == False):
							continue

					total_count_dict["positive"]=total_count_dict["positive"] + int( emot[modified_word].get("positive", 0) )
					total_count_dict["joy"]= total_count_dict["joy"] + int( emot[modified_word].get("joy", 0) )
					total_count_dict["trust"]= total_count_dict["trust"] + int( emot[modified_word].get("trust",0 ) )
					total_count_dict["surprise"]= total_count_dict["surprise"] + int( emot[modified_word].get("surprise",0 ) )
					total_count_dict["anticip"]= total_count_dict["anticip"] + int( emot[modified_word].get("anticip",0) )
				if(sentence_flag==0): #neutral
					total_count_dict["trust"]= total_count_dict["trust"] + int( emot[lower_wrd].get("trust", 0) )
					total_count_dict["surprise"]= total_count_dict["surprise"] + int( emot[lower_wrd].get("surprise",0 ) )
					total_count_dict["anticip"]= total_count_dict["anticip"] + int( emot[lower_wrd].get("anticip",0) )

				if(sentence_flag==-1):
					modified_word=lower_wrd+ "-neg"

					if(emot.get(modified_word, False) == False):
							continue

					total_count_dict["negative"]=total_count_dict["negative"] + int( emot[modified_word].get("negative", 0) )
					total_count_dict["fear"]= total_count_dict["fear"]+ int ( emot[modified_word].get("fear", 0))
					total_count_dict["anger"]= total_count_dict["anger"] + int( emot[modified_word].get("anger", 0) )
					total_count_dict["disgust"]= total_count_dict["disgust"] + int( emot[modified_word].get("disgust", 0) )
					total_count_dict["surprise"]= total_count_dict["surprise"] + int( emot[modified_word].get("surprise", 0) )
					total_count_dict["sadness"]= total_count_dict["sadness"] + int( emot[modified_word].get("sadness", 0) )
					total_count_dict["anticip"]= total_count_dict["anticip"] + int( emot[modified_word].get("anticip", 0) )
		


				
				

				num_words_hit=num_words_hit+1

			else:
				stemmed_word=stemmer.stem(lower_wrd)
				#lemmatized_wrd= lemmatizer.lemmatize("better", pos="a")


				if(stemmed_word in emot.keys()):


					if(sentence_flag==1):
						modified_word=stemmed_word+"-pos"
						if(emot.get(modified_word, False) == False):
							continue
						total_count_dict["positive"]=total_count_dict["positive"] + int( emot[modified_word].get("positive", 0) )
						total_count_dict["joy"]= total_count_dict["joy"] + int( emot[modified_word].get("joy", 0) )
						total_count_dict["trust"]= total_count_dict["trust"] + int( emot[modified_word].get("trust",0 ) )
						total_count_dict["surprise"]= total_count_dict["surprise"] + int( emot[modified_word].get("surprise",0 ) )
						total_count_dict["anticip"]= total_count_dict["anticip"] + int( emot[modified_word].get("anticip",0) )
					if(sentence_flag==0): #neutral
						total_count_dict["trust"]= total_count_dict["trust"] + int( emot[stemmed_word].get("trust", 0) )
						total_count_dict["surprise"]= total_count_dict["surprise"] + int( emot[stemmed_word].get("surprise",0 ) )
						total_count_dict["anticip"]= total_count_dict["anticip"] + int( emot[stemmed_word].get("anticip",0) )

					if(sentence_flag==-1):
						modified_word=stemmed_word+ "-neg"
						if(emot.get(modified_word, False) == False):
							continue
						total_count_dict["negative"]=total_count_dict["negative"] + int( emot[modified_word].get("negative", 0) )
						total_count_dict["fear"]= total_count_dict["fear"]+ int ( emot[modified_word].get("fear", 0))
						total_count_dict["anger"]= total_count_dict["anger"] + int( emot[modified_word].get("anger", 0) )
						total_count_dict["disgust"]= total_count_dict["disgust"] + int( emot[modified_word].get("disgust", 0) )
						total_count_dict["surprise"]= total_count_dict["surprise"] + int( emot[modified_word].get("surprise", 0) )
						total_count_dict["sadness"]= total_count_dict["sadness"] + int( emot[modified_word].get("sadness", 0) )
						total_count_dict["anticip"]= total_count_dict["anticip"] + int( emot[modified_word].get("anticip", 0) )
					
					num_words_hit=num_words_hit+1


		
	return(total_count_dict, num_words_hit)

def get_emotion_counts(li,vader_flag=1):
	if(vader_flag)==1:
		return(get_emotion_counts_with_vader(li))
	else:
		return(get_emotion_counts_without_vader(li))


def get_emotion_counts_without_vader(li):

	num_words_hit=0
	#emot is a dictionaries where the keys are the words and the value is a dictionary with key asd emotions and values a 1/0
	emot= parse_nrc()
	#t= read_comments_from_file()
	#print(t)
	stemmer = SnowballStemmer("english")
	lemmatizer = WordNetLemmatizer() 

	total_count_dict=defaultdict(int)
	#initialises values with integer 0
	analyser = SentimentIntensityAnalyzer()
	#print(li)
	#print(nltk.pos_tag(nltk.word_tokenize(s)))


	for line in li:
		#print(line)
		for wrd in line.split():
			clean_wrd= wrd.strip(string.punctuation)
			lower_wrd= clean_wrd.lower()
			#print(lower_wrd)
			#print(lower_wrd)
			if lower_wrd in emot.keys():
				total_count_dict["positive"]=total_count_dict["positive"] + int( emot[lower_wrd]["positive"] )
				total_count_dict["joy"]= total_count_dict["joy"] + int( emot[lower_wrd]["joy"] )
				total_count_dict["trust"]= total_count_dict["trust"] + int( emot[lower_wrd]["trust"] )

				total_count_dict["negative"]=total_count_dict["negative"] + int( emot[lower_wrd]["negative"] )
				total_count_dict["fear"]= total_count_dict["fear"]+ int ( emot[lower_wrd]["fear"] )
				total_count_dict["anger"]= total_count_dict["anger"] + int( emot[lower_wrd]["anger"] )
				total_count_dict["disgust"]= total_count_dict["disgust"] + int( emot[lower_wrd]["disgust"] )

			
				total_count_dict["surprise"]= total_count_dict["surprise"] + int( emot[lower_wrd]["surprise"] )
				total_count_dict["sadness"]= total_count_dict["sadness"] + int( emot[lower_wrd]["sadness"] )
				total_count_dict["anticip"]= total_count_dict["anticip"] + int( emot[lower_wrd]["anticip"] )

				num_words_hit=num_words_hit+1

			else:
				stemmed_word=stemmer.stem(lower_wrd)
				#lemmatized_wrd= lemmatizer.lemmatize("better", pos="a")


				if(stemmed_word in emot.keys()):

					total_count_dict["positive"]= total_count_dict["positive"] + int( emot[stemmed_word]["positive"] )
					total_count_dict["joy"]= total_count_dict["joy"] + int( emot[stemmed_word]["joy"] )
					total_count_dict["trust"]= total_count_dict["trust"] + int ( emot[stemmed_word]["trust"] )

					total_count_dict["negative"]=total_count_dict["negative"] + int( emot[stemmed_word]["negative"] )
					total_count_dict["fear"]= total_count_dict["fear"]+ int ( emot[stemmed_word]["fear"] )
					total_count_dict["anger"]= total_count_dict["anger"] + int( emot[stemmed_word]["anger"] )
					total_count_dict["disgust"]= total_count_dict["disgust"] + int( emot[stemmed_word]["disgust"] )

				
					total_count_dict["surprise"]= total_count_dict["surprise"] + int( emot[stemmed_word]["surprise"] )
					total_count_dict["sadness"]= total_count_dict["sadness"] + int( emot[stemmed_word]["sadness"] )
					total_count_dict["anticip"]= total_count_dict["anticip"] + int( emot[stemmed_word]["anticip"] )

					num_words_hit=num_words_hit+1


		
	return(total_count_dict, num_words_hit)
	

def get_watson_counts(text):



	tone = tone_analyzer.tone(
    {'text': text},
    content_type='application/json').get_result()

	#print(tone)
	#print("\n")
	#print(json.dumps(tone, indent=2))

	return(tone)


def get_parallel_dots_emo(transcript_li):
	total_emot_dict=defaultdict(int)
	line_counter=1
	try:
		for line in transcript_li:
			line_score_dict= pd.emotion( line )['emotion']
			print(line_score_dict)
			total_emot_dict["Excited"]+= line_score_dict["Excited"]
			total_emot_dict["Bored"]+= line_score_dict["Bored"]
			total_emot_dict["Happy"]+= line_score_dict["Happy"]
			total_emot_dict["Fear"]+= line_score_dict["Fear"]
			total_emot_dict["Angry"]+= line_score_dict["Angry"]
			total_emot_dict["Sad"]+= line_score_dict["Sad"]


			line_counter+=1


	except:
		normalized_total_emot_dict = {k: v / line_counter for k, v in total_emot_dict.items()}
		return normalized_total_emot_dict

	normalized_total_emot_dict = {k: v / line_counter for k, v in total_emot_dict.items()} #dividing each value by total number of sentences processed
	return normalized_total_emot_dict

def softmaxed_normalized_emotion_counts(li,vader_flag=1):
	normalized_emotion_counts={}
	softmax_counts={}

	total_count_dict, num_words_hit= get_emotion_counts(li,vader_flag)
	normalized_emotion_counts["positive"]= total_count_dict["positive"]/ num_words_hit
	normalized_emotion_counts["negative"]= total_count_dict["negative"]/ num_words_hit
	normalized_emotion_counts["fear"]= total_count_dict["fear"]/ num_words_hit
	normalized_emotion_counts["anger"]= total_count_dict["anger"]/ num_words_hit
	normalized_emotion_counts["surprise"]= total_count_dict["surprise"]/ num_words_hit
	normalized_emotion_counts["sadness"]= total_count_dict["sadness"]/ num_words_hit
	normalized_emotion_counts["disgust"]= total_count_dict["disgust"]/ num_words_hit
	normalized_emotion_counts["joy"]= total_count_dict["joy"]/ num_words_hit
	normalized_emotion_counts["anticip"]= total_count_dict["anticip"]/ num_words_hit
	normalized_emotion_counts["trust"]= total_count_dict["trust"]/ num_words_hit

	value_list=[]
	#print(normalized_emotion_counts)
	for value in normalized_emotion_counts.values():
		value_list.append(value)


	#print(value_list)
	sentiment_list=value_list[:2]
	emotion_list=value_list[2:]
	
	softmax_sentiment_list= softmax(sentiment_list)
	print(softmax_sentiment_list)
	softmax_emotion_list= softmax(emotion_list)
	print(softmax_emotion_list)
	#print(sum(softmax_value_list))
	softmax_counts["positive"]= softmax_sentiment_list[0]
	softmax_counts["negative"]= softmax_sentiment_list[1]
	softmax_counts["fear"]= softmax_emotion_list[0]
	softmax_counts["anger"]= softmax_emotion_list[1]
	softmax_counts["surprise"]= softmax_emotion_list[2]
	softmax_counts["sadness"]= softmax_emotion_list[3]
	softmax_counts["disgust"]= softmax_emotion_list[4]
	softmax_counts["joy"]= softmax_emotion_list[5]
	softmax_counts["anticip"]= softmax_emotion_list[6]
	softmax_counts["trust"]= softmax_emotion_list[7]
	"""
	i=0

	for key in normalized_emotion_counts.keys():

		softmax_counts[key]= softmax_value_list[i]
		i=i+1
	#print(normalized_emotion_counts)
	"""

	return(normalized_emotion_counts, softmax_counts)


if __name__=="__main__":

	video_id=sys.argv[1]

	vader_flag=1
	#print(get_transcript())
	#get_comments_clean_and_organise()

	print( "TRANSCRIPT" + "\n")
	transcript_li= get_transcript(video_id)

	text_li= segmenter.segment(" ".join(transcript_li) )
	#print(text_li)

	str_text= ". ".join(text_li) #converting into a single string to easily pass to watson tone analyzer
	#print(str_text)
	
	print("Parallel Dots \n")

	paralleldots_dict=  get_parallel_dots_emo(transcript_li)
	print(paralleldots_dict)


	print("IBM WATSON: ")
	print( get_watson_counts(str_text) )

	print("\n\n\n")
	print("NRC")
	sent_by_sent_transcript_li= str_text.split(".")
	normalized_counts_transcript, softmaxed_counts_transcript= softmaxed_normalized_emotion_counts(sent_by_sent_transcript_li,vader_flag)
	print("Normalized emotion counts: \n")
	print(normalized_counts_transcript)
	print("\n Softmaxed emotion counts: \n")
	print(softmaxed_counts_transcript)

	print("\n\n")

	print("COMMENTS: " + "\n")
	comments_li=get_comments(video_id)
	normalized_counts_comments, softmaxed_counts_comments= softmaxed_normalized_emotion_counts(comments_li,vader_flag)
	
	print("COMMENT SCORES: " + "\n")

	print("Ibm_watson")

	print( get_watson_counts(". ".join(comments_li)) )

	print("\n\n\n")


	print()


	print("NRC")
	print("Normalized emotion counts: \n")
	print(normalized_counts_comments)
	print("\n Softmaxed emotion counts: \n")
	print(softmaxed_counts_comments)



