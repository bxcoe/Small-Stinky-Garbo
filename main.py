#This will be the main program
#This program will allow a user to select an input file, and perform various plotting techniques to visualize data
#Examples include generating scatterplots, histograms, and animated GIFs
#These will then be output into the output file by default, or the user can choose where to save


#Random links:
#https://docs.python.org/3/tutorial/classes.html
#https://wxpython.org/Phoenix/docs/html/Overviews.html
#https://wxpython.org/Phoenix/docs/html/sizers_overview.html
#https://wiki.wxpython.org/FrontPage
#https://www.blog.pythonlibrary.org/2018/10/19/wxpython-how-to-open-a-second-window-frame/
#http://zetcode.com/wxpython/dialogs/
#https://stackoverflow.com/questions/10833163/how-to-kill-a-wxpython-application-when-user-clicks-a-frames-close

#====================== Pseudo code =======================
#Run DataHandler, get the large data arrays
#Run Plotter, get how the large data arrays are organized
#Assign large data arrays to smaller arrays in main
#

import DataHandler as dh
import animator as anim
import plotter as plotter

def main():
    #app = dh.wx.App()
    dh.main()
    plotter.main()
    #To access the data from DataHandler use this:
    #dh.DataHandler.dataArray[0]

if __name__ == '__main__':
    main()
