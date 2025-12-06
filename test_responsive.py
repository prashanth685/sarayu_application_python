#!/usr/bin/env python3
"""
Test script for responsive design functionality
Tests the media query system and responsive behaviors
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import QTimer
import logging

# Import the dashboard components
from dashboard.dashboard_window import DashboardWindow
from database import Database

class ResponsiveTestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Responsive Design Test")
        self.setGeometry(100, 100, 1200, 800)
        
        # Setup logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        
        # Initialize database (in-memory for testing)
        self.db = Database(":memory:")
        
        # Create dashboard window
        self.dashboard = DashboardWindow(self.db, "test@example.com")
        self.setCentralWidget(self.dashboard)
        
        # Add test controls
        self.setup_test_controls()
        
        # Show window
        self.show()
        
        # Schedule automatic resize tests
        QTimer.singleShot(2000, self.run_resize_tests)
    
    def setup_test_controls(self):
        """Setup test controls for manual testing"""
        # Add resize buttons for testing different screen sizes
        test_widget = QWidget()
        layout = QVBoxLayout()
        
        # Add info label
        info_label = QLabel("Responsive Design Test Window")
        info_label.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px;")
        layout.addWidget(info_label)
        
        # Add resize buttons
        sizes = [
            ("Mobile (XS)", 320, 568),
            ("Mobile (L)", 414, 736),
            ("Tablet (Portrait)", 768, 1024),
            ("Tablet (Landscape)", 1024, 768),
            ("Desktop (Small)", 1280, 720),
            ("Desktop (Large)", 1920, 1080),
            ("Desktop (Ultra)", 2560, 1440)
        ]
        
        for name, width, height in sizes:
            btn = QPushButton(f"Resize to {name} ({width}x{height})")
            btn.clicked.connect(lambda checked, w=width, h=height: self.resize(w, h))
            layout.addWidget(btn)
        
        test_widget.setLayout(layout)
        test_widget.setWindowTitle("Test Controls")
        test_widget.show()
    
    def run_resize_tests(self):
        """Automatically test different window sizes"""
        sizes = [
            (320, 568),   # Mobile
            (768, 1024),  # Tablet
            (1280, 720),  # Desktop small
            (1920, 1080), # Desktop large
        ]
        
        self.current_test_index = 0
        self.test_sizes = sizes
        
        self.run_next_test()
    
    def run_next_test(self):
        """Run the next resize test"""
        if self.current_test_index < len(self.test_sizes):
            width, height = self.test_sizes[self.current_test_index]
            print(f"Testing size: {width}x{height}")
            
            # Resize window
            self.resize(width, height)
            
            # Log current breakpoint
            if hasattr(self.dashboard, 'media_query_manager'):
                breakpoint = self.dashboard.media_query_manager.get_current_breakpoint()
                print(f"Current breakpoint: {breakpoint.value if breakpoint else 'None'}")
            
            # Schedule next test
            self.current_test_index += 1
            QTimer.singleShot(3000, self.run_next_test)
        else:
            print("Resize tests completed!")
    
    def resizeEvent(self, event):
        """Handle resize events and log information"""
        super().resizeEvent(event)
        
        if hasattr(self.dashboard, 'media_query_manager'):
            mq = self.dashboard.media_query_manager
            breakpoint = mq.get_current_breakpoint()
            
            print(f"Window resized to: {self.width()}x{self.height()}")
            print(f"Breakpoint: {breakpoint.value if breakpoint else 'None'}")
            print(f"Is mobile: {mq.is_mobile()}")
            print(f"Is tablet: {mq.is_tablet()}")
            print(f"Is desktop: {mq.is_desktop()}")
            print(f"Recommended sidebar width: {mq.get_sidebar_width()}")
            print(f"Recommended toolbar height: {mq.get_toolbar_height()}")
            print(f"Recommended grid layout: {mq.get_grid_layout()}")
            print("-" * 50)

def main():
    app = QApplication(sys.argv)
    
    # Create test window
    test_window = ResponsiveTestWindow()
    
    # Run the application
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
