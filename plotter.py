#This will be the plotter program
#This program will allow a user to specify what style of plot they would like created via a wx GUI
#The plots should be easily configurable via a GUI that will allow a user to choose things such as:
    #color of axes, background, gridlines,
    #plot title, axes labels, tick specifications
    #legends, various text boxes,
#A preview of the plot should appear each time a change is pushed by the user (i.e, an apply changes button)
#The plot should only be saved when the user is satisfied with the outcome of the plot.
# https://wiki.wxpython.org/Change%20wxGrid%20CheckBox%20with%20one%20click
#====================== Pseudo code =======================
#read in data from main (types of plots, data file info, fileCount)
#FOR i -> fileCount
    #read in what type of plot is being generated, set as label for window
    #ask user how the columns for the data are organized
    #organize data into appropriate arrays based on user response
        #->user response dictates xpos, ypos, zpos, etc
        #GUI should be a matrix style w/ radio buttons to allow selection
    #display available settings the user can modify for that style of plot
    #have an apply button that will generate a preview of what the updated plot looks like
        #->possible special case scenario for animated scatterplots
    #have a save button that will perform the appropriate task

#====================== Imports =========================
#Plotting
import matplotlib.pyplot as plt
from matplotlib import colors
from mpl_toolkits.mplot3d import Axes3D #used for plotting in 3d
import numpy as np
#GUI
import wx, wx.grid as grd
#====================== Functions =====================

#====================== Classes =======================
class MyGrid(grd.Grid):
    # Set the dimensions of the grid
    rows = 8
    cols = 8
    colRowBool = np.full(shape=(rows,cols),fill_value=0,dtype=int)

    def __init__(self, parent):
        grd.Grid.__init__(self, parent, -1,size=(400,525))

        # Create a grid
        self.CreateGrid(MyGrid.rows,MyGrid.cols)
        self.RowLabelSize = 55
        self.ColLabelSize = 15

        # Make the grid have editable checkboxes
        grd.Grid.SetDefaultRenderer(self,grd.GridCellBoolRenderer())
        grd.Grid.SetDefaultEditor(self,grd.GridCellBoolEditor())

        # Give these columns custom headers
        customRowLabels = ["x-pos","y-pos","z-pos","vx-pos","vy-pos","vz-pos","color-pos","time-pos"]
        customColLabels = ["col 1","col 2","col 3","col 4","col 5","col 6","col 7","col 8"]

        # Apply the custom headers
        for x in range(len(customRowLabels)):
            self.SetColSize(x,40)
            self.SetRowSize(x,55)
            self.SetRowLabelValue(x,customRowLabels[x])
            self.SetColLabelValue(x,customColLabels[x])

            # Set the default data organization style
            self.SetCellValue(x,x,"1")
            MyGrid.colRowBool[x,x] = 1

        self.Bind(grd.EVT_GRID_CELL_LEFT_CLICK,self.on_mouse)
        self.Bind(grd.EVT_GRID_SELECT_CELL,self.on_cell_selected)
        self.Bind(grd.EVT_GRID_EDITOR_CREATED,self.on_editor_created)

    def on_mouse(self,evt):
        wx.CallLater(10,self.toggle_check_box)
        evt.Skip()

    def on_frame_closed(self):
        print("User closed program")
        self.Destroy()

    def toggle_check_box(self):
        self.cb.Value = not self.cb.Value
        self.after_check_box(self.cb.Value)

    def on_cell_selected(self,evt):
        wx.CallAfter(self.EnableCellEditControl)
        evt.Skip()

    def on_editor_created(self,evt):
        self.cb = evt.Control
        self.cb.WindowStyle |= wx.WANTS_CHARS
        self.cb.Bind(wx.EVT_KEY_DOWN,self.on_key_down)
        self.cb.Bind(wx.EVT_CHECKBOX,self.on_check_box)
        evt.Skip()

    def on_key_down(self,evt):
        if evt.KeyCode == wx.WXK_UP:
            if self.GridCursorRow > 0:
                self.DisableCellEditControl()
                self.MoveCursorUp(False)
        elif evt.KeyCode == wx.WXK_DOWN:
            if self.GridCursorRow < (self.NumberRows-1):
                self.DisableCellEditControl()
                self.MoveCursorDown(False)
        elif evt.KeyCode == wx.WXK_LEFT:
            if self.GridCursorCol > 0:
                self.DisableCellEditControl()
                self.MoveCursorLeft(False)
        elif evt.KeyCode == wx.WXK_RIGHT:
            if self.GridCursorCol < (self.NumberCols-1):
                self.DisableCellEditControl()
                self.MoveCursorRight(False)
        else:
            evt.Skip()

    def on_check_box(self,evt):
        self.after_check_box(evt.IsChecked())

    def after_check_box(self,isChecked):
        MyGrid.colRowBool[self.GridCursorRow,self.GridCursorCol] = isChecked

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,title='Select Data Organization Style',size=(395,600))
        panel = MyPanel(self)
        self.Show()

class MyPanel(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent)

        grid = MyGrid(self)
        btnOK = wx.Button(self,label='OK')
        btnOK.Bind(wx.EVT_BUTTON,self.on_ok_button)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(grid,wx.ALIGN_CENTER,wx.ALIGN_CENTER,wx.ALIGN_CENTER)
        sizer.Add(btnOK,wx.EXPAND,wx.EXPAND,1)
        sizer.SetSizeHints(self)
        self.SetSizer(sizer)

    def on_ok_button(self,event):
        if(self.verify_check_box()):
            wx.MessageDialog(None,'Check rows for valid input','Info',wx.OK).ShowModal()
        else:
            self.Close()
            wx.GetTopLevelParent(self).Destroy()

    def verify_check_box(self):
        #This will verify that the users input is valid and only one item is selected properly per
        #row.
        return False

def main():
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()

if __name__ == '__main__':
    main()
