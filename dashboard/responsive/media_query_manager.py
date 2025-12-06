"""
Media Query Manager for Responsive Design
Handles window size detection and responsive layout adjustments
"""

from PyQt5.QtCore import QObject, pyqtSignal, QTimer
from PyQt5.QtWidgets import QWidget
import logging
from enum import Enum


class Breakpoint(Enum):
    """Breakpoint categories for responsive design"""
    EXTRA_SMALL = "xs"  # < 576px
    SMALL = "sm"        # 576px - 768px
    MEDIUM = "md"       # 768px - 992px
    LARGE = "lg"        # 992px - 1200px
    EXTRA_LARGE = "xl"  # 1200px - 1400px
    EXTRA_EXTRA_LARGE = "xxl"  # > 1400px


class MediaQueryManager(QObject):
    """
    Media query manager that monitors window size changes
    and emits signals for responsive layout adjustments
    """
    
    # Signals emitted when breakpoints are reached
    breakpoint_changed = pyqtSignal(str, str)  # old_breakpoint, new_breakpoint
    window_resized = pyqtSignal(int, int)      # width, height
    
    # Specific breakpoint signals
    entered_extra_small = pyqtSignal()
    entered_small = pyqtSignal()
    entered_medium = pyqtSignal()
    entered_large = pyqtSignal()
    entered_extra_large = pyqtSignal()
    entered_extra_extra_large = pyqtSignal()
    
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        self.current_breakpoint = None
        self.previous_breakpoint = None
        self.debounce_timer = QTimer()
        self.debounce_timer.setSingleShot(True)
        self.debounce_timer.timeout.connect(self._handle_resize)
        
        # Breakpoint thresholds in pixels
        self.breakpoints = {
            Breakpoint.EXTRA_SMALL: (0, 575),
            Breakpoint.SMALL: (576, 767),
            Breakpoint.MEDIUM: (768, 991),
            Breakpoint.LARGE: (992, 1199),
            Breakpoint.EXTRA_LARGE: (1200, 1399),
            Breakpoint.EXTRA_EXTRA_LARGE: (1400, float('inf'))
        }
        
        # Initialize with current window size
        if self.parent_window.isVisible():
            self._update_breakpoint()
    
    def start_monitoring(self):
        """Start monitoring window resize events"""
        self.parent_window.resizeEvent = self._on_resize_event
    
    def _on_resize_event(self, event):
        """Handle window resize events with debouncing"""
        # Call original resize event if it exists
        original_resize = getattr(self.parent_window.__class__, 'resizeEvent', None)
        if original_resize:
            original_resize(self.parent_window, event)
        
        # Emit window resized signal
        self.window_resized.emit(self.parent_window.width(), self.parent_window.height())
        
        # Debounce breakpoint checking
        self.debounce_timer.start(150)  # 150ms debounce
    
    def _handle_resize(self):
        """Handle debounced resize event"""
        self._update_breakpoint()
    
    def _update_breakpoint(self):
        """Update current breakpoint based on window width"""
        width = self.parent_window.width()
        new_breakpoint = self._get_breakpoint(width)
        
        if new_breakpoint != self.current_breakpoint:
            self.previous_breakpoint = self.current_breakpoint
            self.current_breakpoint = new_breakpoint
            
            # Emit breakpoint changed signal
            old_bp = self.previous_breakpoint.value if self.previous_breakpoint else None
            new_bp = self.current_breakpoint.value
            self.breakpoint_changed.emit(old_bp, new_bp)
            
            # Emit specific breakpoint signals
            self._emit_breakpoint_signal(new_breakpoint)
            
            logging.info(f"Breakpoint changed: {old_bp} -> {new_bp} (width: {width}px)")
    
    def _get_breakpoint(self, width):
        """Get breakpoint for given width"""
        for breakpoint, (min_width, max_width) in self.breakpoints.items():
            if min_width <= width <= max_width:
                return breakpoint
        return Breakpoint.SMALL  # Default fallback
    
    def _emit_breakpoint_signal(self, breakpoint):
        """Emit signal for specific breakpoint"""
        signal_map = {
            Breakpoint.EXTRA_SMALL: self.entered_extra_small,
            Breakpoint.SMALL: self.entered_small,
            Breakpoint.MEDIUM: self.entered_medium,
            Breakpoint.LARGE: self.entered_large,
            Breakpoint.EXTRA_LARGE: self.entered_extra_large,
            Breakpoint.EXTRA_EXTRA_LARGE: self.entered_extra_extra_large
        }
        signal = signal_map.get(breakpoint)
        if signal:
            signal.emit()
    
    def get_current_breakpoint(self):
        """Get current breakpoint"""
        return self.current_breakpoint
    
    def is_mobile(self):
        """Check if current size is mobile (xs or sm)"""
        return self.current_breakpoint in [Breakpoint.EXTRA_SMALL, Breakpoint.SMALL]
    
    def is_tablet(self):
        """Check if current size is tablet (md)"""
        return self.current_breakpoint == Breakpoint.MEDIUM
    
    def is_desktop(self):
        """Check if current size is desktop (lg, xl, xxl)"""
        return self.current_breakpoint in [Breakpoint.LARGE, Breakpoint.EXTRA_LARGE, Breakpoint.EXTRA_EXTRA_LARGE]
    
    def get_sidebar_width(self):
        """Get recommended sidebar width for current breakpoint"""
        width_map = {
            Breakpoint.EXTRA_SMALL: 50,   # Collapsed
            Breakpoint.SMALL: 200,        # Narrow
            Breakpoint.MEDIUM: 250,       # Medium
            Breakpoint.LARGE: 300,        # Full
            Breakpoint.EXTRA_LARGE: 300,  # Full
            Breakpoint.EXTRA_EXTRA_LARGE: 300  # Full
        }
        return width_map.get(self.current_breakpoint, 300)
    
    def get_toolbar_height(self):
        """Get recommended toolbar height for current breakpoint"""
        height_map = {
            Breakpoint.EXTRA_SMALL: 60,   # Compact
            Breakpoint.SMALL: 70,        # Compact
            Breakpoint.MEDIUM: 80,       # Normal
            Breakpoint.LARGE: 80,        # Normal
            Breakpoint.EXTRA_LARGE: 80,  # Normal
            Breakpoint.EXTRA_EXTRA_LARGE: 80  # Normal
        }
        return height_map.get(self.current_breakpoint, 80)
    
    def get_console_height(self):
        """Get recommended console height for current breakpoint"""
        height_map = {
            Breakpoint.EXTRA_SMALL: 60,   # Minimal
            Breakpoint.SMALL: 80,        # Small
            Breakpoint.MEDIUM: 80,       # Normal
            Breakpoint.LARGE: 80,        # Normal
            Breakpoint.EXTRA_LARGE: 80,  # Normal
            Breakpoint.EXTRA_EXTRA_LARGE: 80  # Normal
        }
        return height_map.get(self.current_breakpoint, 80)
    
    def get_grid_layout(self):
        """Get recommended grid layout for current breakpoint"""
        layout_map = {
            Breakpoint.EXTRA_SMALL: "1x1",      # Single column
            Breakpoint.SMALL: "1x2",            # Single row
            Breakpoint.MEDIUM: "2x2",           # 2x2 grid
            Breakpoint.LARGE: "2x2",            # 2x2 grid
            Breakpoint.EXTRA_LARGE: "2x3",       # 2x3 grid
            Breakpoint.EXTRA_EXTRA_LARGE: "3x3"  # 3x3 grid
        }
        return layout_map.get(self.current_breakpoint, "2x2")
    
    def should_collapse_sidebar(self):
        """Check if sidebar should be collapsed for current breakpoint"""
        return self.current_breakpoint in [Breakpoint.EXTRA_SMALL, Breakpoint.SMALL]
    
    def should_hide_toolbar_labels(self):
        """Check if toolbar labels should be hidden for current breakpoint"""
        return self.current_breakpoint == Breakpoint.EXTRA_SMALL


class ResponsiveMixin:
    """
    Mixin class to add responsive capabilities to widgets
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._media_query_manager = None
        self._responsive_styles = {}
    
    def set_media_query_manager(self, manager):
        """Set the media query manager for this widget"""
        self._media_query_manager = manager
        if manager:
            manager.breakpoint_changed.connect(self._on_breakpoint_changed)
            # Apply initial breakpoint styles
            self._apply_breakpoint_styles(manager.get_current_breakpoint())
    
    def _on_breakpoint_changed(self, old_breakpoint, new_breakpoint):
        """Handle breakpoint change"""
        self._apply_breakpoint_styles(new_breakpoint)
    
    def _apply_breakpoint_styles(self, breakpoint):
        """Apply styles for current breakpoint"""
        if breakpoint in self._responsive_styles:
            styles = self._responsive_styles[breakpoint]
            if hasattr(self, 'setStyleSheet'):
                self.setStyleSheet(styles)
    
    def add_responsive_style(self, breakpoint, stylesheet):
        """Add responsive stylesheet for a specific breakpoint"""
        if isinstance(breakpoint, str):
            breakpoint = Breakpoint(breakpoint)
        self._responsive_styles[breakpoint] = stylesheet
    
    def get_media_query_manager(self):
        """Get the media query manager"""
        return self._media_query_manager
