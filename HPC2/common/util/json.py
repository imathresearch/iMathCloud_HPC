import simplejson as json

class JSON:

	def ArrayToJsonString(self,user,session,operation,data):
		jSonVariable = '{"user" : ' + user + ',"session" : ' + session + '"operation" : ' + str(operation) + ', "resultado" : ['
		for ActualData in data:
			jSonVariable = jSonVariable + str(ActualData) + ','
		jSonVariable = jSonVariable[0:len(jSonVariable)-1]
		jSonVariable = jSonVariable + ']}'
		return jSonVariable

	def ArrayToJsonStringLists(self,Parameters,ParameterValues):
		jSonVariable = '{'
		CrossedPosition = 0
		for Parameter in Parameters:
			jSonVariable = jSonVariable + Parameter + ':' + str(ParameterValues[CrossedPosition]) + ','
			CrossedPosition = CrossedPosition + 1
		jSonVariable = jSonVariable[0:len(jSonVariable)-1]
		jSonVariable = jSonVariable + '}'
		return jSonVariable

	def ArrayToJsonStringCompleteListParameterValues(self,ListParameterValues):
		jSonVariable = '{'
		for ParameterValue in ListParameterValues:
			jSonVariable = jSonVariable + str(ParameterValue) + ','
		jSonVariable = jSonVariable[0:len(jSonVariable)-1]
		jSonVariable = jSonVariable + '}'
		return jSonVariable

	def ArrayToJsonFileNames(self,ListFileNames):
		jSonVariable = '{'
		for ListFileName in ListFileNames:
			jSonVariable = jSonVariable + str(ListFileName) +  ','
		jSonVariable = jSonVariable[0:len(jSonVariable)-1]
		jSonVariable = jSonVariable + '}'
		return jSonVariable
	
	'''
		We create a json dictionary that contains the list of files and directories as job output
		The / of the paths are eliminated because of an interference with JBOSS
	'''
	def FilesDirsPlusPathtoJSonString(self, ListFileNames, ListDirs):
		my_list_files = []
		for l in ListFileNames:
			my_list_files.append(l.split('/'))
		
		my_list_dirs = []
		for l in ListDirs:
			my_list_dirs.append(l.split('/'))
		
		my_dic = {};
		my_dic['files'] = my_list_files
		my_dic['dirs'] = my_list_dirs
		
		print my_dic
		
		return my_dic
		
	def JSonStringToJsonEncoder(self,JsonString):
		return json.loads(JsonString)
		
	def JSonStringToJsonDecoder(self,JSonData):
		return json.dumps(JSonData)
