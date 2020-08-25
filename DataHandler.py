#This will be the file getter program (Or should it be called data collecter?)
#This program will allow a user to choose the file they would like to import and then
#describe how the file is organized. That description will then change how the file is read such as:
    #Is it a histogram?
        #How is the data organized?
        #Ask this in the plotter program instead ->#Is it an animated scatterplot?
                                                    #Does it include nbodies present?
                                                    #Does it include timesteps to animate?
#This program will also read in the data and handle array assigning
#Finally, this program will handle choosing where to save the final results, and how they should be named

#====================== Pseudo code =======================
#data to read in:
    #How many data fileLocation? -> file_detail_ui
    #DO from 0 -> #of data fileLocation:
        #How is this data file organized? -> get_data_organized_style, then save to data_organized_style array
        #What would you like done with this data file? -> save to data_plot_style array
            #histogram,heatmap,scatterplot,animated scatterplot, etc
        #Where should this be saved, and what would you like it to be named? -> save to completed_plot_title array
#====================== Imports =========================
import wx
#====================== Functions =====================
def hasNumbers(inputString):
    """Checks if a string has a number inside of it"""
    for char in inputString:
        if(char == '-'):
            return True
        try:
            float(char)
            return True
        except:
            return False

def read_data(filePath):
    """Read in the input file given by filePath"""
    data = []
    newdata = []
    inputfile = open(filePath,"r")
    #Reads in the data
    while True:
        line = inputfile.readline()
        #if the end of the file is reached
        if not line:
            break;
        rawdata = line.split(" ")
        for i in rawdata:
            if hasNumbers(i) == True:
                i = i.rstrip()
                newdata.append(i)
        data.append(newdata)
        newdata = []
    inputfile.close()
    return data
#====================== Classes =======================

class MyDataHandler(wx.Frame):
    fileCount = 0
    fileLocation = []
    filePlotStyle = []
    dataArray = [] #an array of arrays. Is having an array this large bad? Probably. Do I care? No.

    def __init__(self,parent):
        super().__init__()

        #Collect information from the user about what files we're working with
        MyDataHandler.fileCount = int(self.file_detail_ui())
        for i in range(MyDataHandler.fileCount):
            MyDataHandler.fileLocation.append(self.file_location_ui())
            MyDataHandler.filePlotStyle.append(self.plot_style_ui())

        #Now that the user is done clicking 50 dialog boxes because I have no prior GUI experience, read the data files in
        for i in range(MyDataHandler.fileCount):
            MyDataHandler.dataArray.append(read_data(filePath=MyDataHandler.fileLocation[i]))

    def file_detail_ui(self):
        """Find how many data fileLocation the user plans to import"""
        message = "How many data files?"
        title = "File Details"
        dialog = wx.TextEntryDialog(self,message,title)
        if(dialog.ShowModal() == wx.ID_OK):
            return dialog.GetValue()
        dialog.Destroy()

    def plot_style_ui(self):
        """Find out what types of plots the user plans to create"""
        choices = ["Scatterplot","Heatmap","Histogram","Animated Scatterplot"]
        message = "Choose the type of plot you'd like created for file"
        title = "Data Plot Style Selector"
        dialog = wx.SingleChoiceDialog(None,message,title,choices,style=wx.CHOICEDLG_STYLE)
        if(dialog.ShowModal() == wx.ID_OK):
            return dialog.GetStringSelection()
        dialog.Destroy()

    def file_location_ui(self):
        """Lets the user select fileLocation to open"""
        dialog = wx.FileDialog(self,"Open File",style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if dialog.ShowModal() == wx.ID_OK:
            return dialog.GetPath()
        else:
            return None
        dialog.Destroy()

def main():
    app = wx.App()
    frame = MyDataHandler(None)
    frame.Show()

if __name__ == '__main__':
    main()
