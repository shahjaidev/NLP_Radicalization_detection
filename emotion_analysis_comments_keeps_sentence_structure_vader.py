#Sentiment and Emotion Analysis on Youtube Transcripts based on NRC lexicon

import sys
import nltk
from youtube_transcript_api import YouTubeTranscriptApi
from nltk.stem.snowball import SnowballStemmer

from nltk.stem import WordNetLemmatizer 

from collections import defaultdict

import json
import ast

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer



  
#from scipy.special import softmax
#from sklearn.utils.extmath import softmax

import numpy as np

def softmax(x):
    """Compute softmax values for each sets of scores in x."""
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()


def get_transcript(): #should actually be get_comments()
	#s1="2DG3pMcNNlw"
	#id="stXgn2iZAAY"
	#s2="LfKLV6rmLxE"

		#print(output)
	f=open("islam.txt")
	g= [line.strip("\n") for line in f ]

	all_text= []
	for l in g:
		k=ast.literal_eval(l)
		all_text.append(k["text"])

		#comments=" ".join(all_text)

		#list_comments= comments.split()
	k = open("comments.txt", "w")
	#print("\n".join(all_text))
	k.write( "\n".join(all_text) )
	k.close()
	#return(all_text)
  	

	"""

	except:
  		print("Error occurred")
  		return(None)
  	"""
  		
	
	
def parse_nrc():
	word_emotion_dict={}
	f=open("NRC-Emotion-Lexicon-Senselevel-v0.92.txt")
	list_lines= f.readlines()

	word_emotion_dict={}

	for line in list_lines:
		splitted= line.split("--")
		word=splitted[0]

		word_emotion_dict[word]={}




	for line in list_lines:

		splitted= line.split("--")
		word=splitted[0]

		splitted2= splitted[1].split("\t")
		emot_score=splitted2[-1].strip("\n")
		emot=splitted2[-2]

		word_emotion_dict[word][emot]= emot_score
		#print(splitted2)
		#print(emot)
		#print(emot_score)
		
	return(word_emotion_dict)



def get_transcript_clean_and_organise():
	get_transcript()
	f=open("comments.txt")
	s=f.read()

	s= s.split("\n")
	print(s)
	f.close()
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
	#f = open("comments.txt", "w")
	#print(s_lowercase)
	#print(" ".join(s_lowercase))
	#f.write(" ".join(s_lowercase))
	#f.close()
	return(s_lowercase)
	#return s.split() 

def sentiment_analyzer_scores(sentence):
    score = analyser.polarity_scores(sentence)
    print("{:-<40} {}".format(sentence, str(score)))

def get_emotion_counts():
	num_words_hit=0

	#emot is a dictionaries where the keys are the words and the value is a dictionary with key asd emotions and values a 1/0
	emot= parse_nrc()
	t= get_transcript_clean_and_organise()
	stemmer = SnowballStemmer("english")
	lemmatizer = WordNetLemmatizer() 

	total_count_dict=defaultdict(int)
	#initialises values with integer 0
	analyser = SentimentIntensityAnalyzer()

	#print(nltk.pos_tag(nltk.word_tokenize(s)))
	for line in t:
		#print(line)
		score_dict = analyser.polarity_scores(" ".join(line))
		if(score_dict["pos"]> score_dict["neg"]):
			sentence_flag=1 #indicates 1 if sentence positive, -1 if negative, 0 if neutral
			for wrd in line:
				if wrd in emot.keys():
					if(sentence_flag==1):
						total_count_dict["positive"]=total_count_dict["positive"] + int( emot[wrd]["positive"] )
						total_count_dict["joy"]= total_count_dict["joy"] + int( emot[wrd]["joy"] )
						total_count_dict["trust"]= total_count_dict["trust"] + int( emot[wrd]["trust"] )
					if(sentence_flag==0): #neutral
						total_count_dict["trust"]= total_count_dict["trust"] + int( emot[wrd]["trust"] )

					if(sentence_flag==-1):
						total_count_dict["negative"]=total_count_dict["negative"] + int( emot[wrd]["negative"] )
						total_count_dict["fear"]= total_count_dict["fear"]+ int ( emot[wrd]["fear"] )
						total_count_dict["anger"]= total_count_dict["anger"] + int( emot[wrd]["anger"] )
						total_count_dict["disgust"]= total_count_dict["disgust"] + int( emot[wrd]["disgust"] )

					
					total_count_dict["surprise"]= total_count_dict["surprise"] + int( emot[wrd]["surprise"] )
					total_count_dict["sadness"]= total_count_dict["sadness"] + int( emot[wrd]["sadness"] )
					total_count_dict["anticip"]= total_count_dict["anticip"] + int( emot[wrd]["anticip"] )

					num_words_hit=num_words_hit+1

				else:
					stemmed_word=stemmer.stem(wrd)
					#lemmatized_wrd= lemmatizer.lemmatize("better", pos="a")


					if(stemmed_word in emot.keys()):


						if(sentence_flag==1):
							total_count_dict["positive"]= total_count_dict["positive"] + int( emot[stemmed_word]["positive"] )
							total_count_dict["joy"]= total_count_dict["joy"] + int( emot[stemmed_word]["joy"] )
							total_count_dict["trust"]= total_count_dict["trust"] + int ( emot[stemmed_word]["trust"] )
						if(sentence_flag==0): #neutral
							total_count_dict["trust"]= total_count_dict["trust"] + int ( emot[stemmed_word]["trust"] )

						if(sentence_flag==-1):
							total_count_dict["negative"]=total_count_dict["negative"] + int( emot[stemmed_word]["negative"] )
							total_count_dict["fear"]= total_count_dict["fear"]+ int ( emot[stemmed_word]["fear"] )
							total_count_dict["anger"]= total_count_dict["anger"] + int( emot[stemmed_word]["anger"] )
							total_count_dict["disgust"]= total_count_dict["disgust"] + int( emot[stemmed_word]["disgust"] )

						
						total_count_dict["surprise"]= total_count_dict["surprise"] + int( emot[stemmed_word]["surprise"] )
						total_count_dict["sadness"]= total_count_dict["sadness"] + int( emot[stemmed_word]["sadness"] )
						total_count_dict["anticip"]= total_count_dict["anticip"] + int( emot[stemmed_word]["anticip"] )

						num_words_hit=num_words_hit+1


			
	return(total_count_dict, num_words_hit)



def softmaxed_normalized_emotion_counts():
	normalized_emotion_counts={}
	softmax_counts={}

	total_count_dict, num_words_hit= get_emotion_counts()
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

	for value in normalized_emotion_counts.values():
		value_list.append(value)

	softmax_value_list= softmax(value_list)
	#print(sum(softmax_value_list))
	i=0

	for key in normalized_emotion_counts.keys():

		softmax_counts[key]= softmax_value_list[i]
		i=i+1
	#print(normalized_emotion_counts)
	return(normalized_emotion_counts, softmax_counts)

if __name__=="__main__":

	#id=sys.argv[1]
	#print(get_transcript())
	normalized_counts, softmaxed_counts= softmaxed_normalized_emotion_counts()
	print("Normalized emotion counts: \n")
	print(normalized_counts)
	print("\n Softmaxed emotion counts: \n")
	print(softmaxed_counts)








