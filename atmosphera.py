#!/usr/bin/env python3
from bottle import get, post, request, run, static_file
from os import listdir
from os.path import expanduser, isdir, join
from socket import gethostbyname, gethostname
from sys import argv

try: host = argv[1]
except: host = gethostbyname(gethostname())
try: root = argv[2]
except: root = expanduser("~")

@get("/")
def greet():
	html = """<title>Atmosphera v1.0</title>
		<h3>Welcome to Atmosphera!</h3>
		<a href="http://{}:8080/download/">-> Click here to download files from root.</a><br>
		<a href="http://{}:8080/upload/">-> Click here to upload files to root.</a>""".format(host, host)
	return html

@get("/download")
@get("/download/")
@get("/download/<filename:path>")
def download(filename=""):
	path = join(root, filename)
	if isdir(path):
		html = """<title>Atmosphera v1.0 - Download</title>
			<h3>Download files.</h3><h4>{}</h4>
			<a href="http://{}:8080"><- Back to Home.</a>
			<br><br>""".format(path, host)
		files, folders = [], []
		for file in listdir(path):
			if isdir(join(path, file)):
				folders += [file]
			else: files += [file]
		files.sort(), folders.sort()
		for folder in folders:
			html += '<b><a href="http://{}:8080/download/{}">{}/</a></b><br>'.format(
				host, join(filename, folder), folder)
		for file in files:
			html += '<a href="http://{}:8080/download/{}">{}</a><br>'.format(
				host, join(filename, file), file)
		return html
	else:
		return static_file(filename=filename, root=root, download=True)

@get("/upload")
@get("/upload/")
def upload_greet():
	html = """<title>Atmosphera v1.0 - Upload</title>
		<h3>Upload files.</h3>
		To upload a file:
		<ol><li>Click the "Examine..." button.</li>
		<li>Click on "Start upload." button.</li></ol>
		<form action="/upload/" method="post" enctype="multipart/form-data">
		Choose file. <input type="file" name="upload"/>
		<input type="submit" value="Start upload."/><br>
		<a href="http://{}:8080"><- Back.</a>""".format(host)
	return html
@post("/upload/")
def upload():
	upload = request.files.get("upload")
	upload.save(root, overwrite=True)
	html = """<title>Atmosphera v1.0 - Upload</title>
		<h3>File uploaded.</h3>
		Go back to upload a new file.<br>
		<a href="http://{}:8080/upload/"><- Back.</a>""".format(host)
	return html

run(host=host, port=8080)