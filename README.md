Data Science Institute Scholar Project
Jaidev Shah, Columbia SEAS '21

### Dependencies
* Python 3+
* requests
* lxml
* cssselect

The python packages can be installed with

    pip install requests
    pip install lxml
    pip install cssselect



### Script to collect sequence data:

python smart_autoplay_sequence.py --query="immigration" --searches=1 --branch=1 --depth=5 --name="immigration"

Note: Video_Ids stored in a txt file called video_ids.txt

### Script to analyse emotions: 

python analyse_sequence.py 1

(Passing in the 1 or 0 tells the script to look at sentiment on a sentence level using Vader, and thereby make decisions on putting emotions into 13 emotion categories)

Dependencies:
from get_emotions_september import *
from matplotlib import pyplot as plt
import xlsxwriter 
from get_and_parse_comments import get_comments
from get_and_parse_comments import get_transcript


### File containing emotion analysis funtions

get_emotions.py

### Script to scrape and parse comments as well as transcript

get_and_parse_comments.py




### Religion, Race and self-created dictionaries (contains commonly used social media words in those fields, and derogatory slurs)

religion.txt
race.txt






