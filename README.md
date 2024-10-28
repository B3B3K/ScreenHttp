# Screen Share Web App

This project is a Flask-based web application designed to provide a live screen-sharing feed with an interactive command console. Users can select a screen to share, view the feed, and enter commands to be executed on the server.

## Features

- **Live Screen Feed**: View a real-time feed of a selected screen on the server.
- **Screen Selection**: Choose between available screens to stream live.
- **Command Console**: Execute shell commands directly through the web page.
- **Responsive Interface**: A dark-themed, responsive web interface with a left panel for screen feed and a right panel for the command console.
- **Kill session with /kill page**: Easy exit without popup.
## Libraries Used

### Flask

Flask is used as the main framework for serving web pages and handling requests. The application uses Flask's routing, templates, and JSON responses.

- **Flask**: The core web framework.
- **Flask-Bootstrap**: For Bootstrap integration, providing a consistent layout and responsive design.

### PIL (Python Imaging Library)

PIL is used to capture and manipulate screen images, converting them into JPEG format for efficient web streaming.

- **Pillow**: The modern version of PIL, used here to handle image capture and conversion.

### mss

`mss` is a cross-platform library for capturing screen data. It allows for efficient screen grabbing, essential for creating the real-time feed.

### Subprocess

The `subprocess` module is used to run shell commands from the web console and capture their output.

### Other Utilities

- **Threading**: Manages continuous screen capture without blocking other processes.
- **Base64**: Encodes the JPEG screen feed as a Base64 string to be served as an image source in the web interface.
- **Signal**: Used to gracefully shut down the server on demand.

## Web Page Settings and Recommendations

### Layout

The web interface is divided into two main sections:
1. **Left Panel (Screen Feed)**: Displays the live screen feed with a dropdown and a button to select the screen. The selected screen updates dynamically every 0.2 seconds (5 FPS).
2. **Right Panel (Command Console)**: Contains a console area to view command outputs and a text input for entering commands. The background is black, with white text for improved visibility and readability.

### Styles and Interactivity

- **Dark Theme**: The page has a dark theme for easier viewing in various environments.
- **Responsive Design**: Adapts to different screen sizes, with CSS ensuring the layout remains flexible.
- **Clear Command**: Users can type `clear` or `cls` in the console to reset the command output.

### Recommendations

- **Security**: Update the `app.secret_key` with a secure, unique key to protect session data.
- **Usage in a Controlled Environment**: This application should only be used in a secure, local network. Running shell commands from a web interface poses significant security risks if exposed to untrusted networks.
- **Screen Refresh Rate**: The screen capture FPS is set to 60 by default to balance performance and update speed. Adjust if needed for your system's capabilities.

## Running the App

1. Install the required libraries:
   ```bash
   pip install flask flask-bootstrap pillow mss
   ```

2. Run the application:
   ```bash
   python screenshare2.pyw
   ```

3. Access the application via a web browser at `http://localhost:3131`.

4. Use the screen selection dropdown to choose the screen to share. Type commands in the console and press Enter to execute.
4. Wrote by ChatGPT
