class Utils:

	@staticmethod
	def getColumnPosition(self,ColumnNameToFound,ColumnNames):

		crossedPosition = 0
		found = False
		for columnName in ColumnNames:
			if (ColumnNameToFound==columnName):
				found = True
				break
			crossedPosition = crossedPosition + 1;
		if (found == True):
			return crossedPosition
		else:
			return -1
