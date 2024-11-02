# osint-tool ScannerApp


ScannerApp is a simple Python-based GUI application for searching usernames across various platforms using Open Source Intelligence (OSINT) techniques. It allows you to check whether a specific username exists on different social media platforms, forums, and video platforms. The app is built using PyQt5 for the graphical user interface and utilizes asynchronous requests with aiohttp for fast and efficient searching.

## Features

Username Search: Search multiple usernames at once, separated by commas.

Category Selection: Select which type of platforms to search (e.g., Social Media, Forums, Video Platforms, or All).

Progress Bar: Shows the progress of ongoing searches.

Save Results: Save the search results to a text file.

Requirements

Python 3.7+

PyQt5

aiohttp

To install the necessary packages, you can use:

    pip install PyQt5 aiohttp


## Usage

To run the application, execute the following command:

    python osint.py

This will launch the GUI application where you can enter usernames, select a category, and start searching.

## Steps to Use the Application

Enter Usernames: Input the usernames you want to search for. You can enter multiple usernames by separating them with commas (e.g., user1, user2, user3).

Select Category: Choose the category of platforms to search in (e.g., Social Media, Forums).

Click Search: Press the "Search" button to start searching. The results will appear in the result area.

Save Results: Once the search is complete, you can save the results by clicking on the "Save Results" button.


## Project Structure
scanner_app.py: Main Python script containing the ScannerApp class and GUI logic.

logo.png: Logo for the application, referenced in the window icon.



## Key Components
PyQt5: Used for building the GUI.

aiohttp: For making asynchronous HTTP requests to different platforms to check for usernames.

QTextBrowser: Displays the search results with clickable links.

QProgressBar: Indicates the progress of the username search.



## Future Improvements
More Platforms: Add more platforms to extend the coverage of username searches.

Error Handling: Improve error handling for network issues and unexpected responses.

Threading: Optimize UI responsiveness during searches by moving I/O operations to separate threads.


## Contributing
Contributions are welcome! Please feel free to submit a Pull Request or open an Issue for suggestions or bug reports.






