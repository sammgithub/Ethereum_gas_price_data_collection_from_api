import requests, datetime, json, time, os, sys, traceback

expiry_date = datetime.datetime(2021, 2, 27, 23, 59, 59)

def get_data():
	r = requests.get('https://www.etherchain.org/api/gasPriceOracle')
	# print(r)
	print(r.status_code, r.text)

	try:
		json_data=r.json()
		# json_data={k:float(v) for k,v in r.json().items()}
		# print(json_data)
		tr_datetime=datetime.datetime.strptime(r.headers['Date'][5:], "%d %b %Y %H:%M:%S %Z")

		row_items=[json_data['safeLow'], json_data['standard'], json_data['fast'], json_data['fastest']]
		row_items.append(r.elapsed)
		row_items.append(tr_datetime)
		row_items.append(tr_datetime.timestamp())
		row_items.extend(str(tr_datetime).split(' '))
		row_items.append(datetime.datetime.utcnow().date())
		row_items.append(datetime.datetime.utcnow().time())
		row_items.append(r.headers['Date'][5:])
		row_items.append(r.url)
		row_items.append('etherchain.org')

		return row_items

	except:
		with open("etherchain_err.log", "a") as file:
			file.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
			file.write("\n")
			file.write(str(r.status_code))
			file.write("\n")
			
			ex_type, ex_value, ex_traceback = sys.exc_info()
			# Extract unformatter stack traces as tuples
			trace_back = traceback.extract_tb(ex_traceback)
			# Format stacktrace
			stack_trace = list()
			for trace in trace_back:
				stack_trace.append("File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3]))
			file.write("Exception type : %s\n " % ex_type.__name__)
			file.write("Exception message : %s\n" %ex_value)
			file.write("Stack trace : %s\n" %stack_trace)			

def export_data(data, addheader=False): # by default False
	with open("etherchain_.csv", "a") as file:
		# if addheader=True and the csv does not have a header, add it
		if addheader and os.stat('etherchain_.csv').st_size<1:
			file.write('safeLow,standard,fast,fastest,elapsedtime,datetime_utc,unixtime,date_utc,time_utc,record_date_utc,record_time_utc,date-GMT,url,sourceoracle\n')
		# export data to csv
		file.write('%s\n' % ','.join([str(e) for e in data]))

def main():
	addheader=True
	while datetime.datetime.now() < expiry_date:
		data = get_data()
		if data is not None:
			export_data(data, addheader)
			print("last run:", datetime.datetime.now())
			addheader=False
		time.sleep(10)

if __name__ == '__main__':
	main()