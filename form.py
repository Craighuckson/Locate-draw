import sys


def get_teldig_data() -> dict:
    import uiautomation as auto
    from ahk import AHK
    from ahk.window import Window
    ahk = AHK()

    script = """
	ControlGet, number, Line,1, edit2, ahk_exe Mobile.exe
	ControlGet, street, line,1, Edit6, ahk_exe Mobile.exe
	ControlGet, intersection, line,1,edit10, ahk_exe mobile.exe
	ControlGet, intersection2, line,1,edit12, ahk_exe mobile.exe
	ControlGet, stationCode, line,1, edit9, ahk_exe mobile.exe
	ControlGetText, digInfo, edit22, ahk_exe mobile.exe
	controlget, ticketNumber, line, 1, edit1, ahk_exe mobile.exe
	controlget, town, line, 1, edit13, ahk_exe mobile.exe
	fileappend,%number%`n%street%`n%intersection%`n%intersection2%`n%stationCode%`n%digInfo%`n%ticketNumber%`n%town%,*
		"""
    try:
        m = ahk.win_get(title="TelDig")
        # m.activate()
        result = ahk.run_script(script)
        results = [x for x in result.splitlines()]
        ticket = {
            "number": results[0],
            "street": results[1],
            "intersection": results[2],
            "intersection2": results[3],
            "station_code": results[4],
            "dig_info": results[5],
            "ticket_number": results[7],
            "town": results[8],
        }
        return ticket
    except (TypeError, IndexError):
        print(
            'Could not get ticket info.'
            'Ensure that ticket is open in TelDig Mobile'
        )
        sys.exit()


def get_form(utility: str, page: str) -> str:
    try:
        if utility == 'ROGYRK01' and page == '1':
            return 'RP'
        elif utility == 'ROGYRK01':
            return 'RA'
        elif utility == 'APTUM01' and page == '1':
            return "AP"
        elif utility == 'APTUM01':
            return 'AA'
        elif utility == 'ENVIN01' and page == '1':
            return 'EP'
        elif utility == 'ENVIN01':
            return 'EA'
        else:
            print('Invalid utility')
            sys.exit(1)
    except NameError:
        print('Could not get form data')
        sys.exit()


def save_bitmap(filename: str = ''):
    import pyautogui as pg
    import uiautomation as auto
    pg.MINIMUM_SLEEP = 0.8
    from pathlib import Path
    win =  auto.WindowControl(SubName='TelDig SketchTool')
    if not win.Exists(3,1):
        auto.MessageBox('SketchTool window not open or accessible', 'Window not open')
        sys.exit()
    if filename is None or filename == '':
        filename = pg.prompt('Enter save file name', 'BMP file name')
    fp = str(Path('C:/Users/Cr/Locatedraw/Locate-draw/') / filename)
    if filename is None:
        pg.alert('Could not save file')
        return
    win.GetWindowPattern().SetWindowVisualState(1)
    win.MenuItemControl(Name='File').GetInvokePattern().Invoke()
    win.SendKeys('{Down}{Enter}')
    sa = win.WindowControl(Name='Save As')
    sa.EditControl(Name='File name:').GetValuePattern().SetValue(fp)
    sa.ComboBoxControl(Name='Save as type:').GetExpandCollapsePattern().Expand()
    sa.ListItemControl(Name='Bitmap (*.bmp)').GetSelectionItemPattern().Select()

if __name__ == '__main__':
    current_page: int = 1
    save_bitmap()
