#for isig in Isigma:#dfIS = {'I_Sigma':isig}
#dframeIS = robjects.DataFrame(dfIS)
#dtfIS = robjects.r.melt(dframeIS,measure_var=['I_Sigma'])
#new_dtfIS=dtfIS.rx(2)
#new_dtfIS.names[tuple(new_dtfIS.colnames).index('value')]='I_Sigma'


for int in I:
    #for sig in sigma:
        for cv in CVI:
            dfI = {'Intesity': int}
            dfcv = {'cv':CVI}
            dframeI = robjects.DataFrame(dfI)
            dtfI = robjects.r.melt(dframeI,measure_var=['Intensity'])
            new_dtfI=dtfI.rx(2)
            dfS = {'Sigma':sig}
            dframeS = robjects.DataFrame(dfS)
            dtfS = robjects.r.melt(dframeS,measure_var=['Sigma'])
            new_dtfS=dtfS.rx(2)
            new_dtfS.names[tuple(new_dtfS.colnames).index('value')]='Sigma'
            dfcv = {'cv':CVI}
            dframecv = robjects.DataFrame(dfcv)
            dtfcv = robjects.r.melt(dframecv,measure_var=['cv'])
            new_dtfcv=dtfcv.rx(2)
            new_dtfcv.names[tuple(new_dtfcv.colnames).index('value')]='cv'
            db=new_dtfI.cbind( Sigma=new_dtfS,Yp=Yp, Xp=Xp,cv = new_dtfcv)
            db.names[tuple(db.colnames).index('value')]='Intensity'
            #print dtf.names
            csvname = csvpath.replace('?','%03d' %i)
            utilis.write_csv(db, csvname)




#print (len(I))
t1=time.time()
csvpath = '/Users/giordano_r/Desktop/PythonCode/In_test_insu_1s?.csv'
for i in range(1,3):
    for int in enumerate(I[0]):
        for cv in enumerate(CVI[0]):
            df = {'Intesity': I}
            dframe = robjects.DataFrame(df)
            dtf = robjects.r.melt(dframe).rx(2)
            dtf.names[tuple(dtf.colnames).index('value')]='Intensity'
            dfcv = {'cv':CVI}
            dframecv = robjects.DataFrame(dfcv)
            dtfcv = robjects.r.melt(dframecv,measure_var=['cv']).rx(2)
            dtfcv.names[tuple(dtfcv.colnames).index('value')]='cv'
            db=dtf.cbind(Yp=Yp, Xp=Xp, cv = dtfcv)
            csvname = csvpath.replace('?','%03d' %i)
            utilis.write_csv(db, csvname)
print "%.3f" % (time.time()-t1)

for i in range(1,3):
    for idx,j in enumerate(Iarray[0]):
        csvf = csvpath.replace('?', '%03d' %i)
        infile = open(csvf,'wb')
        writer = csv.writer(infile, delimiter='\t', quotechar='"',quoting=csv.QUOTE_ALL)
        #header = ['XP', 'YP']
        #writer.writerow(header)
        #for idx,j in enumerate(Iarray[0]):
        row = []
        #row.append(Xp[idx])
        #row.append(Yp[idx])
        row.append(Iarray[:,idx])
        #row.extend(CVIarray[:,idx])
        writer.writerow(row)
        infile.close()


#Peak = []
#for i in range(0,70):
#P = robjects.conversion.py2ri(newRow[i])
#PV = robjects.IntVector(P)
#Peak.append(PV)
#df = {'Peak':Peak,'x':x}
#datPeak=robjects.DataFrame(df)



#for i in range(1,71):
#dtfP = robjects.r.melt(dataf, measure_var=['P_i'], variable_name='PeakType')

#P_R.replace('?', %i)
#row1V=robjects.IntVector(Rnewrow1)



#for i in range(1,8):
#csvname = csvpath.replace('?','%03d' %i)
#    print csvname
#csv_data=utilis.read_csv(csvname)
#x=csv_data.rx(1)
#db=robjects.DataFrame(csv_data)
#dtf=db.cbind(Nspot=x)
#limits = ggplot2.aes_string(ymax= 'Intensity + cv', ymin= 'Intensity - cv')
#gp = ggplot2.ggplot(dtf)
#pp=gp+ggplot2.aes_string(x='X',y='Intensity')+ ggplot2.geom_point()+ggplot2.theme_bw()+ ggplot2.geom_errorbar(limits) + ggplot2.ylim(2500,50000)
#grdevices.pdf(path)
#grdevices.X11()
#pp.plot()
# mean value of intensity for each frame
#Im = csv_data.rx(2)

#grdevices.dev_off()
#for i in range(1,3):
#csvname = csvpath.replace('?','%01d' %i)
#print csvname
#csv_data=utilis.read_csv(csvname)
#I = x=csv_data.rx(2)
#cvI = cv(I)
##cvINT.append()
#utilis.write_csv(cv, '/Users/giordano_r/Desktop/PythonCode/cv.csv')






robjects.globalenv["I1_r"] = I1_r
robjects.globalenv["N"] = N

fmla1_pl3 = Formula('I1_r ~ poly(N, 3)')
fit1_pl3 = robjects.r('lm(%s)' %fmla1_pl3.r_repr())
print(base.summary(fit1_pl3))
fit1Values3 = fit1_pl3.rx('fitted.values')
fit1Array = np.array(fit1Values3)


## Calculate the difference between the data and the fitted values.
#dtrend1 = int1List - fit1Array

# Calculate the rmsd of the data point from the polynomial regression.
#rmsd1 = []
#for i in dtrend1:
#   rmsd1 = rmsd(i)

# Calculate the rmsd relatice:
#rmsd1_r = []
#for i in dtrend1:
#rmsd1_r = rmsd_r(i,int1List)


# Coefficient of variation of the Intensity
#f = open('/Users/giordano_r/Desktop/e10019/20121015/lyso1/still2/cv_lyso.dat', 'a+')
#cv1 = cv(In1)



#d = {'N' : N, 'R1' : I1_r}
#dataf = robjects.DataFrame(d)

#gp = ggplot2.ggplot(dataf)

#pp = gp + ggplot2.aes_string(x='N', y= 'I1_r')

#print 'CV', sys.argv[1], 'I1 is:', cv1

#f.write(cvI1, cvI2, cvI3)


## Create a dataframe containing all reflection and the number of images.
#d = {'R1' : I1_r, 'R2' : I2_r, 'R3' : I3_r,}
#dataf = robjects.DataFrame(d)

# melt from horizontal into vertical format
#dtf = robjects.r.melt(dataf, measure_var=['R1','R2','R3'], variable_name='RType')

# add a column with the number of images
#db=dtf.cbind(dtf, images = robjects.IntVector(range(1,501)))
#db.names[tuple(db.colnames).index('variable')] = 'Reflections'



#title = 'Vertical position 0'
#title1=title.replace('0',sys.argv[2])
#Plot the data using ggplot2
#gp = ggplot2.ggplot(db)
#pp=gp+ggplot2.aes_string(x='images',y='value', color='Reflections', shape='Reflections') + ggplot2.geom_point()+ggplot2.theme_bw()+ ggplot2.ggtitle(title1)+ \
ggplot2.scale_x_continuous("N images")+ ggplot2.scale_y_continuous("Intensity")

#r.X11()
#pp.plot()

#path2 = '/Users/giordano_r/Desktop/e10019/20121015/lyso1/still2/Ipos0.pdf'
#path3 = path2.replace('pos0',sys.argv[3])

#print path3

#grdevices.pdf(path3)
#pp.plot()
#grdevices.dev_off()


def gaus_fit_x(x,m):
    proj=m.mean(0)
    y = robjects.conversion.py2ri(proj)
    mu = base.mean(y)
    sigma = stats.sd(y)
    robjects.globalenv['x'] = x
    robjects.globalenv['y'] = y
    formula = robjects.Formula('y~(1/(sigma*sqrt(2*pi))*exp(-(x-mu)**2/(2.*sigma**2)))')
    fit = robjects.r('nls(%s, start=list(sigma=1, mu=1),alg="plinear")' %formula.r_repr())
    coeff=stats.coef(stats.summary_nls(fit))
    summary = stats.summary_nls(fit)
    fitvalue = stats.predict_nls(fit)
    return coeff, fitvalue, proj, mu,sigma


#def gaus_fit_y(x,m):
#proj=m.mean(1)
#y = robjects.conversion.py2ri(proj)
#mu = base.mean(y)
#sigma = stats.sd(y)
#robjects.globalenv['x'] = x
#robjects.globalenv['y'] = y
#formula = robjects.Formula('y~(1/(sigma*sqrt(2*pi))*exp(-(x-mu)**2/(2.*sigma**2)))')
#fit = robjects.r('nls(%s, start=list(sigma=1, mu=1),alg="plinear")' %formula.r_repr())
#coeff=stats.coef(stats.summary_nls(fit))
#summary = stats.summary_nls(fit)
#fitvalue = stats.predict_nls(fit)
#return coeff, fitvalue, proj, mu,sigma, summary


dimBox = 15
X0i=0
X0f=dimBox
Y0i=0
Y0f=dimBox

for i in xrange(0,x-dimBox):
    print i
    for j in xrange(0,y-dimBox):
        print j
        m=a[Y0i+j:Y0f+j,X0i+i:X0f+i]
        print m
        stat = matCal(m)
        print stat

for i in xrange(0,x-dimBox):
    for j in xrange(0,y-dimBox):
        m=a[Y0i+j:Y0f+j,X0i+i:X0f+i]     # measurement box
        stat = matCal(m)
        #s = m.sum()
        #sup = m.max()
        Yc=((Y0i+j)+(Y0f+j))/2           # peak coordinates
        Xc=((X0i+i)+(X0f+i))/2
        Y=[Y0i+j,Y0f+j]                  # measurement box coordinates
        X=[X0i+i,X0f+i]
        if (stat[0]>500 and stat[1]> 500 and
            m.argmax()== centerPosition):
            append(m)
            append1((Xc,Yc))
            coorappend((Y,X))
            del m

