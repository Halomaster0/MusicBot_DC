Set shell = CreateObject("WScript.Shell")
' Use the virtual environment's pythonw.exe if it exists, otherwise fall back to system pythonw
vVenvPath = shell.CurrentDirectory & "\.venv\Scripts\pythonw.exe"
vScriptPath = shell.CurrentDirectory & "\src\main.py"

If CreateObject("Scripting.FileSystemObject").FileExists(vVenvPath) Then
    shell.Run Chr(34) & vVenvPath & Chr(34) & " " & Chr(34) & vScriptPath & Chr(34), 0
Else
    shell.Run "pythonw.exe " & Chr(34) & vScriptPath & Chr(34), 0
End If
