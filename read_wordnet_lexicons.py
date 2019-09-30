import ast
import json
import yaml

if __name__=="__main__":

	f=open("Lexicons/race/asian_2.txt")
	
	s = f.readline().strip("\n")
	asian_dict={}
	asian_dict[s]=[]

	for line in f:
		asian_dict[s].append(line.strip("\n"))

	print(s)
	#asian_dict = ast.literal_eval(s)
	#asian_dict= eval(s)
	#asian_dict = json.load(f)
	print(asian_dict)

