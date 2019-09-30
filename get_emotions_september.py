##emotion analysis
import json
#from ibm_watson import ToneAnalyzerV3
import numpy
import string
from watson_developer_cloud import ToneAnalyzerV3

import paralleldots as pd

from deepsegment import DeepSegment

from ibm_watson import NaturalLanguageUnderstandingV1

from ibm_watson.natural_language_understanding_v1 \
    import Features, EntitiesOptions, KeywordsOptions

natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2019-07-12',
    iam_apikey='oRW-WiI73HQMQxq0mVZnPJzN3UFwX4-9oD-XpjLjqUNi',
    url='https://gateway-wdc.watsonplatform.net/natural-language-understanding/api')


segmenter = DeepSegment('en')

pd.set_api_key( "Mf5Rgw0kBSWSNThFQxKYbEQvPgKgrexUKqPEPDMwGkM" )

tone_analyzer = ToneAnalyzerV3(
    version='2017-09-21',
    iam_apikey='E8dobLcUUvh7NZU6MzpFv-GDUiIuEmOV43vQIWSNO0tE',
    url='https://gateway-wdc.watsonplatform.net/tone-analyzer/api'
)

import sys
import nltk
from youtube_transcript_api import YouTubeTranscriptApi
from nltk.stem.snowball import SnowballStemmer

from nltk.stem import WordNetLemmatizer 

from collections import defaultdict

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
	pos_sentence_count=0
	neg_sentence_count=0

	total_count_dict=defaultdict(int)
	#initialises values with integer 0
	analyser = SentimentIntensityAnalyzer()
	print(li)
	#print(nltk.pos_tag(nltk.word_tokenize(s)))
	f=open("test.txt", 'w')

	for line in li:
		#print(line)
		if line == '':
			continue

		f.write(line)
		score_dict = analyser.polarity_scores(line)
		compound_score= score_dict["compound"]
		if(compound_score >0.05):
			sentence_flag=1 #indicates 1 if sentence positive, -1 if negative, 0 if neutral
			print("POSITIVE SENTENCE")
			pos_sentence_count+=1
		elif(compound_score <-0.05):
			sentence_flag=-1
			neg_sentence_count+=1

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
				if(sentence_flag==1): #positive sentence
					modified_word=lower_wrd+"-pos"

					if(emot.get(modified_word, False) == False):
						modified_word=lower_wrd
						if(emot.get(modified_word, False) == False):
							continue

					total_count_dict["positive"]=total_count_dict["positive"] + int( emot[modified_word].get("positive", 0) )
					total_count_dict["joy"]= total_count_dict["joy"] + int( emot[modified_word].get("joy", 0) )* compound_score
					total_count_dict["positive_trust"]= total_count_dict["positive_trust"] + int( emot[modified_word].get("trust",0 ) )* compound_score

					total_count_dict["positive_surprise"]= total_count_dict["positive_surprise"] + int( emot[modified_word].get("surprise",0 ) )* compound_score
					total_count_dict["positive_anticipation"]= total_count_dict["positive_anticipation"] + int( emot[modified_word].get("anticip",0) )* compound_score
				

				if(sentence_flag==0): #neutral
					total_count_dict["neutral_trust"]= total_count_dict["neutral_trust"] + int( emot[lower_wrd].get("trust", 0) )
					total_count_dict["neutral_surprise"]= total_count_dict["neutral_surprise"] + int( emot[lower_wrd].get("surprise",0 ) )
					total_count_dict["neutral_anticip"]= total_count_dict["neutral_anticip"] + int( emot[lower_wrd].get("anticip",0) )

				if(sentence_flag==-1):
					modified_word=lower_wrd+ "-neg"

					if(emot.get(modified_word, False) == False):
							modified_word=lower_wrd
							if(emot.get(modified_word, False) == False):
								continue

					total_count_dict["negative"]=total_count_dict["negative"] + int( emot[modified_word].get("negative", 0) )
					total_count_dict["fear"]= total_count_dict["fear"]+ int ( emot[modified_word].get("fear", 0))* (-1 * compound_score)
					total_count_dict["anger"]= total_count_dict["anger"] + int( emot[modified_word].get("anger", 0) ) * (-1 * compound_score)
					total_count_dict["disgust"]= total_count_dict["disgust"] + int( emot[modified_word].get("disgust", 0) ) * (-1 * compound_score)
					total_count_dict["negative_surprise"]= total_count_dict["negative_surprise"] + int( emot[modified_word].get("surprise", 0) )* (-1 * compound_score)
					total_count_dict["sadness"]= total_count_dict["sadness"] + int( emot[modified_word].get("sadness", 0) ) * (-1 * compound_score)
					total_count_dict["negative_anticipation"]= total_count_dict["negative_anticip"] + int( emot[modified_word].get("anticip", 0) ) * (-1 * compound_score)
		


				
				

				num_words_hit=num_words_hit+1

			else:
				stemmed_word=stemmer.stem(lower_wrd)
				#lemmatized_wrd= lemmatizer.lemmatize("better", pos="a")


				if(stemmed_word in emot.keys()):


					if(sentence_flag==1):
						modified_word=stemmed_word+"-pos"
						if(emot.get(modified_word, False) == False):
							modified_word=lower_wrd
							if(emot.get(modified_word, False) == False):
								continue


	
						total_count_dict["joy"]= total_count_dict["joy"] + int( emot[modified_word].get("joy", 0) )* compound_score
						total_count_dict["positive_trust"]= total_count_dict["positive_trust"] + int( emot[modified_word].get("trust",0 ) )* compound_score

						total_count_dict["positive_surprise"]= total_count_dict["positive_surprise"] + int( emot[modified_word].get("surprise",0 ) )* compound_score
						total_count_dict["positive_anticip"]= total_count_dict["positive_anticip"] + int( emot[modified_word].get("anticip",0) )* compound_score
					

					if(sentence_flag==0): #neutral
						total_count_dict["neutral_trust"]= total_count_dict["neutral_trust"] + int( emot[stemmed_word].get("trust", 0) )
						total_count_dict["neutral_surprise"]= total_count_dict["neutral_surprise"] + int( emot[stemmed_word].get("surprise",0 ) )
						total_count_dict["neutral_anticip"]= total_count_dict["neutral_anticip"] + int( emot[stemmed_word].get("anticip",0) )

					if(sentence_flag==-1):
						modified_word=stemmed_word+ "-neg"
						if(emot.get(modified_word, False) == False):
							modified_word=lower_wrd
							if(emot.get(modified_word, False) == False):
								continue
							

						total_count_dict["negative"]=total_count_dict["negative"] + int( emot[modified_word].get("negative", 0) )
						total_count_dict["fear"]= total_count_dict["fear"]+ int ( emot[modified_word].get("fear", 0))* (-1 * compound_score)
						total_count_dict["anger"]= total_count_dict["anger"] + int( emot[modified_word].get("anger", 0) ) * (-1 * compound_score)
						total_count_dict["disgust"]= total_count_dict["disgust"] + int( emot[modified_word].get("disgust", 0) ) * (-1 * compound_score)
						total_count_dict["negative_surprise"]= total_count_dict["negative_surprise"] + int( emot[modified_word].get("surprise", 0) )* (-1 * compound_score)
						total_count_dict["sadness"]= total_count_dict["sadness"] + int( emot[modified_word].get("sadness", 0) ) * (-1 * compound_score)
						total_count_dict["negative_anticip"]= total_count_dict["negative_anticip"] + int( emot[modified_word].get("anticip", 0) ) * (-1 * compound_score)
			

					
					num_words_hit=num_words_hit+1

	if((neg_sentence_count + pos_sentence_count) != 0):
		arousal= abs(neg_sentence_count - pos_sentence_count)/ (neg_sentence_count + pos_sentence_count)
	else:
		arousal= "cannot. calculate"


	return(total_count_dict, num_words_hit, arousal)

def get_emotion_counts(li,vader_flag=1):
	if(vader_flag)==1:
		return(get_emotion_counts_with_vader(li))
	else:
		return(get_emotion_counts_without_vader(li))


def get_watson_tone_counts(sent_by_sent_transcript_li):

	overall_tone_dict=defaultdict(int)
	"""
	line_counter=0
	cleaned_list=[]
	for line in sent_by_sent_transcript_li:
		if (line):
			cleaned_list.append(line)
			line_counter+=1
	print(cleaned_list)
	print(len(cleaned_list))
	transcript_batches = numpy.array_split(cleaned_list, len(cleaned_list)% 100 + 1)
	print(len(transcript_batches))
	"""
	"""
	for batch in transcript_batches:
		
		print(punctuated_batch)
		tone_object = tone_analyzer.tone( {'text': punctuated_batch},content_type='application/json').get_result()
		print(tone_object)
		for sentence_dict in tone_object["sentences_tone"]:
			for tone_dict in sentence_dict["tones"]:
				tone_id= tone_dict["tone_id"]
				overall_tone_dict[tone_id]+= tone_dict["score"] 
	
	"""

	tone_object = tone_analyzer.tone( {'text': ". ".join(sent_by_sent_transcript_li)},content_type='application/json').get_result()
	print(tone_object)
	try:
		for sentence_dict in tone_object["sentences_tone"]:
				for tone_dict in sentence_dict["tones"]:
					tone_id= tone_dict["tone_id"]
					overall_tone_dict[tone_id]+= tone_dict["score"] 
		

		line_counter= len(sent_by_sent_transcript_li)
		normalized_overall_tone_dict = {k: v / line_counter for k, v in overall_tone_dict.items()}
		return(normalized_overall_tone_dict)
	except:
		print ("Exception occurred while using watson API- bad transcript ")
		empty_dict={}
		return empty_dict

	


def get_parallel_dots_emo(transcript_li):


	total_emot_dict=defaultdict(int)
	line_counter=1
	try:
		for line in transcript_li:
			if (line):
				print(line)
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

def normalized_emotion_counts(li,vader_flag):

	total_count_dict, num_words_hit, arousal= get_emotion_counts(li,vader_flag)
	normalized_total_emot_dict = {k: v / num_words_hit for k, v in total_count_dict.items()}

	softmax_counts={}


	emotion_list=[]
	#print(normalized_emotion_counts)
	for value in normalized_total_emot_dict.values():
		emotion_list.append(value)

	print(normalized_total_emot_dict)
	#print(value_list)

	"""
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
	return(normalized_total_emot_dict, arousal)


"""
def get_watson_emotion_counts(transcript_li):
	watson_emot_dict=defaultdict(int)
	for sentence in transcript_li:
		print(sentence)
		#json.dumps(response)

		response = natural_language_understanding.analyze(
	    text= sentence,
	    features=Features(
	        entities=EntitiesOptions(emotion=True, sentiment=True, limit=2),
	        keywords=KeywordsOptions(emotion=True, sentiment=True,
	                                 limit=2))).get_result()

		print(response)
		watson_emot_dict['sadness'] = watson_emot_dict['sadness'] + response['entities']['emotion']['sadness']
		watson_emot_dict['joy'] = watson_emot_dict['joy'] + response['entities']['emotion']['joy']
		watson_emot_dict['fear'] = watson_emot_dict['fear'] + response['entities']['emotion']['fear']
		watson_emot_dict['disgust'] = watson_emot_dict['disgust'] + response['entities']['emotion']['disgust']
		watson_emot_dict['anger'] = watson_emot_dict['anger'] + response['entities']['emotion']['anger']

		return (watson_emot_dict)


"""


if __name__=="__main__":

	video_id=sys.argv[1]

	vader_flag=1
	#print(get_transcript())
	#get_comments_clean_and_organise()

	print( "TRANSCRIPT" + "\n")
	transcript_li= get_transcript(video_id)

	segmented_text_li= segmenter.segment(" ".join(transcript_li) )
	print(segmented_text_li)

	str_text= ". ".join(segmented_text_li) #converting into a single string to easily pass to watson tone analyzer
	#print(str_text)
	

	print("NRC")
	sent_by_sent_transcript_li= segmented_text_li
	normalized_counts_transcript, Arousal= normalized_emotion_counts(sent_by_sent_transcript_li,vader_flag)
	print("Normalized emotion counts of transcript: \n")
	print(normalized_counts_transcript)
	print("Arousal Score: "+ str(Arousal))

	print("Parallel Dots \n")

	paralleldots_dict=  get_parallel_dots_emo(sent_by_sent_transcript_li)
	print(paralleldots_dict)


	print("IBM WATSON Tone Analyzer: ")
	#print(sent_by_sent_transcript_li)

	print( get_watson_tone_counts(sent_by_sent_transcript_li) )

	print("\n\n\n")
	
	print("COMMENTS: " + "\n")
	comments_li=get_comments(video_id)
	
	
	print("COMMENT SCORES: " + "\n")

	

	#pre-processing
	for comment in comments_li:
		if comment[-1] not in string.punctuation:
			comment= comment + ". "

	if len(comments_li) > 950:
		comments_li=comments_li[:950]

	print(comments_li)



	#comments_concatenated_with_periods= ". ".join(comments_li)


	print("Ibm Watson: ")

	print( get_watson_tone_counts(comments_li))

	print("\n\n\n")

	print("NRC")
	print("Normalized emotion counts of comments: \n")


	normalized_comments, Arousal_comments= normalized_emotion_counts(comments_li,vader_flag)
	print(normalized_comments)
	print("Arousal of comments:")
	print(Arousal_comments)




