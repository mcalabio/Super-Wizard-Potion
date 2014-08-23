import web
import sys
import json
import os
from binascii import a2b_base64
from git import *

repo = Repo(".")
assert repo.bare == False
git = repo.git

render = web.template.render('.')

urls = (
	'/', 'engine'
	)

paths_players = [ ["0501zonk1","0501zonk2","0501zonk3","cassidy","mikey","mika"],["0502zonk1","0502zonk2","0502zonk3"],["0503zonk1","0503zonk2","0503zonk3"],["0504zonk1","0504zonk2","0504zonk3"] ]

class engine:
	def GET(self):
		name = 'Brendon'
		return render.engine(name)

	def POST(self):

		json_data = web.data()

		data = json.loads(json_data)

		web.debug("running function = " + data["type"])

		# saveRecord()
		if (data["type"] == "saveRecord"):
			record = data["data"]
			f = open('records/records.json','r+')
			f.seek(-1,2)
			f.write(record)
			f.close()
			web.debug("git commiting")
			git.commit(a=True, m="'new record added'")

			return record

		# getRecords()
		elif (data["type"] == "getRecords"):
			try:
				f = open('records/records.json','r')
				records_data = f.read()
				f.close()
				web.debug("records_data = " + records_data)
				return records_data
			except:
				web.debug("error opening json file")
				return ""

		# playerPath()
		elif (data["type"] == "playerPath"):
			name = data["data"]

			for i in xrange(0,len(paths_players)):
				for j in paths_players[i]:
					web.debug("checking if " + j + " equals " + name)
					if (j == name):
						web.debug("player \""+ name + "\" is designated path = " + str(i))
						return i

			web.debug("player \"" + name + "\" does not have a designated path = -1")
			return -1

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
			all_levels.sort()

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

			try:
				f = open('levels/sprints.json','r')
				levels_data["sprints"] = f.read()
				f.close()

			except:
				web.debug("failed to open sprints.json file")

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

			if (data["level"][0]==0):
				level = "0-" + str(data["level"][2])

			else:
				level = str(data["level"][0]) + "-" + str(data["level"][1])

			web.debug("level_name = " + level)

			binary_data = a2b_base64(encoded_data)

			fd = open('levels/screens/' + level + '.png', 'wb')
			fd.write(binary_data)
			fd.close()

			return 0

		return


if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()
