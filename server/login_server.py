import pymysql

def login(data):

	db = pymysql.connect("localhost","root","12345678","userdb",charset="utf8")
	cur = db.cursor()
	data = data.split(' ')
	print("data:",data)
	if data[1] == '' or data[2] == '':
		return 'try agian'
	sql_select = r"select name,pwds from logintab where  name = '%s'"%(data[1])
	cur.execute(sql_select)
	db.commit()

	name = cur.fetchone()	
	print("data:",name)

	sql_select = r"select name,pwds from logintab where  name = '%s'  and pwds = '%s';"%(data[1],data[2])
	cur.execute(sql_select)
	db.commit()
	name_pwds = cur.fetchone()

	print("data2:",name_pwds)

	if name !=None:
		if name_pwds != None:	
			print('ok1')	
			return 'ok usrname password'
		else:
			return 'password error'
	else:
		sql_select = r"insert into logintab (name,pwds) values('%s','%s');"%(data[1],data[2])
		cur.execute(sql_select)
		db.commit()
		print('ok2')		
		return 'ok usrname password'



	
	# if data3 == ():
	# 	print("true",type(data3))
	# print("fetchall的结果为",data3)

	