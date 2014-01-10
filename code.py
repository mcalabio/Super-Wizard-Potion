import web
import sys
import json
import os
from binascii import a2b_base64

render = web.template.render('.')

urls = (
	'/', 'engine'
	)

class engine:
	def GET(self):
		name = 'Brendon'
		return render.engine(name)

	def POST(self):

		json_data = web.data()

		data = json.loads(json_data)

		# saveRecord()
		if (data["type"] == "saveRecord"):
			record = data["data"]
			f = open('records/records','a')
			f.write(record)
			f.close()

			return record

		# findEditLevels()
		elif (data["type"] == "findEditLevels"):

			stage = 1

			while (stage < 100):

				try: 
					f = open('levels/0-' + str(stage))
					f.close()
					stage += 1

				except: break

			web.debug("last level found = 0-" + str(stage-1))
			return stage


		elif (data["type"] == "deleteLevel"):

			if (data["level"][0] == 0):
				level = str(data["level"][0]) + "-" + str(data["level"][1])
			else:
				level = str(data["level"][1])
			os.remove('levels/' + level)

			latest = int(data["level"][2]) - 1

			return 0

		# loadLevel()
		elif (data["type"] == "loadLevel"):
			level = str(data["level"][0]) + "-" + str(data["level"][1])

			try:
				f = open('levels/' + level,'r')
				level_string = f.read()
				f.close()

			except:
				level_string = "\n\n\n\n\n\n"

			web.debug("returning level_string = " + level_string)
			return level_string

		# loadLevels()
		elif (data["type"] == "loadLevels"):

			levels_data = {"levels": [[]]}

			home_path = os.getcwd()

			os.chdir("levels/")
			web.debug(os.getcwd())

			all_levels = os.listdir(".")

			stage = 0
			for files in all_levels:
				if files.startswith("0-"):
					f = open(files)
					levels_data["levels"][0].append(f.read())
					f.close()
					stage += 1

			os.chdir(home_path)

			level = 1

			while (level < 100):

				try:

					f = open('levels/' + str(level) + '-1')
					f.close()

					levels_data["levels"].append([])

					stage = 1
					while (stage < 100):

						try:

							f = open('levels/' + str(level) + '-' + str(stage))
							levels_data["levels"][level].append(f.read())
							f.close()

							stage += 1

						except:

							break

					level += 1

				except:

					break

			return json.JSONEncoder().encode(levels_data)

		# saveLevel()
		elif (data["type"] == "saveLevel"):
			level = str(data["level"][0]) + "-" + str(data["level"][1])
			level_string = data["data"]
			web.debug("level = " + level)
			web.debug("level_string = " + level_string)
			if (data["level"][0]==0):
				f = open('levels/0-' + data["name"],'w')
			else:
				f = open('levels/' + str(level),'w')
			f.write(level_string)
			f.close()

			web.debug("saved level " + str(level))
			return str(level)

		# saveImage()
		elif (data["type"] == "saveImage"):

			encoded_data = data["data"]
			level = str(data["level"][0]) + "-" + str(data["level"][1])

			binary_data = a2b_base64(encoded_data)

			fd = open('levels/screens/' + level + '.png', 'wb')
			fd.write(binary_data)
			fd.close()

			web.debug("encoded data = " + encoded_data)
			return 0

		return


if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()

