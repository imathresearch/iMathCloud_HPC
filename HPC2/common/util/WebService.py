import pycurl
import urllib

class WebServiceClass:

	def executeWebService(self, ConcenateString):
		print "Start executeWebService"
		pyCurlClass = pycurl.Curl()
		#print "ExecuteWebService after pycurl.Curl"
		pyCurlClass.setopt(pyCurlClass.URL,str(ConcenateString))
		#print "ExecuteWebService after setopt 1"
		pyCurlClass.setopt(pycurl.USERPWD, 'WSUser:943793072')
		#pyCurlClass.setopt(pycurl.USERPWD, 'ammartinez:h1i1m1')
		#print "ExecuteWebService after setopt 2"
		pyCurlClass.perform()
		print "End executeWebService"	

	def callWebService(self,Url,Parameters,ParametersValue):
		
		CrossedParameters = 0
		ConcenateString = Url + '?';
		for Parameter in Parameters:
			ConcenateString = ConcenateString + Parameter + '=' + str(ParametersValue[CrossedParameters]) + '&'
			CrossedParameters = CrossedParameters + 1
		ConcenateString = ConcenateString[0:len(ConcenateString)-1]
		self.executeWebService(ConcenateString)

	def old_callWebServiceJSON(self,Url,JSONValue):
		
		ConcenateString = Url + urllib.quote_plus(JSONValue);
		print ConcenateString
		self.executeWebService(ConcenateString)
		
	def callWebServiceJSON(self,Url,JSONValue):
		
		print "DENTRO DE callWebServiceJSON"
		ConcenateString = Url + urllib.quote(JSONValue, safe='');
		print ConcenateString
		self.executeWebService(ConcenateString)

	def getParameterAndParametersValueList(self,Url):

		FindElement = '?'
		FoundPosition = Url.find(FindElement,0)
		if (FoundPosition>-1):
			UrlUsefull = Url[FoundPosition+1:len(Url)]
			RangeUrlUsefull = range(len(UrlUsefull))
			Element = ''
			ParametersParametersValueEachElement = []
			ParametersParametersValueAllElements = []
			Parameters = 0
			for i in RangeUrlUsefull:
				if (UrlUsefull[i]=='&'):
					ParametersParametersValueEachElement.append(Element)
					ParametersParametersValueAllElements.append(ParametersParametersValueEachElement)
					Element = ''
					ParametersParametersValueEachElement = []
					Parameters = Parameters + 1
				else:
					if (UrlUsefull[i]=='='):
						ParametersParametersValueEachElement.append(Element)
						Element = ''
					else:
						Element = Element + UrlUsefull[i]
							
			ParametersParametersValueAllElements.append(ParametersParametersValueEachElement)
			Parameters = Parameters + 1
			return ParametersParametersValueAllElements
		else:
			return 0

	def getParameterAndParametersValueDict(self,Url):

		FindElement = '?'
		FoundPosition = Url.find(FindElement,0)
		if (FoundPosition>-1):
			UrlUsefull = Url[FoundPosition+1:len(Url)]
			RangeUrlUsefull = range(len(UrlUsefull))
			Element = ''
			ParametersParametersValueAllElements = {}
			Parameters = 0
			for i in RangeUrlUsefull:
				if (UrlUsefull[i]=='&'):
					ParametersParametersValueEachElement = eval(Element)
					ParametersParametersValueAllElements.update(ParametersParametersValueEachElement)
					Element = ''
				else:
					Element = Element + UrlUsefull[i]
							
			ParametersParametersValueAllElements.update(Element)
			return ParametersParametersValueAllElements
		else:
			return 0

	def getTornadoWebServices(self,WebServicesData,positionGroup,PositionFunction,PositionTornadoFunction):

		ListWebServices = []
		for webServicesData in WebServicesData:
			PathWebService = "/" + webServicesData[positionGroup] + "/" + webServicesData[PositionFunction]
			ActualElement = (PathWebService,webServicesData[PositionTornadoFunction])
			ListWebServices.append(ActualElement)
		return ListWebServices
