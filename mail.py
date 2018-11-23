import smtplib
import sched, time
s = sched.scheduler(time.time, time.sleep)
def send(): 
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login("rakshith.s.budihal@gmail.com", "7406848092")
 
	msg = "Test!"
	server.sendmail("rakshith.s.budihal@gmail.com", "rakshith.s.budihal@gmail.com", msg)
	server.quit()
	
#send()

def print_some_times():
	print (time.time())
	s.enter(5, 1, send, ())
	s.enter(8, 1, send, ())
	s.run()
	print (time.time())
	
print_some_times()
