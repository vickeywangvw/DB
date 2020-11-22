import time
import random
from BTrees.OOBTree import OOBTree


def get_relop(string):
	#get relop from strings
	relop = ""
	if ">=" in string:
		relop = ">="
	elif "<=" in string:
		relop = "<="
	elif "!=" in string:
		relop = "!="
	elif ">" in string:
		relop = ">"
	elif "<" in string:
		relop = "<"
	elif "=" in string:
		relop = "="
	return relop


def read_file(file_name, table):
	#read data file into system
	with open(file_name, 'r') as fp:
		for line in fp:
			line = line.strip('\n').split("|")
			#seperate data with '|'
			for i in range(len(line)):
				if line[i].isdigit():
					#only save data into file
					line[i] = int(line[i])
			table.append(line)


def deal_arithop(row_name, limit):
	#deal with special symbols
	if '+' in row_name:
		constant = int(row_name.split("+")[1])
		row_name = row_name.split("+")[0]
		limit = limit - constant
	elif '-' in row_name:
		constant = int(row_name.split("-")[1])
		row_name = row_name.split("-")[0]
		limit = limit + constant
	elif '*' in row_name:
		constant = int(row_name.split("*")[1])
		row_name = row_name.split("*")[0]
		limit = limit / constant
	elif r'/' in row_name:
		constant = int(row_name.split(r"/")[1])
		row_name = row_name.split(r"/")[0]
		limit = limit * constant
	return row_name, limit


def read_condition(condition, expre, tablename_opera, pre, return_line_number=False):
	#deal with special conditions
	if ">=" in condition:
		row_name, limit = condition.split(">=")
		if limit.isdigit():
			limit = int(limit)
		else:
			row_name, limit = limit, row_name
		row_name, limit = deal_arithop(row_name, limit)
		row_number = expre[tablename_opera][0].index(row_name)
		if return_line_number:
			line_number = []
			for i in range(1, len(expre[tablename_opera])):
				if expre[tablename_opera][i][row_number] >= limit:
					line_number.append(i)
			return line_number
		for line in expre[tablename_opera][1:]:
			if line[row_number] >= limit:
				expre[pre].append(line)
	elif "<=" in condition:
		if "<=" in condition:
			row_name, limit = condition.split("<=")
			if limit.isdigit():
				limit = int(limit)
			else:
				row_name, limit = limit, row_name
			row_name, limit = deal_arithop(row_name, limit)
			row_number = expre[tablename_opera][0].index(row_name)
			if return_line_number:
				line_number = []
				for i in range(1, len(expre[tablename_opera])):
					if expre[tablename_opera][i][row_number] <= limit:
						line_number.append(i)
				return line_number
			for line in expre[tablename_opera][1:]:
				if line[row_number] <= limit:
					expre[pre].append(line)
	elif "!=" in condition:
		if "!=" in condition:
			row_name, limit = condition.split("!=")
			if limit.isdigit():
				limit = int(limit)
			else:
				row_name, limit = limit, row_name
			row_name, limit = deal_arithop(row_name, limit)
			row_number = expre[tablename_opera][0].index(row_name)
			if return_line_number:
				line_number = []
				for i in range(1, len(expre[tablename_opera])):
					if expre[tablename_opera][i][row_number] != limit:
						line_number.append(i)
				return line_number
			for line in expre[tablename_opera][1:]:
				if line[row_number] != limit:
					expre[pre].append(line)
	elif ">" in condition:
		if ">" in condition:
			row_name, limit = condition.split(">")
			if limit.isdigit():
				limit = int(limit)
			else:
				row_name, limit = limit, row_name
			row_name, limit = deal_arithop(row_name, limit)
			row_number = expre[tablename_opera][0].index(row_name)
			if return_line_number:
				line_number = []
				for i in range(1, len(expre[tablename_opera])):
					if expre[tablename_opera][i][row_number] > limit:
						line_number.append(i)
				return line_number
			for line in expre[tablename_opera][1:]:
				if line[row_number] > limit:
					expre[pre].append(line)
	elif "<" in condition:
		if "<" in condition:
			row_name, limit = condition.split("<")
			if limit.isdigit():
				limit = int(limit)
			else:
				row_name, limit = limit, row_name
			row_name, limit = deal_arithop(row_name, limit)
			row_number = expre[tablename_opera][0].index(row_name)
			if return_line_number:
				line_number = []
				for i in range(1, len(expre[tablename_opera])):
					try:
						if expre[tablename_opera][i][row_number] < limit:
							line_number.append(i)
					except TypeError:
						print(expre[tablename_opera][i][row_number], " | ", limit)
						exit()
				return line_number
			for line in expre[tablename_opera][1:]:
				if line[row_number] < limit:
					expre[pre].append(line)
	elif "=" in condition:
		if "=" in condition:
			row_name, limit = condition.split("=")
			if limit.isdigit():
				limit = int(limit)
			else:
				row_name, limit = limit, row_name
			row_name, limit = deal_arithop(row_name, limit)
			row_number = expre[tablename_opera][0].index(row_name)
			if return_line_number:
				line_number = []
				for i in range(1, len(expre[tablename_opera])):
					if expre[tablename_opera][i][row_number] == limit:
						line_number.append(i)
				return line_number
			for line in expre[tablename_opera][1:]:
				if line[row_number] == limit:
					expre[pre].append(line)


def read_condition_for_join(expre, table_1, table_2, relop, column_1_index, column_2_index, pre, return_list=False):
	#read in condition for join command
	j = 0
	answer = []
	for line_right in expre[table_2][1:]:
		i = 0
		j = j + 1
		if relop == ">=":
			for line_left in expre[table_1][1:]:
				i = i + 1
				if line_left[column_1_index] >= line_right[column_2_index]:
					if return_list:
						answer.append((i, j))
					else:
						expre[pre].append(line_left + line_right)
		elif relop == "<=":
			for line_left in expre[table_1][1:]:
				i = i + 1
				if line_left[column_1_index] <= line_right[column_2_index]:
					if return_list:
						answer.append((i, j))
					else:
						expre[pre].append(line_left + line_right)
		elif relop == "!=":
			for line_left in expre[table_1][1:]:
				i = i + 1
				if line_left[column_1_index] != line_right[column_2_index]:
					if return_list:
						answer.append((i, j))
					else:
						expre[pre].append(line_left + line_right)
		elif relop == ">":
			for line_left in expre[table_1][1:]:
				i = i + 1
				if line_left[column_1_index] > line_right[column_2_index]:
					if return_list:
						answer.append((i, j))
					else:
						expre[pre].append(line_left + line_right)
		elif relop == "<":
			for line_left in expre[table_1][1:]:
				i = i + 1
				if line_left[column_1_index] < line_right[column_2_index]:
					if return_list:
						answer.append((i, j))
					else:
						expre[pre].append(line_left + line_right)
		elif relop == "=":
			for line_left in expre[table_1][1:]:
				i = i + 1
				if line_left[column_1_index] == line_right[column_2_index]:
					if return_list:
						answer.append((i, j))
					else:
						expre[pre].append(line_left + line_right)
	if return_list:
		return answer


class HashTable:
	#build hash table to store data
	def __init__(self):
		self.size = 1007
		self.slots = [None for i in range(self.size)]
		self.data = [[] for i in range(self.size)]

	def put(self, key, value):
		hashvalue = self.hashfunction(key, len(self.slots))
		if self.slots[hashvalue] is None:
			self.slots[hashvalue] = key
		self.data[hashvalue].append(value)

	def hashfunction(self, key, size):
		return key % size

	def get(self, key):
		hashvalue = self.hashfunction(key, len(self.slots))
		if self.slots[hashvalue] is None:
			return []
		else:
			return self.data[hashvalue]
def openopfile(path):
	#open operation file in order to execute lots of operations
	with open(path, 'r') as f:
		line=f.readlines();
		opl=[]
		for i in line:
			if '/' in i:
				opl.append(i[:i.index('/')]);
				#each operation is sperated with another by '/' in our inputFile
			else:
				opl.append(i)
	f.close()
	return opl

if __name__ == '__main__':
	expre = {}

	sentlist=openopfile('inputFile.txt');
	#print(sentlist)
	for i in sentlist:#read operations into system
		if i=='\n':
			sentlist.remove(i)

	for sent in sentlist:#clear data in sentlist, so that all elements in sentlist is not null
		if sent == '':
			continue
		if ":=" not in sent:
			#conditions: outputtofile, hash, btree
			func, param = sent.replace(" ", "").split("(")
			param = param[:-1]

			if func == 'outputtofile':
				'''
				    Function: output table to text file
				    Input: table-table to perform operations on; filename(string)-name of the output file
				    Output: None
				    Effect on globals: None
				'''
				start_time = time.time()

				tablename_opera, save_file = param.split(",")
				with open(save_file + '.txt', 'w') as fp:
					for line in expre[tablename_opera]:
						if isinstance(line, list):
							fp.write("|".join(str(i) for i in line))
							fp.write("\n")
						else:
							fp.write(str(line) + "\n")

				end_time = time.time()
				print("Time used: ", end_time - start_time, "ns")

			elif func == 'Btree':
				'''
				    Function: create btree of a column of certain table
				    Input: table-table to perform operations on; table name(string)-name of table; col(string)-column to perform operations on
				    Output: None
				    Effect to globals: btree, btree-index
				    Reference: BTrees
				'''
				start_time = time.time()

				tablename_opera, column_opera = param.split(",")
				column_index = expre[tablename_opera][0].index(column_opera)
				table_opera = expre[tablename_opera]
				global btree_index
				tree = OOBTree()
				#build new tree
				tree.update({-1: table_opera[0]})
				for line in table_opera[1:]:
					k = line[column_index]
					while list(tree.values(k, k)):
						random.seed(k)
						k = k + random.randint(100, 1000)
					tree.update({k: line})

				end_time = time.time()
				print("Time used: ", end_time - start_time, "ns")
			elif func == 'Hash':
				'''
				    Function: create hash of a column of certain table
				    Input: table-table to perform operations on; table name(string)-name of table; col(string)-column to perform operations on
				    Output: None
				    Effect on globals: hash
				'''
				start_time = time.time()

				tablename_opera, column_opera = param.split(",")
				column_index = expre[tablename_opera][0].index(column_opera)
				table_opera = expre[tablename_opera]
				expre[tablename_opera] = HashTable()
				expre[tablename_opera].put(0, table_opera[0])
				for line in table_opera[1:]:
					expre[tablename_opera].put(line[column_index], line)

				end_time = time.time()
				print("Time used: ", end_time - start_time, "ns")
			continue;
		sent = sent.split(":=")
		if(sent[1]!='\n'):
			opera = sent[1].replace(" ", "")

		pre = sent[0].replace(" ", "")  # R1

		#seperate function name, parameters with name of execution result
		devide_pos = opera.index('(') #find index of '('
		func = opera[:devide_pos]#find name of function
		param = opera[devide_pos + 1:-1]#find parameters of the function

		expre[pre] = []

		if func == 'inputfromfile':
			'''
			    Function: read from a text file and 
			    Input: filename(str)-name of the text file
			    Output: data table
			    Effect on globals: None
			'''
			start_time = time.time()

			file = param + '.txt'
			read_file(file, expre[pre])

			end_time = time.time()
			print("Time used: ", end_time - start_time, "ns")

			#print(expre[pre][0:5])

		elif func == 'select':
			'''
			    Function: select rows of table under certain condition
			    Input: table-table to select on; table name(string)-name of table; cond(string)-condition to follow
			    Output: data table
			    Effect on globals: None
			'''
			start_time = time.time()

			tablename_opera, condition = param.split(",")

			if isinstance(expre[tablename_opera], OOBTree):
				column = list(expre[tablename_opera].values(-1))[0]
				#print(column)
				expre[pre].append(column)
				#print(expre[pre])
				column_index = column.index(condition.split("=")[0])
				#print(column_index)
				aim = int(condition.split("=")[1])
				#print(aim)

				search_result = list(expre[tablename_opera].values(aim, aim))
				temp_aim = aim
				while search_result:
					if search_result[0][column_index] == temp_aim:
						expre[pre].append(search_result[0])
					random.seed(aim)
					aim = aim + random.randint(100, 1000)
					search_result = list(expre[tablename_opera].values(aim, aim))

				if expre[pre][0][0] == expre[pre][1][0]:
					expre[pre] = expre[pre][1:]
			elif isinstance(expre[tablename_opera], HashTable):
				column = expre[tablename_opera].get(0)[0]
				expre[pre].append(column)
				column_index = column.index(condition.split("=")[0])
				aim = int(condition.split("=")[1])
				search_result = expre[tablename_opera].get(aim)
				if search_result is not None:
					for i in search_result:
						if i[column_index] == aim:
							expre[pre].append(i)
				if expre[pre][0][0] == expre[pre][1][0]:
					expre[pre] = expre[pre][1:]
			elif ')or(' in param:
				expre[pre].append(expre[tablename_opera][0])
				conditions = condition.split(")or(")
				conditions[0] = conditions[0].replace("(", "")
				conditions[-1] = conditions[-1].replace(")", "")
				list_s = [read_condition(i, expre, tablename_opera, pre, True) for i in conditions]
				list_all = list_s[0]
				for i in list_s:
					list_all = list(set(list_all).union(i))

				for i in list_all:
					expre[pre].append(expre[tablename_opera][i])
			elif ')and(' in param:
				expre[pre].append(expre[tablename_opera][0])
				conditions = condition.split(")and(")
				conditions[0] = conditions[0].replace("(", "")
				conditions[-1] = conditions[-1].replace(")", "")
				list_s = [read_condition(i, expre, tablename_opera, pre, True) for i in conditions]
				list_all = list_s[0]
				for i in list_s:
					list_all = list(set(list_all).intersection(i))

				for i in list_all:
					expre[pre].append(expre[tablename_opera][i])
			else:
				expre[pre].append(expre[tablename_opera][0])
				read_condition(condition, expre, tablename_opera, pre)

			end_time = time.time()
			print("Time used: ", end_time - start_time, "ns")

			#print(expre[pre])

		elif func == 'project':
			'''
			    Function: select certain columns of table withour certain conditions
			    Input: table-table to select on; columns(list)-columns to select
			    Output: data table that contains table after projection
			    Effect on globals: None
			'''
			start_time = time.time()

			tablename_opera = param.split(",")[0]
			table_list = param.split(",")
			row_number = [expre[tablename_opera][0].index(row) for row in table_list[1:]] 

			expre[pre] = []
			for line in expre[tablename_opera]:
				expre[pre].append([line[i] for i in row_number])

			end_time = time.time()
			print("Time used: ", end_time - start_time, "ns")

			#print(expre[pre][0:5])

		elif func == 'avg':
			'''
			    Function: calculate average of a certain column of a table
			    Input: table-table to perform operations on; columns(string)-column to average on
			    Output: data table that contains the average value
			    Effect on globals: None
			'''
			start_time = time.time()

			tablename_opera, row_name = param.split(",") #get table nmae and row name
			row_number = expre[tablename_opera][0].index(row_name)
			avg = 0
			for line in expre[tablename_opera][1:]:
				avg = avg + line[row_number]
			avg = avg / (len(expre[tablename_opera]) - 1)
			expre[pre].append(avg)

			end_time = time.time()
			print("Time used: ", end_time - start_time, "ns")

			#print(expre[pre])

		elif func == 'sum':
			'''
			    Function: take the sum of column of a table
			    Input: table-table to perform operations on; columns(string)-column to sum on
			    Output: data table that contains the sum
			    Effect on globals: None
			'''
			start_time = time.time()

			tablename_opera, row_name = param.split(",")
			row_number = expre[tablename_opera][0].index(row_name)
			row_sum = 0
			for line in expre[tablename_opera][1:]:
				row_sum = row_sum + line[row_number]
			expre[pre].append(row_sum)

			end_time = time.time()
			print("Time used: ", end_time - start_time, "ns")

			#print(expre[pre])

		elif func == 'count':
			'''
			    Function: count the number of rows of a table
			    Input: table-table to perform operations on
			    Output: data table that contains the count of rows
			    Effect on globals: None
			'''
			start_time = time.time()

			tablename_opera= str(param.split())
			tablename_opera=tablename_opera[2] # original tablename_opera is a list, we need to get table name from that list, which is tablename_opera[2]
			#row_number = expre[tablename_opera][0].index()
			num = len(expre[tablename_opera]) - 1
			expre[pre].append(num)

			end_time = time.time()
			print("Time used: ", end_time - start_time, "ns")

			#print(expre[pre])

		elif func == 'sumgroup':
			'''
			    Function: take the sum of a column after group by some other column(s)
			    Input: table-table to perform operations on; sum col(string)-column to sum on; group by col(list)-columns to group by on
			    Output: data table that contains the sum of the sumcol after grouping by gbcol
			    Effect on globals: None
			'''
			start_time = time.time()

			tablename_opera = param.split(",")[0]
			sum_row = param.split(",")[1]
			group_row = param.split(",")[2:]
			sum_row_number = expre[tablename_opera][0].index(sum_row)
			group_row_number = [expre[tablename_opera][0].index(i) for i in group_row]
			max_len = len(expre[tablename_opera])
			mark = [False for i in range(max_len)]
			mark[0] = True
			while False in mark:
				row_sum = 0
				start = mark.index(False)
				first_group_value = [expre[tablename_opera][start][i] for i in group_row_number]
				row_sum = row_sum + expre[tablename_opera][start][sum_row_number]
				mark[start] = True
				start = start + 1

				while start < max_len:
					if [expre[tablename_opera][start][i] for i in group_row_number] == first_group_value:
						row_sum = row_sum + expre[tablename_opera][start][sum_row_number]
						mark[start] = True
					start = start + 1
				expre[pre].append(row_sum)

			end_time = time.time()
			print("Time used: ", end_time - start_time, "ns")

			#print(expre[pre])

		elif func == 'countgroup':
			'''
			    Function: take the count of record of a column after groupby some other column(s)
			    Input: table-table to perform operations on; countcol(string)-column to count on; gbcol(list)-columns to group by on
			    Output: data table that contains the count of records of the countcol after grouping by gbcol
			    Effect on globals: None
			'''
			start_time = time.time()

			tablename_opera = param.split(",")[0]
			sum_row = param.split(",")[1]
			group_row = param.split(",")[2:]
			sum_row_number = expre[tablename_opera][0].index(sum_row)
			group_row_number = [expre[tablename_opera][0].index(i) for i in group_row]
			max_len = len(expre[tablename_opera])
			mark = [False for i in range(max_len)]
			mark[0] = True
			while False in mark:
				count = 0
				start = mark.index(False)
				first_group_value = [expre[tablename_opera][start][i] for i in group_row_number]
				count = count + 1
				mark[start] = True
				start = start + 1

				while start < max_len:
					if [expre[tablename_opera][start][i] for i in group_row_number] == first_group_value:
						count = count + 1
						mark[start] = True
					start = start + 1
				expre[pre].append(count)

			end_time = time.time()
			print("Time used: ", end_time - start_time, "ns")

			#print(expre[pre])

		elif func == 'avggroup':
			'''
			    Function: take the average of a column after groupby some other column(s)
			    Input: table-table to perform operations on; avgcol(string)-column to average on; group by col(list)-columns to group by on
			    Output: data table  that contains the average of the avgcol after grouping by gbcol
			    Effect on globals: None
			'''
			start_time = time.time()

			tablename_opera = param.split(",")[0]
			sum_row = param.split(",")[1]
			group_row = param.split(",")[2:]
			sum_row_number = expre[tablename_opera][0].index(sum_row)
			group_row_number = [expre[tablename_opera][0].index(i) for i in group_row]
			max_len = len(expre[tablename_opera])
			mark = [False for i in range(max_len)]
			mark[0] = True
			while False in mark:
				count = 0
				row_sum = 0
				start = mark.index(False)
				first_group_value = [expre[tablename_opera][start][i] for i in group_row_number]
				row_sum = row_sum + expre[tablename_opera][start][sum_row_number]
				count = count + 1
				mark[start] = True
				start = start + 1

				while start < max_len:
					if [expre[tablename_opera][start][i] for i in group_row_number] == first_group_value:
						row_sum = row_sum + expre[tablename_opera][start][sum_row_number]
						count = count + 1
						mark[start] = True
					start = start + 1
				expre[pre].append(row_sum / count)

			end_time = time.time()
			print("Time used: ", end_time - start_time, "ns")

			#print(expre[pre])

		elif func == 'join':
			'''
			    Function: join two tables based on certain condition
			    Input: table1-left table to join on; 
			    	   name1(string)-name of table1;
			           table2-right table to join on; 
			           name2(string)-name of table2;
			           cond(string)-conditions to join on
			    Output: data table that contains the result after join
			    Effect on globals: None
			'''
			start_time = time.time()

			table_1, table_2, condition = param.split(",")
			if ")and(" in condition:
				conditions = condition.split(")and(")
				conditions[0] = conditions[0].replace("(", "")
				conditions[-1] = conditions[-1].replace(")", "")
				list_s = []
				head_flag = True
				for one_con in conditions:
					relop = get_relop(one_con)
					left_condition, right_condition = one_con.split(relop)
					table_1, column_1 = left_condition.split(".")
					table_2, column_2 = right_condition.split(".")
					if head_flag:
						expre[pre].append(
						[str(table_1) + "_" + str(i) for i in expre[table_1][0]] + [str(table_2) + "_" + str(i) for i in
																					expre[table_2][0]])
						head_flag = False
					column_1_index = expre[table_1][0].index(column_1)
					column_2_index = expre[table_2][0].index(column_2)
					list_s.append(read_condition_for_join(expre, table_1, table_2, relop, column_1_index, column_2_index, pre, True))
				list_all = list_s[0]
				for i in list_s:
					list_all = list(set(list_all).intersection(i))
				for i in list_all:
					expre[pre].append(expre[table_1][i[0]] + expre[table_2][i[1]])

			elif ")or(" in condition:
				conditions = condition.split(")or(")
				conditions[0] = conditions[0].replace("(", "")
				conditions[-1] = conditions[-1].replace(")", "")
				list_s = []
				head_flag = True
				for one_con in conditions:
					relop = get_relop(one_con)
					left_condition, right_condition = one_con.split(relop)
					table_1, column_1 = left_condition.split(".")
					table_2, column_2 = right_condition.split(".")
					if head_flag:
						expre[pre].append(
							[str(table_1) + "_" + str(i) for i in expre[table_1][0]] + [str(table_2) + "_" + str(i) for
																						i in
																						expre[table_2][0]])
						head_flag = False
					column_1_index = expre[table_1][0].index(column_1)
					column_2_index = expre[table_2][0].index(column_2)
					list_s.append(
						read_condition_for_join(expre, table_1, table_2, relop, column_1_index, column_2_index, pre,
												True))
				list_all = list_s[0]
				for i in list_s:
					list_all = list(set(list_all).union(i))
				for i in list_all:
					expre[pre].append(expre[table_1][i[0]] + expre[table_2][i[1]])
			else:
				relop = get_relop(condition)
				left_condition, right_condition = condition.split(relop)
				table_1, column_1 = left_condition.split(".")
				table_2, column_2 = right_condition.split(".")
				expre[pre].append([str(table_1) + "_" + str(i) for i in expre[table_1][0]] + [str(table_2) + "_" + str(i) for i in expre[table_2][0]])
				column_1_index = expre[table_1][0].index(column_1)
				column_2_index = expre[table_2][0].index(column_2)
				read_condition_for_join(expre, table_1, table_2, relop, column_1_index, column_2_index, pre)

			end_time = time.time()
			print("Time used: ", end_time - start_time, "ns")

			#print(expre[pre][0:10])
		elif func == 'sort':
			'''
			    Function: sort a table based on certain columns
			    Input: table-table to perform operations on; cols(list)-columns to sort by
			    Output: data table that contains the table sorted by cols
			    Effect on globals: None
			'''
			start_time = time.time()

			table_row = param.split(",")
			tablename_opera = table_row[0]
			expre[pre].append(expre[tablename_opera][0])

			sort_row_name = table_row[1:]
			sort_row_number = [expre[tablename_opera][0].index(i) for i in sort_row_name]
			expre[pre].append(sorted(expre[tablename_opera][1:], key=lambda x: tuple([x[i] for i in sort_row_number])))

			end_time = time.time()
			print("Time used: ", end_time - start_time, "ns")
			#print(expre[pre][:10])
		elif func == 'concat':
			'''
			    Function: concatenate two tables of the same schema
			    Input: table1-table to perform operations on; 
			    	   table2-table to be concatenated to another table
			    Output:  data table after concatenation
			    Effect on globals: None
			'''
			start_time = time.time()

			table_1, table_2 = param.split(",")
			for line in expre[table_1]:
				expre[pre].append(line)
			for line in expre[table_2][1:]:
				expre[pre].append(line)

			end_time = time.time()
			print("Time used: ", end_time - start_time, "ns")
			#print(expre[pre][:10])
		elif func == 'movsum':
			'''
			    Function: calculate moving sum of a column of certain table
			    Input: table-table to perform operations on; col(string)-column to perform operations on; num(int)-length of moving sum
			    Output: data table that contains the result of moving sum
			    Effect on globals: None
			'''
			start_time = time.time()

			tablename_opera, column_opera, num = param.split(",")
			num = int(num)
			column_index = expre[tablename_opera][0].index(column_opera)
			for line_index in range(1, len(expre[tablename_opera])):
				if line_index < num:
					expre[pre].append(sum([expre[tablename_opera][i][column_index] for i in range(1, int(int(line_index) + 1))]))
				else:
					expre[pre].append(sum([expre[tablename_opera][i][column_index] for i in range(int(int(line_index) - num + 1), int(int(line_index) + 1))]))

			end_time = time.time()
			print("Time used: ", end_time - start_time, "ns")
			#print(expre[pre][:10])
		elif func == 'movavg':
			'''
			    Function: calculate moving average of a column of certain table
			    Input: table-table to perform operations on; col(string)-column to perform operations on; num(int)-length of moving average
			    Output: data table that contains the result of moving average
			    Effect on globals: None
			'''
			start_time = time.time()

			tablename_opera, column_opera, num = param.split(",")
			num = int(num)
			column_index = expre[tablename_opera][0].index(column_opera)
			for line_index in range(1, len(expre[tablename_opera])):
				if line_index < num:
					expre[pre].append(sum([expre[tablename_opera][i][column_index] for i in range(1, int(int(line_index) + 1))]) / line_index)
				else:
					expre[pre].append(sum(
						[expre[tablename_opera][i][column_index] for i in range(int(int(line_index) - num + 1), int(int(line_index) + 1))]) / num)

			end_time = time.time()
			print("Time used: ", end_time - start_time, "ns")
			#print(expre[pre][:10])

			end_time = time.time()
			print("Time used: ", end_time - start_time, "ns")
