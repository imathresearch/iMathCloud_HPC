import numpy as np
import pylab as P
import matplotlib.gridspec as gridspec
import matplotlib.mlab as mlab

from urlparse import urlparse


class Plots:
	def UnivarDescStat(self,Data,FileOutPath):
		# Analitic Descriptives text
		N = len(Data)
		Mean = np.mean(Data)
		Minimum = np.min(Data)
		Maximum = np.max(Data)
		Variance = np.var(Data)
		Std = np.std(Data)
		
		MinimumQ = np.percentile(Data,0)
		Q1 = np.percentile(Data,25)
		Median = np.percentile(Data,50)
		Q3 = np.percentile(Data,75)
		MaximumQ = np.percentile(Data,100)
		
		
		txt = ("\nN : {0:8d}".format(N))
		txt = txt + ("\nMean : {0:8.6f}".format(Mean))
		txt = txt + ("\nMinimum : {0:8.6f}".format(Minimum))
		txt = txt + ("\nMaximum : {0:8.6f}".format(Maximum))
		txt = txt + ("\nVariance : {0:8.6f}".format(Variance))
		txt = txt + ("\nStd. deviation : {0:8.6f}".format(Std))
		txt = txt + ("\n\n\n")
		txt = txt + ("\nMinimum : {0:8.6f}".format(MinimumQ))
		txt = txt + ("\n1st Quartile : {0:8.6f}".format(Q1))
		txt = txt + ("\nMedian : {0:8.6f}".format(Median))
		txt = txt + ("\n3rd Quartile : {0:8.6f}".format(Q3))
		txt = txt + ("\nMaximum : {0:8.6f}".format(MaximumQ))
		

		# Grid to plot into.
		G = gridspec.GridSpec(2, 2, width_ratios=[2, 1])
		
		# Plot Analitics
		axes_1 = P.subplot(G[:,1])
		axes_1.set_title("Analitics")
		axes_1.axis('off')
		P.text(0.15, 0.25, txt, size=12)
		
		# Histogram and...
		axes_2 = P.subplot(G[0,0])	
		axes_2.set_title("Histogram")
		n, bins, patches = P.hist(Data, 15, normed=1)
		# ... PDF Plots (Probability Distribution Function)
		y = mlab.normpdf( bins, Mean, Std)
		P.plot(bins, y, 'r--', linewidth=1)
		P.ylabel('Probability')
			
		# Plot boxplot
		axes_3 = P.subplot(G[1,0])
		axes_3.set_title("Boxplot")
		P.boxplot(Data,0,'rs',0);
		
		# Store as SVG
		P.savefig(FileOutPath)

		
	def MultivarDescStat(self,Data,FileOutPath):
		NVars = len(Data[0])
		
		# Plot histograms if both are the same variables (diagonal).
		# For different variables, a scatter plot with both variables against each other.
		loc = 1
		for i in range(NVars):
			for j in range(NVars):
				P.subplot(NVars, NVars, loc)
				if (i==j):
					P.hist(Data[:,i], 15, normed=1)
				else:
					P.scatter(Data[:,i],Data[:,j])
					
				loc = loc + 1
				
		# Store as SVG
		P.savefig(FileOutPath)


	def PolinomialRegression(self,Data,FileOutPath,hasHeader,polinoimalDegree):
		NVars = len(Data[0])
		# Plot column name if both are the same variables (diagonal).
		# For different variables, a scatter plot with both variables and their regression.
		Header = []
		if (hasHeader):
			Header = Data[0]
			Data = Data[1:]
		else:
			for i in range(NVars):
				Header.append("column "+str(i+1))
				Data = Data

		loc = 1
		for i in range(NVars):
			for j in range(NVars):
				P.subplot(NVars, NVars, loc)
				if (i==j):
					P.text(0.2, 0.5, Header[i], size=12)
				else:
					fit = P.polyfit(Data[:,i],Data[:,j],polinoimalDegree)
					yp = P.polyval(fit,np.sort(Data[:,i]))
	
					P.plot(np.sort(Data[:,i]),yp,'g-',Data[:,i],Data[:,j],'b.')
					P.grid(True)
					
				loc = loc + 1
		
		# Store as SVG
		P.savefig(FileOutPath)
