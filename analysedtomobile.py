import uiautomation as auto

win = auto.WindowControl(SubName='LocateAccess')
win.GetWindowPattern().SetWindowVisualState(1)

# activate the grid control
win.Click(1330,100)
win.ListItemControl(Name="Grid").GetInvokePattern().Invoke()

#filter for mobile
win.EditControl(Name='Request status').SetFocus()
#win.SendKeys('MOBILE')

print(win.CustomControl().get
