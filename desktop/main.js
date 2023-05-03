const { app, BrowserWindow, screen } = require('electron');

function createWindow()
{
    const { width, height } = screen.getPrimaryDisplay().workAreaSize;

    const win = new BrowserWindow(
    {
        show: false,
        width: width,
        height: height,
        icon: 'assets/icon.ico',
        webPreferences:
        {
            nodeIntegration: false,
            contextIsolation: true,
        },
    });

    win.setMenuBarVisibility(false);
    win.loadURL('https://proj-aums.hu/');

    win.once('ready-to-show', () =>
    { win.show(); });
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () =>
{ if (process.platform !== 'darwin') app.quit(); });

app.on('activate', () =>
{ if (BrowserWindow.getAllWindows().length === 0) createWindow(); });