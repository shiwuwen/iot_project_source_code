import os

def makeuserdir(username):
	user_base_name = './static/userpic/'
	try:
		os.makedirs(user_base_name+username)
	except OSError as e:
		pass

def removedir(username):
	user_base_name = './static/userpic/'
	try:
		os.rmdir(user_base_name+username)
	except OSError as e:
		pass
		
if __name__ == '__main__':
	makeuserdir('test')