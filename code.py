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
			level = str(data["level"][0]) + "-" + str(data["level"][1])
			os.remove('levels/' + level)

			latest = int(data["level"][2]) - 1

			web.debug("latest = " + str(latest))
			web.debug("stage = " + str(data["level"][1]))

			if (latest == int(data["level"][1])):
				web.debug("deleting latest level")
				return latest

			stage = int(data["level"][1]) + 1
			next_level = str(data["level"][0]) + "-" + str(stage)

			while (stage < 100):
				try:
					os.rename('levels/' + next_level,'levels/' + level)
					level = next_level
					stage += 1
					next_level = str(data["level"][0]) + "-" + str(stage)

				except:
					break

			return stage - 1

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

			levels_data = {"levels": []}

			level = 0

			while (level < 4):

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


			return json.JSONEncoder().encode(levels_data)

		# saveLevel()
		elif (data["type"] == "saveLevel"):
			level = str(data["level"][0]) + "-" + str(data["level"][1])
			level_string = data["data"]
			web.debug("level = " + level)
			web.debug("level_string = " + level_string)
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

