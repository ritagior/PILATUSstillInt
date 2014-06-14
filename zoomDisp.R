#####################################################
# zoom function for diffraction images using DISP   #
#####################################################

# Define a function to display the cbf images and the spot. This function takes as arguments the imageMatrix and the coordinates of the centre of the measurement box.
dispPlot<-function(imageMatrix,xPx,yPx){
	disp(flipVertical(imageMatrix), origin=c(0,0))
	points(xPx,yPx, col='blue', cex=0.8)
}


zoom <- function (imageMatrix,x, y, xlim, ylim, xd, yd) 
{
  # Define the measurement box of abot 15 x 15 pixels
  Nxi <- (x-7)
  Nxf <- (x+7)
  Nyi <- (y-7)
  Nyf <- (y+7)
  par(mfrow=c(2,2))
  dispPlot(imageMatrix,xd,yd)
  #points(xd,yd, col='blue', cex=0.4)
  m=imageMatrix[Nxi:Nxf,Nyi:Nyf]
  mcol=colMeans(m)
  mrow=rowMeans(m)
  xm=seq(Nxi,Nxf, by=1)
  ym=seq(Nyi,Nyf, by=1)
  Is=sum(m)/sd(as.numeric(m))
  #par(mfrow=c(2,3))
  #layout(matrix(c(2,0,1,3),2,2,byrow=TRUE), c(3,1), c(1,3), TRUE)
  #layout(matrix(c(0,1,3,2,0,4),2,3), c(2,1), c(2,3))
  #par(mfrow=c(2,2))
  disp(flipVertical(imageMatrix[Nxi:Nxf,Nyi:Nyf]), origin=c(Nxi,Nyi))
  plot(xm,mrow, type='l',xlab="X Pixels", ylab="X Projection", sub=paste("I:",sum(m)))
  plot(ym,mcol, type='l', xlab="Y Pixels", ylab="Y Projection", sub=paste("x,y=", x ,",",y))
  
  #plot(mcol,ym, type='l',ylim=rev(range(y)),las=1, ylab="", xlab="Y Projection")
  #X11()
  par(mfg = c(1, 1))
  dispPlot(imageMatrix,xd,yd)
  #dev.off()
  #points(xd,yd, col='blue',cex=0.3)
}
print("Zoom in: Click on the spot", quote=FALSE)
print("Stop zoom:    Right click", quote=FALSE)
print("Close image:  Return", quote=FALSE)


ident <- function(imageMatrix,x, y, ...)
{
	
  ans <- identify(x, y, n = 1, plot = FALSE, ...)
  if(length(ans)) {
    zoom(imageMatrix,x[ans], y[ans], range(x), range(y), x, y)
    points(x[ans], y[ans], pch = 21)
    ident(imageMatrix,x, y)
  }
}

