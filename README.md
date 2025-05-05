# SaveThemAll – Sublime Text Plugin

**SaveThemAll** is a Sublime Text plugin that automatically saves unsaved buffers (files) to organized, project-based directories with timestamped names. It simplifies and speed-up file management by ensuring unsaved work is preserved in a structured, predictable way.

---
![SublimeTextLogo](https://www.sublimetext.com/images/logo.svg)
---

## Why SaveThemAll?

As a Network Engineer and developer, I often open multiple new tabs daily—quick notes, experiments, config checks, scratch code. Over time, it becomes impossible to remember which files are worth keeping and which are just junk. Manually saving and organizing them is tedious and breaks focus.

**SaveThemAll** was built to solve this: It captures and preserves unsaved buffers automatically, storing them in a clear, project-based structure with zero manual effort. Now I never lose valuable notes, and I don’t waste time closing or saving temporary files one by one.

And because all text buffers are saved—even the ones you forgot about—you can now **search for and find** that important idea or snippet days later. It’s probably sitting in the `unsorted` folder, **safely preserved**.

---

## Features

- Automatically names and saves unsaved buffers using a `dateclock-uuid` format.
- Organizes files by project (`private`, `work`, `unsorted`) and date (`year/month/day`).
- Saves unsaved buffers in the **active window** or **all open windows**, depending on the command.
- Configurable via `SaveThemAll.sublime-settings`, with support for the `%username%` variable for portable paths.
- Provides status bar feedback for save operations and errors.
- Skips empty or read-only buffers to avoid unnecessary saves.

---

## Requirements

- Sublime Text 3 or 4.
- macOS, Windows, or Linux (paths with `%username%` are supported cross-platform).

---

### Compatibility
- Sublime Text 3 (Build 3000 and above) and Sublime Text 4.
- Tested on macOS, Windows, and Linux. The `%username%` variable is resolved cross-platform using `os.path.expanduser('~')` and fallbacks.

--- 

## Installation

#### via Sublime Text Package Manager

1. Open Sublime Text.
2. Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (macOS) to open the Command Palette.
3. Type `Package Control: Install Package` and press Enter.
4. Search for `SaveThemAll` and select it to install.
5. Restart Sublime Text if prompted.



#### Manual Installation

1. **Save the Plugin Files**  
   Copy `SaveThemAll.py` and `SaveThemAll.sublime-settings` to your Sublime Text `Packages/User` directory:
   - **macOS**: `~/Library/Application Support/Sublime Text/Packages/User`
   - **Windows**: `%APPDATA%\Sublime Text\Packages\User`
2. **Restart Sublime Text**  
   Restart Sublime Text to load the plugin.

---

## Usage

1. **Create a New File**  
   Open a new file (`Ctrl+N` on Windows or `Super+N` on macOS). The plugin assigns a temporary name (e.g., `2025-05-01_123456-abcd1234.txt`).

2. **Save Unsaved Buffers**  
   Use the Command Palette (`Ctrl+Shift+P` on Windows or `Super+Shift+P` on macOS) to run:
   - `Save Temporary Buffers`: Saves all unsaved buffers in the active window.
   - `Save All Buffers`: Saves all unsaved buffers across all open windows.
   Files are saved to a project-based directory, such as:
   - **macOS**: `~/Documents/sublime-project-autosaves/unsorted/2025/05/01/`
   - **Windows**: `C:\Users\%username%\Documents\sublime-project-autosaves\unsorted\2025\05\01\`

3. **Check Feedback**  
   The status bar shows messages like `"Saved 2 temporary buffer(s) in active window"` or `"Saved 3 unsaved buffer(s) across 2 window(s)"`, or error details if something goes wrong.

4. **Project-Based Organization**  
   Files are saved to directories based on their project context (`private`, `work`, `unsorted`) as determined by their file path. Unsaved files default to the `unsorted` directory.

5. **Example**  
   - Open multiple Sublime Text windows, each with several unsaved tabs (e.g., notes in one window, code snippets in another).
   - To save only the active window’s unsaved tabs, press `Super+Opt+S` (macOS) or `Ctrl+Alt+S` (Windows).
   - To save all unsaved tabs across all windows, press `Super+Opt+Shift+S` (macOS) or `Ctrl+Alt+Shift+S` (Windows).
   - Files are saved, e.g., to `/Users/johndoe/Documents/sublime-project-autosaves/unsorted/2025/05/01/2025-05-01_123456-abcd1234.txt`.
   - Later, search your `unsorted` folder to find the notes using your OS’s search tools (e.g., Spotlight on macOS or File Explorer on Windows).

---

## Configuration

Edit `SaveThemAll.sublime-settings` in your `Packages/User` directory.

### Settings

- **`base_dir`**  
  Root directory for saved files.
  - **Default**:
    - macOS: `~/Documents/sublime-project-autosaves`
    - Windows: `C:\Users\%username%\Documents\sublime-project-autosaves`
  - **Example**:
    - macOS: `"base_dir": "/Users/%username%/Documents/my-autosaves"`
    - Windows: `"base_dir": "C:\\Users\\%username%\\Documents\\my-autosaves"`

- **`default_extension`**  
  Default file extension for saved files.
  - **Default**: `.txt`
  - **Example**: `"default_extension": ".md"`

- **`project_mappings`**  
  Maps parts of a file path to named save directories.
  - **Default**:
    ```json
    [
        {"match": "private", "path": "~/Documents/sublime-project-autosaves/private"},
        {"match": "work", "path": "~/Documents/sublime-project-autosaves/work"},
        {"match": "unsorted", "path": "~/Documents/sublime-project-autosaves/unsorted"}
    ]
    ```
  - **Example**:
    ```json
    [
        {"match": "personal", "path": "~/Documents/sublime-project-autosaves/personal"},
        {"match": "projects", "path": "~/Documents/sublime-project-autosaves/projects"}
    ]
    ```
  - **Notes**:
    - `match` is case-sensitive and supports partial matches (e.g., `work` matches `work-project`).
    - `path` supports `%username%`, which expands to the current user’s username (e.g., `johndoe`).
    - The first matching rule determines the save path; otherwise, `base_dir/unsorted` is used.

---

### Keybindings (Optional)

Add to `Default.sublime-keymap` in `Packages/User`.

#### macOS:

```json
[
    {"keys": ["super+option+s"], "command": "save_temporary_buffers"},
    {"keys": ["super+option+shift+s"], "command": "save_all_buffers"}
]
```

#### Windows:

```json
[
    {"keys": ["ctrl+alt+s"], "command": "save_temporary_buffers"},
    {"keys": ["ctrl+alt+shift+s"], "command": "save_all_buffers"}
]
```

---

## Commands

The plugin provides two commands to save unsaved buffers, accessible via the Command Palette (`Ctrl+Shift+P` on Windows or `Super+Shift+P` on macOS) or custom keybindings (see above).

- **`SaveTemporaryBuffersCommand`**  
  - **Purpose**: Saves all unsaved buffers (files without a file name) in the **active window**.
  - **Behavior**: For each unsaved buffer in the active window, the plugin generates a unique filename in the format `YYYY-MM-DD_HHMMSS-uuid8.ext` (e.g., `2025-05-01_123456-abcd1234.txt`, where `ext` is set by `default_extension` in settings). Files are saved to a directory determined by the project context (`private`, `work`, or `unsorted`) and organized by date (`year/month/day`).
  - **Use Case**: Ideal for quickly saving temporary buffers in the current window, such as notes or code snippets, without affecting other open windows.
  - **Trigger**: Run via the Command Palette by selecting `Save Temporary Buffers` or use the keybinding (`Super+Opt+S` on macOS or `Ctrl+Alt+S` on Windows).
  - **Feedback**: The status bar shows the number of buffers saved (e.g., "Saved 3 temporary buffer(s) in active window") or "No unsaved buffers to save in active window" if none exist. Errors (e.g., permission issues) are displayed in the status bar.
  - **Notes**: Skips empty or read-only buffers and does not affect files with existing names.

- **`SaveAllBuffersCommand`**  
  - **Purpose**: Saves all unsaved buffers across **all open windows**.
  - **Behavior**: Processes all unsaved buffers in every open window, applying the same `dateclock-uuid` naming convention and saving to project-based, date-organized directories. It does not save files that already have a file name.
  - **Use Case**: Useful for saving all temporary buffers across multiple projects or windows, ensuring no unsaved work is lost when working with multiple Sublime Text instances.
  - **Trigger**: Run via the Command Palette by selecting `Save All Buffers` or use the keybinding (`Super+Opt+Shift+S` on macOS or `Ctrl+Alt+Shift+S` on Windows).
  - **Feedback**: The status bar shows the number of buffers saved (e.g., "Saved 5 unsaved buffer(s) across 2 window(s)") or "No unsaved buffers to save across all windows" if none exist. Errors are displayed in the status bar.
  - **Notes**: Skips empty or read-only buffers and does not affect files with existing names.

Both commands ensure that only unsaved buffers are processed, preserving the integrity of named files. They integrate with the plugin’s configuration, using settings like `base_dir`, `default_extension`, and `project_mappings` to determine save locations.

---

## How It Works

- **Naming**: `YYYY-MM-DD_HHMMSS-uuid8.ext` (e.g., `2025-05-01_123456-abcd1234.txt`)
- **Scope**: Unsaved buffers in the active window (`SaveTemporaryBuffersCommand`) or all open windows (`SaveAllBuffersCommand`).
- **Structure**:
  ```
  base_dir/
  └── project/
      └── YYYY/
          └── MM/
              └── DD/
  ```
- **Error Handling**: Errors are shown in the status bar; safe defaults are used.

---

## Troubleshooting

- **Plugin not loading**:
  - Ensure `SaveThemAll.py` and `SaveThemAll.sublime-settings` are in `Packages/User` (e.g., `~/Library/Application Support/Sublime Text/Packages/User` on macOS).
  - Open the Sublime Text console (`Ctrl+`` or `Super+``) and check for errors related to `SaveThemAll`.
  - Add `print("SaveThemAll plugin is loading...")` at the top of `SaveThemAll.py` to verify loading.
  - Restart Sublime Text after moving files or making changes.
- **Permission denied errors**:
  - If you see errors like `[Errno 13] Permission denied: '/Users/root'`, the `%username%` variable may not be expanding correctly.
  - Verify that `base_dir` in `SaveThemAll.sublime-settings` uses a valid path (e.g., `/Users/%username%/Documents/sublime-project-autosaves`).
  - Check write permissions for the target directory:
    ```bash
    mkdir -p ~/Documents/sublime-project-autosaves/unsorted
    chmod u+rwx ~/Documents/sublime-project-autosaves
    ```
  - Ensure Sublime Text is running as your user (e.g., `johndoe`), not `root`. Check the process:
    ```bash
    ps aux | grep Sublime
    ```
  - If `os.getlogin()` returns `root`, ensure `SaveThemAll.py` uses `os.path.expanduser('~')` for username resolution.
- **Files not saving**:
  - Verify write permissions for `base_dir` (e.g., `/Users/johndoe/Documents/sublime-project-autosaves`).
  - Ensure `%username%` resolves correctly (e.g., `/Users/johndoe/...`).
  - Check for errors in the console when running commands.
- **Wrong directory**:
  - Verify `project_mappings` in `SaveThemAll.sublime-settings`. The `match` field should align with directory names in your file paths.
- **Keybindings not working**:
  - Confirm the keymap file is in `Packages/User/Default.sublime-keymap` and contains valid JSON.
  - Check for conflicts with other keybindings in the Sublime Text console.
- **General issues**:
  - Clear the Sublime Text cache: `rm -rf ~/Library/Application Support/Sublime Text/Cache/*`.
  - Ensure you’re using Sublime Text 3 or 4 (check via `Sublime Text > About Sublime Text`).
  - Test with a minimal plugin to confirm the Python environment:
    ```python
    # Packages/User/TestPlugin.py
    import sublime_plugin
    print("TestPlugin is loading...")
    ```

---

## Contributing

Contributions are welcome! Please submit issues or pull requests on the [GitHub repository](https://github.com/yourusername/SaveThemAll) for bug reports, feature requests, or improvements.

---

## License

This plugin is licensed under the [MIT License](LICENSE).

---

## Notes

- `%username%` is automatically replaced by the current system username (e.g., `johndoe` on macOS or Windows).
