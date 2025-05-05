import sublime
import sublime_plugin
from datetime import datetime
from uuid import uuid4
import os

print("SaveThemAll plugin is loading...")

def expand_username(path):
    """Replace %username% in a path with the current user's username.
    Args:
        path: The path string containing %username% or other variables.
    Returns:
        str: The path with %username% replaced by the actual username.
    """
    # Try getting username from home directory
    try:
        username = os.path.basename(os.path.expanduser('~'))
        print(f"Using home dir username: {username}")
    except Exception as e:
        try:
            username = os.getlogin()
            print(f"Home dir failed: {e}, using os.getlogin(): {username}")
        except Exception as e2:
            username = os.environ.get('USER', os.environ.get('USERNAME', 'unknown'))
            print(f"os.getlogin() failed: {e2}, using USER/USERNAME env: {username}")
    return path.replace('%username%', username)

def save_view_as_temporary(view, tmp_dir=None):
    """Save a view as a temporary file with a generated name.
    
    Args:
        view: The Sublime Text view object.
        tmp_dir: Optional directory path to save the file. If None, determined automatically.
    
    Returns:
        bool: True if the file was saved successfully, False otherwise.
    """
    # Skip empty buffers to avoid saving files with no content
    if not view.size():
        return False
    # Skip read-only views to prevent errors
    if view.is_read_only():
        return False

    try:
        # Use provided tmp_dir or determine it based on project and date
        if tmp_dir is None:
            tmp_dir = get_temp_dir(view)
        
        # Load plugin settings for configuration
        settings = sublime.load_settings("SaveThemAll.sublime-settings")
        # Generate a unique filename with timestamp and UUID
        now = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        rnd = str(uuid4())[:8]
        ext = settings.get("default_extension", ".txt")
        tmp_name = f"{now}-{rnd}{ext}"

        # Construct full file path
        filename = os.path.join(tmp_dir, tmp_name)
        # Store temporary metadata in view settings
        view.settings().set("_tmp_name", tmp_name)
        view.settings().set("_tmp_dir", tmp_dir)
        # Set the view's display name
        view.set_name(tmp_name)

        # Save the file if it doesn't already exist
        if not os.path.exists(filename):
            view.retarget(filename)
            view.run_command("save")
            # Notify user of successful save
            sublime.status_message(f"Saved temporary file: {tmp_name}")
            return True
        return False
    except Exception as e:
        # Display error message in status bar
        sublime.status_message(f"Error saving temporary file: {str(e)}")
        print(f"Error saving file {filename}: {str(e)}")
        return False

def get_project_based_dir(view):
    """Determine the project-specific directory based on the file path.
    
    Args:
        view: The Sublime Text view object.
    
    Returns:
        str: The path to the project-specific directory or 'unsorted' if no match.
    """
    # Load plugin settings for base directory and project mappings
    settings = sublime.load_settings("SaveThemAll.sublime-settings")
    # Default to user's home directory if base_dir not specified
    base_dir = settings.get("base_dir", os.path.expanduser("~/Documents/sublime-project-autosaves"))
    # Expand %username% in base_dir
    base_dir = expand_username(base_dir)
    print(f"Base dir resolved to: {base_dir}")
    file_name = view.file_name()

    # Use unsorted directory for unsaved files
    if file_name is None:
        return os.path.join(base_dir, "unsorted")

    # Split file path into directory components
    directories = os.path.normpath(file_name).split(os.sep)
    # Load project mappings as a list of rules
    project_mappings = settings.get("project_mappings", [
        {"match": "private", "path": os.path.join(base_dir, "private")},
        {"match": "work", "path": os.path.join(base_dir, "work")},
        {"match": "unsorted", "path": os.path.join(base_dir, "unsorted")}
    ])

    # Check each directory against mapping rules
    for directory in directories:
        for mapping in project_mappings:
            # Match directory name against rule
            if mapping.get("match") in directory:
                # Expand %username% in the mapping path
                mapped_path = expand_username(mapping.get("path"))
                print(f"Matched mapping: {mapping.get('match')} -> {mapped_path}")
                return mapped_path
    
    # Fallback to unsorted directory if no project match
    unsorted_path = os.path.join(base_dir, "unsorted")
    print(f"No mapping matched, using unsorted: {unsorted_path}")
    return unsorted_path

def get_temp_dir(view):
    """Get or create a date-based directory for temporary files.
    
    Args:
        view: The Sublime Text view object.
    
    Returns:
        str: The path to the date-based directory.
    """
    try:
        # Get project-specific base directory
        project_dir = get_project_based_dir(view)
        # Create year/month/day subdirectories
        now = datetime.now()
        day_dir = os.path.join(project_dir, now.strftime("%Y"), now.strftime("%m"), now.strftime("%d"))
        print(f"Attempting to create directory: {day_dir}")
        # Create directories if they don't exist
        os.makedirs(day_dir, exist_ok=True)
        return day_dir
    except Exception as e:
        # Display error message if directory creation fails
        sublime.status_message(f"Error creating temporary directory: {str(e)}")
        print(f"Error creating directory {day_dir}: {str(e)}")
        return None

class SaveTemporaryBuffersCommand(sublime_plugin.WindowCommand):
    """Command to save all unsaved (temporary) buffers in the active window."""
    def run(self):
        # Track number of saved buffers
        saved_count = 0
        # Iterate through all views in the active window
        print(f"Processing views in active window")
        for view in self.window.views():
            # Only process unsaved buffers
            if view.file_name() is None:
                if save_view_as_temporary(view):
                    saved_count += 1
        # Provide user feedback
        if saved_count > 0:
            sublime.status_message(f"Saved {saved_count} temporary buffer(s) in active window")
        else:
            sublime.status_message("No unsaved buffers to save in active window")

class TemporaryFileEventListener(sublime_plugin.EventListener):
    """Event listener for handling new files and cleanup."""
    def on_new(self, view):
        """Set up a new file with a temporary name and directory."""
        # Load settings for default extension
        settings = sublime.load_settings("SaveThemAll.sublime-settings")
        ext = settings.get("default_extension", ".txt")
        # Get temporary directory
        tmp_dir = get_temp_dir(view)
        if tmp_dir is None:
            return

        # Generate unique temporary filename
        now = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        rnd = str(uuid4())[:8]
        tmp_name = f"{now}-{rnd}{ext}"

        try:
            # Store temporary metadata in view settings
            view.settings().set("_tmp_dir", tmp_dir)
            view.settings().set("_tmp_name", tmp_name)
            view.settings().set("default_dir", tmp_dir)
            # Set the view's display name
            view.set_name(tmp_name)
        except Exception as e:
            # Display error if setup fails
            sublime.status_message(f"Error setting up new file: {str(e)}")

    def on_save(self, view):
        """Clear temporary settings when a file is saved."""
        # Remove temporary metadata
        view.settings().erase("_tmp_dir")
        view.settings().erase("_tmp_name")

    def on_close(self, view):
        """Clear temporary settings when a view is closed."""
        # Clean up temporary metadata
        view.settings().erase("_tmp_dir")
        view.settings().erase("_tmp_name")

class SaveAllBuffersCommand(sublime_plugin.WindowCommand):
    """Command to save all unsaved buffers across all open windows."""
    def run(self):
        # Track number of saved buffers
        saved_count = 0
        # Iterate through all open windows
        windows = sublime.windows()
        print(f"Processing {len(windows)} open window(s)")
        for window in windows:
            # Iterate through all views in the window
            for view in window.views():
                # Only process unsaved buffers
                if view.file_name() is None:
                    if save_view_as_temporary(view):
                        saved_count += 1
        # Provide user feedback
        if saved_count > 0:
            sublime.status_message(f"Saved {saved_count} unsaved buffer(s) across {len(windows)} window(s)")
        else:
            sublime.status_message("No unsaved buffers to save across all windows")
