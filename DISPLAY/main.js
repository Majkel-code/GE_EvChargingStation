

// Modules to control application life and create native browser window
const { app, BrowserWindow } = require('electron');
const { platform } = require('node:os');
const os = require("os");


const path = require('node:path');

const createWindow = () => {
  // Create the browser window.
  const mainWindow = new BrowserWindow({
    title: 'GE_Ev_ChargingStation',
    width: 1024,
    height: 600,
    maxHeight: 600,
    maxWidth: 1024,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js')
    },
    resizable: false,
    frame: false,
  })
  // and load the index.html of the app.
  mainWindow.loadFile('renderer/html/index.html');
  mainWindow.reload(true);


  if (os.type() === 'Linux'){
    mainWindow.fullScreen = true;

    // Preven windows to be closed
    mainWindow.on('close', e => {
      e.preventDefault();
    });
  }
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


