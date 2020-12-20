@if (@a==@a) @end /*
        cscript //E:JScript //nologo "%~f0" %*

    REM --- Insert other batch codes here ---

        exit /b 
*/



var WshShell = WScript.CreateObject("WScript.Shell");
var ARGS = WScript.Arguments;

WshShell.AppActivate(ARGS.Item(0));
WshShell.SendKeys("~");
WScript.Echo(ARGS.Item(0) + " activated");
WScript.Quit(0);