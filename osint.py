import sys
import asyncio
import aiohttp
import ssl
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLineEdit, QLabel, QFileDialog, QGroupBox, QTextBrowser, QProgressBar,
                             QComboBox, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QTextCursor, QIcon

class ScannerApp(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("ScannerApp")
        self.setWindowIcon(QIcon("C:/Users/yusuf/OneDrive/Belgeler/GitHub/osint-tool/logo.png"))
        self.resize(600, 600)
        self.initUI()
        
    def initUI(self):
        main_layout = QVBoxLayout()
        
        # User Input Group
        user_input_group = QGroupBox("Search Username (You can search multiple usernames by separating them with commas.)")
        user_input_group.setStyleSheet("""
        QGroupBox {
            border: 2px solid #8f91;
            border-radius: 10px;
            margin-top: 20px;
            padding: 10px;
            background-color: #f9f9f9;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top center;
            padding: 0 10px;
            color: #8f91;
            font-weight: bold;
            font-size: 14pt;
        }
        """)
        
        user_input_layout = QVBoxLayout()
        
        # Username Input
        self.label = QLabel("Username:")
        self.label.setFont(QFont('Arial', 12, QFont.Bold))
        self.label.setStyleSheet("color: #333;")
        
        self.username_input = QLineEdit()
        self.username_input.setStyleSheet("border: 2px solid #8f91; border-radius: 5px; padding: 5px;")
        self.username_input.setPlaceholderText("Enter username")
        self.username_input.returnPressed.connect(self.search_username)
        
        # Category Selection
        category_layout = QHBoxLayout()
        self.category_label = QLabel("Category Selection:")
        self.category_label.setFont(QFont('Arial', 12, QFont.Bold))
        self.category_label.setStyleSheet("color: #333;")
        
        self.category_selector = QComboBox()
        self.category_selector.addItems(["All", "Social Media", "Forums", "Video Platforms"])
        self.category_selector.setFont(QFont('Arial', 12))
        self.category_selector.setStyleSheet("border: 2px solid #8f91; border-radius: 5px; padding: 5px;")
        
        category_layout.addWidget(self.category_label)
        category_layout.addWidget(self.category_selector)
        
        # Search Button
        self.search_button = QPushButton("Search")
        self.search_button.setFont(QFont('Arial', 12))
        self.search_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px;")
        self.search_button.clicked.connect(self.search_username)
        
        # Save Results Button
        self.save_button = QPushButton("Save Results")
        self.save_button.setFont(QFont('Arial', 12))
        self.save_button.setStyleSheet("background-color: #008CBA; color: white; padding: 10px; border-radius: 5px;")
        self.save_button.clicked.connect(self.save_results)
        
        # Add Buttons to Layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.search_button)
        button_layout.addWidget(self.save_button)
        
        # Progress Bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet("""
        QProgressBar {
            border: 2px solid #8f91;
            border-radius: 5px;
            background: #e0e0e0;
        }
        QProgressBar::chunk {
            background-color: #4CAF50;
            width: 20px;
        }
        """)
        
        # Result Area
        self.result_area = QTextBrowser()
        self.result_area.setFont(QFont('Arial', 11))
        self.result_area.setStyleSheet("border: 2px solid #8f91; border-radius: 5px; padding: 10px;")
        self.result_area.setPlaceholderText("Search results will appear here...")
        self.result_area.setOpenExternalLinks(True)
        
        # Add User Input Layout
        user_input_layout.addWidget(self.label)
        user_input_layout.addWidget(self.username_input)
        user_input_layout.addLayout(category_layout)
        user_input_layout.addLayout(button_layout)
        user_input_layout.addWidget(self.progress_bar)
        user_input_group.setLayout(user_input_layout)
        
        # Add to Main Layout
        main_layout.addWidget(user_input_group)
        main_layout.addWidget(self.result_area)
        self.setLayout(main_layout)
        
        # Initialize results list
        self.results = []

    def search_username(self):
        usernames = self.username_input.text().split(',')
        if not usernames[0]:
            QMessageBox.warning(self, "Error", "Please enter at least one username.")
            return
        self.result_area.clear()
        self.results = []
        self.progress_bar.setValue(0)

        selected_category = self.category_selector.currentText()

        for username in usernames:
            username = username.strip()
            if username:
                self.result_area.append(f"Searching for user '{username}'...\n")
                asyncio.run(self.run_search(username, selected_category))

    async def run_search(self, username, category):
        sites = [
            {"name": "GitHub", "url": f"https://api.github.com/users/{username}", "api": True, "category": "All"},
            {"name": "Reddit", "url": f"https://www.reddit.com/user/{username}", "api": False, "category": "Forums"},
            {"name": "Instagram", "url": f"https://www.instagram.com/{username}/", "api": False, "category": "Social Media"},
            {"name": "Twitter", "url": f"https://twitter.com/{username}", "api": False, "category": "Social Media"},
            {"name": "LinkedIn", "url": f"https://www.linkedin.com/in/{username}/", "api": False, "category": "Social Media"}
            # Add more sites as needed
        ]

        if category != "All":
            sites = [site for site in sites if site['category'] == category]
        total_sites = len(sites)
        tasks = []
        async with aiohttp.ClientSession() as session:
            for index, site in enumerate(sites):
                if site['api']:
                    tasks.append(self.search_api(username, site, session))
                else:
                    tasks.append(self.search_website(username, site, session))
                progress = int(((index + 1) / total_sites) * 100)
                self.progress_bar.setValue(progress)

            results = await asyncio.gather(*tasks)

        for result in results:
            self.result_area.append(result)
            self.result_area.moveCursor(QTextCursor.Start)
            self.results.append(result)
        QMessageBox.information(self, "Info", "Search Completed!")

    async def search_api(self, username, site, session):
        try:
            async with session.get(site['url']) as response:
                if response.status == 200:
                    data = await response.json()
                    profile_url = data.get("html_url")
                    if profile_url:
                        return self.format_result(username, site['name'], profile_url, True)
                    else:
                        return self.format_result(username, site['name'], site['url'], True)
                else:
                    return self.format_result(username, site['name'], site['url'], False)
        except Exception as e:
            return f"Error on {site['name']}: {str(e)}"

    async def search_website(self, username, site, session, ssl_context=None):
        try:
            async with session.get(site["url"], ssl=ssl_context) as response:
                if response.status == 200:
                    return self.format_result(username, site["name"], site["url"], True)
                else:
                    return self.format_result(username, site["name"], site["url"], False)
        except Exception as e:
            return f"Error on {site['name']}: {str(e)}"

    def format_result(self, username, site_name, url, found):
        if found:
            icon = "✔️"
            link = f'<a href="{url}" style="text-decoration:none; color:#4CAF50;">{username} found on {site_name} {icon}</a>'
            return f'<div>{link}</div>'
        else:
            icon = "❌"
            return f'<div style="color:#f44336;">{username} not found on {site_name} {icon}'

    def save_results(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getSaveFileName(self, "Save Results", "", "Text Files (*.txt)", options=options)
        if filename:
            if filename.endswith('.txt'):
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(self.result_area.toPlainText())
                    QMessageBox.information(self, "Info", "Save Completed!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    scanner = ScannerApp()
    scanner.show()
    sys.exit(app.exec_())
