// main.js

// Modules to control application life and create native browser window
const { app, BrowserWindow } = require('electron');

const path = require('node:path')

const isDev = process.env.NODE_ENV !== 'development';

const createWindow = () => {
  // Create the browser window.
  const mainWindow = new BrowserWindow({
    title: 'GE_Ev_ChargingStation',
    width: 1024,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js')
    }
  })

  if (isDev) {
    mainWindow.webContents.openDevTools();
  }

  // and load the index.html of the app.
  mainWindow.loadFile('renderer/html/index.html');
  mainWindow.reload(true);
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.whenReady().then(() => {
  createWindow()

  app.on('activate', () => {
    // On macOS it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})


