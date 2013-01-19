#!/usr/bin/python
"This is a hello world script that is used to test bin"

def hello_world():
    name = raw_input('What is your name?')
    if name == '':
        name = 'World'
    print "Hello, %s." % name

hello_world()
