import re
import json
import os 
def remove_placeholders(message):
	skip_list = ['<This message was edited>','This message was deleted.',' omitted\n']
	for phrase in skip_list:
		if phrase in message:
			return True
	return False

def replace_users(message, contact_name, user_name,bot_name):
	message = re.sub('Advaith Sridhar', bot_name, message)
	message = re.sub(contact_name, user_name, message)
	return message

def remove_links(message):
	message = re.sub(r"http\S*", '', message)
	return message

def get_user_text(message):
	if ': ' not in message:
		return None,message
	try:
		user, text = message.split(": ", 1)
	except Exception as e:
		print(e)
		print(message)
		return message.split(":")[0],''
	return user, text

def clean_text(text):
	return text.split(":")[0]

def collate_messages(messages, user_name, bot_name, friend_name):
	conversations = []

	fp = 0
	sp = 0
	snippet = ''

	while sp < len(messages):
		if snippet =='':
			og_user,_ = get_user_text(messages[fp])
		cur_user,text = get_user_text(messages[sp])
		if cur_user==og_user or cur_user==None:
			snippet = snippet + clean_text(text)
			sp+=1
		else:
			if og_user==user_name:
				conversations.append({og_user + ' (' + friend_name +')': snippet})
			if og_user==bot_name:
				conversations.append({og_user: snippet})
			snippet=''
			fp = sp

	#Append last conversation
	conversations.append({og_user:snippet})
	return conversations


if __name__ == "__main__":
	user_name='User'
	bot_name='Advaith'
	friend_name = 'Akash'
	contact_name = 'Akash Ramdas US' #'Akash Ramdas US','Vineet Gopakumar','Shubham IITM','Adarsh','Ritu Gala USA', 'Aiswarya Sasi', 'Briti USA', 'Samvida S Venkatesh','Rikkin Majani Flipkart APM'
	with open('../Dataset/'+friend_name+'Chat.txt', encoding="utf-8") as f:
		lines = f.readlines()


	regex = r"\s?\[\d{1,2}\/\d{1,2}\/\d{2,4}\, \d{1,2}:\d{1,2}:\d{1,2}\s[APM]{2}\]\s" #remove timestamps

	dataset = []

	for line in lines:
		message = re.sub(regex, "", line)
		if remove_placeholders(message):
			continue
		message = remove_links(message)
		# message = remove_placeholders(message)
		message = replace_users(message, contact_name, user_name, bot_name)

		dataset.append(message)
		#print(message)

	#print(dataset)
	dataset = collate_messages(dataset, user_name, bot_name, friend_name)
	with open('json_dataset/'+friend_name+'Chat.json', 'w') as file:
		json.dump(dataset, file)