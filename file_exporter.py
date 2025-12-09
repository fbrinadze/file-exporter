"""
File Location Exporter - GUI Application
=========================================
A desktop application that scans a directory and exports all file names 
and paths to an Excel spreadsheet with the folder structure broken out 
into separate columns.

Requirements:
    - Python 3.x
    - pandas (pip install pandas)
    - openpyxl (pip install openpyxl)
    - python-docx (pip install python-docx) - for Word doc authors
    - python-pptx (pip install python-pptx) - for PowerPoint authors

To create a standalone .exe:
    python -m pip install pyinstaller
    python -m PyInstaller --onefile --windowed file_exporter.py
"""

import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from dotenv import set_key, load_dotenv

# Import core functions
from file_exporter_core import (
    parse_extensions,
    scan_directory,
    export_to_excel,
    get_root_folder_name
)

# Import notification functions
try:
    from includes.teams_notifier import (
        send_success_notification as teams_success,
        send_failure_notification as teams_failure
    )
    TEAMS_AVAILABLE = True
except ImportError:
    TEAMS_AVAILABLE = False
    print("Teams notifications not available. Install requests and python-dotenv to enable.")

try:
    from includes.email_notifier import (
        send_success_notification as email_success,
        send_failure_notification as email_failure
    )
    EMAIL_AVAILABLE = True
except ImportError:
    EMAIL_AVAILABLE = False
    print("Email notifications not available. Install python-dotenv to enable.")


class FileLocationExporter:
    """
    Main application class that creates the GUI and handles file export functionality.
    """
    
    def __init__(self, root):
        """
        Initialize the application window and create all UI elements.
        
        Args:
            root: The tkinter root window
        """
        
        # ============================================================
        # CANCEL FLAG
        # Used to signal the export process to stop early
        # ============================================================
        self.cancel_requested = False
        self.is_exporting = False
        
        # Store root reference for updates
        self.root = root
        
        # ============================================================
        # WINDOW SETUP
        # Configure the main application window
        # ============================================================
        root.title("File Location Exporter")
        root.geometry("600x500")
        root.resizable(False, False)
        
        # ============================================================
        # DIRECTORY SELECTION
        # Input field and browse button for selecting the folder to scan
        # ============================================================
        tk.Label(root, text="Directory to Scan:").pack(anchor="w", padx=10, pady=(15,0))
        frame_dir = tk.Frame(root)
        frame_dir.pack(fill="x", padx=10)
        self.directory_var = tk.StringVar()
        tk.Entry(frame_dir, textvariable=self.directory_var, width=60).pack(side="left")
        tk.Button(frame_dir, text="Browse", command=self.browse_directory).pack(side="left", padx=5)
        
        # Settings button
        tk.Button(frame_dir, text="⚙ Settings", command=self.open_settings).pack(side="left", padx=5)
        
        # ============================================================
        # ROOT FOLDER LABEL
        # A custom label that appears in the "RootFolder" column of the export
        # Auto-populated with the top-level folder name from selected directory
        # ============================================================
        tk.Label(root, text="Root Folder Label:").pack(anchor="w", padx=10, pady=(15,0))
        self.root_name_var = tk.StringVar()
        tk.Entry(root, textvariable=self.root_name_var, width=40).pack(anchor="w", padx=10)
        
        # ============================================================
        # FOLDER COLUMNS COUNT
        # Determines how many "Folder1", "Folder2", etc. columns to include
        # Each column represents one level of the directory structure
        # ============================================================
        tk.Label(root, text="Number of Folder Columns:").pack(anchor="w", padx=10, pady=(15,0))
        self.folder_cols_var = tk.IntVar(value=3)
        tk.Spinbox(root, from_=1, to=10, textvariable=self.folder_cols_var, width=10).pack(anchor="w", padx=10)
        
        # ============================================================
        # TITLE CASE OPTION
        # When enabled, converts folder names like "KEY ITEMS" to "Key Items"
        # ============================================================
        self.title_case_var = tk.BooleanVar(value=True)
        tk.Checkbutton(root, text="Convert folder names to Title Case", variable=self.title_case_var).pack(anchor="w", padx=10, pady=(15,0))
        
        # ============================================================
        # INCLUDE METADATA OPTIONS
        # Options to include file dates and author in the export
        # ============================================================
        self.include_dates_var = tk.BooleanVar(value=True)
        tk.Checkbutton(root, text="Include file dates (Created, Modified)", variable=self.include_dates_var).pack(anchor="w", padx=10, pady=(5,0))
        
        self.include_author_var = tk.BooleanVar(value=True)
        tk.Checkbutton(root, text="Include file author (Office files only)", variable=self.include_author_var).pack(anchor="w", padx=10, pady=(5,0))
        
        # ============================================================
        # FILE EXTENSION FILTER
        # Optional filter to only include specific file types
        # Leave blank to include all files
        # ============================================================
        tk.Label(root, text="File Extensions (comma-separated, leave blank for all):").pack(anchor="w", padx=10, pady=(15,0))
        self.extensions_var = tk.StringVar()
        tk.Entry(root, textvariable=self.extensions_var, width=40).pack(anchor="w", padx=10)
        tk.Label(root, text="Example: .psd, .tif, .pdf, .docx", fg="gray").pack(anchor="w", padx=10)
        
        # ============================================================
        # PROGRESS INDICATOR
        # Displays status messages during export
        # ============================================================
        self.progress_var = tk.StringVar(value="")
        tk.Label(root, textvariable=self.progress_var, fg="blue").pack(anchor="w", padx=10, pady=(15,0))
        
        # ============================================================
        # BUTTON FRAME
        # Contains Export and Cancel buttons side by side
        # ============================================================
        button_frame = tk.Frame(root)
        button_frame.pack(pady=20)
        
        # Export Button - Triggers the file scanning and Excel export process
        self.export_btn = tk.Button(
            button_frame, 
            text="Export to Excel", 
            command=self.export, 
            width=18, 
            height=2, 
            bg="#2E7D32",  # Darker green for better contrast
            fg="white",
            font=("Arial", 11, "bold"),
            activebackground="#1B5E20",  # Even darker when clicked
            activeforeground="white",
            relief="raised",
            bd=3,
            cursor="hand2"
        )
        self.export_btn.pack(side="left", padx=10)
        
        # Cancel Button - Stops the export process early
        self.cancel_btn = tk.Button(
            button_frame, 
            text="Cancel", 
            command=self.cancel_export, 
            width=18, 
            height=2, 
            bg="#C62828",  # Darker red for better contrast
            fg="yellow",  # Change this to your preferred color
            font=("Arial", 11, "bold"),
            activebackground="#8E0000",  # Even darker when clicked
            activeforeground="white",  # Change this too
            disabledforeground="white",  # And this for disabled state
            relief="raised",
            bd=3,
            cursor="hand2",
            state="disabled"  # Disabled until export starts
        )
        self.cancel_btn.pack(side="left", padx=10)
    
    
    def browse_directory(self):
        """
        Opens a folder selection dialog and updates the directory field.
        Auto-fills the Root Folder Label with the top-level folder name.
        """
        folder = filedialog.askdirectory()
        if folder:
            self.directory_var.set(folder)
            # Auto-fill root name with top-level folder name
            self.root_name_var.set(get_root_folder_name(folder))
    
    
    def open_settings(self):
        """
        Opens the settings dialog for configuring notifications.
        """
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Notification Settings")
        settings_window.geometry("600x500")
        settings_window.resizable(False, False)
        
        # Load current settings
        load_dotenv()
        
        # Create notebook for tabs
        notebook = ttk.Notebook(settings_window)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # ============================================================
        # EMAIL TAB
        # ============================================================
        email_frame = ttk.Frame(notebook)
        notebook.add(email_frame, text="Email Notifications")
        
        tk.Label(email_frame, text="Email Notification Settings", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Label(email_frame, text="Configure SMTP settings to receive email notifications", fg="gray").pack()
        
        # Enable/Disable checkbox
        email_enabled_var = tk.BooleanVar(value=os.getenv('EMAIL_ENABLED', 'false').lower() == 'true')
        enable_frame = tk.Frame(email_frame)
        enable_frame.pack(pady=10)
        tk.Checkbutton(
            enable_frame, 
            text="Enable Email Notifications", 
            variable=email_enabled_var,
            font=("Arial", 10, "bold")
        ).pack()
        
        # Email fields
        fields_frame = tk.Frame(email_frame)
        fields_frame.pack(pady=20, padx=20, fill="both")
        
        tk.Label(fields_frame, text="SMTP Server:").grid(row=0, column=0, sticky="w", pady=5)
        smtp_server = tk.Entry(fields_frame, width=40)
        smtp_server.insert(0, os.getenv('SMTP_SERVER', 'smtp.gmail.com'))
        smtp_server.grid(row=0, column=1, pady=5, padx=5)
        
        tk.Label(fields_frame, text="SMTP Port:").grid(row=1, column=0, sticky="w", pady=5)
        smtp_port = tk.Entry(fields_frame, width=40)
        smtp_port.insert(0, os.getenv('SMTP_PORT', '587'))
        smtp_port.grid(row=1, column=1, pady=5, padx=5)
        
        tk.Label(fields_frame, text="Username:").grid(row=2, column=0, sticky="w", pady=5)
        smtp_user = tk.Entry(fields_frame, width=40)
        smtp_user.insert(0, os.getenv('SMTP_USERNAME', ''))
        smtp_user.grid(row=2, column=1, pady=5, padx=5)
        
        tk.Label(fields_frame, text="Password:").grid(row=3, column=0, sticky="w", pady=5)
        smtp_pass = tk.Entry(fields_frame, width=40, show="*")
        smtp_pass.insert(0, os.getenv('SMTP_PASSWORD', ''))
        smtp_pass.grid(row=3, column=1, pady=5, padx=5)
        
        tk.Label(fields_frame, text="From Email:").grid(row=4, column=0, sticky="w", pady=5)
        from_email = tk.Entry(fields_frame, width=40)
        from_email.insert(0, os.getenv('FROM_EMAIL', ''))
        from_email.grid(row=4, column=1, pady=5, padx=5)
        
        tk.Label(fields_frame, text="To Email:").grid(row=5, column=0, sticky="w", pady=5)
        to_email = tk.Entry(fields_frame, width=40)
        to_email.insert(0, os.getenv('TO_EMAIL', ''))
        to_email.grid(row=5, column=1, pady=5, padx=5)
        
        # Quick presets
        tk.Label(email_frame, text="Quick Presets:", font=("Arial", 10, "bold")).pack(pady=(10,5))
        preset_frame = tk.Frame(email_frame)
        preset_frame.pack()
        
        def set_gmail():
            smtp_server.delete(0, tk.END)
            smtp_server.insert(0, "smtp.gmail.com")
            smtp_port.delete(0, tk.END)
            smtp_port.insert(0, "587")
        
        def set_outlook():
            smtp_server.delete(0, tk.END)
            smtp_server.insert(0, "smtp.office365.com")
            smtp_port.delete(0, tk.END)
            smtp_port.insert(0, "587")
        
        tk.Button(preset_frame, text="Gmail", command=set_gmail, width=10).pack(side="left", padx=5)
        tk.Button(preset_frame, text="Outlook", command=set_outlook, width=10).pack(side="left", padx=5)
        
        # ============================================================
        # TEAMS TAB
        # ============================================================
        teams_frame = ttk.Frame(notebook)
        notebook.add(teams_frame, text="Teams Notifications")
        
        tk.Label(teams_frame, text="MS Teams Notification Settings", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Label(teams_frame, text="Configure webhook URL to receive Teams notifications", fg="gray").pack()
        
        # Enable/Disable checkbox
        teams_enabled_var = tk.BooleanVar(value=os.getenv('TEAMS_ENABLED', 'false').lower() == 'true')
        teams_enable_frame = tk.Frame(teams_frame)
        teams_enable_frame.pack(pady=10)
        tk.Checkbutton(
            teams_enable_frame, 
            text="Enable Teams Notifications", 
            variable=teams_enabled_var,
            font=("Arial", 10, "bold")
        ).pack()
        
        teams_fields = tk.Frame(teams_frame)
        teams_fields.pack(pady=20, padx=20, fill="both")
        
        tk.Label(teams_fields, text="Webhook URL:").pack(anchor="w", pady=5)
        teams_webhook = tk.Entry(teams_fields, width=60)
        teams_webhook.insert(0, os.getenv('TEAMS_WEBHOOK_URL', ''))
        teams_webhook.pack(pady=5)
        
        tk.Label(teams_frame, text="How to get a webhook URL:", font=("Arial", 10, "bold")).pack(pady=(20,5))
        instructions = tk.Text(teams_frame, height=8, width=60, wrap="word")
        instructions.insert("1.0", 
            "1. Open MS Teams and go to your channel\n"
            "2. Click the three dots (...) next to the channel name\n"
            "3. Select 'Connectors' or 'Workflows'\n"
            "4. Search for 'Incoming Webhook'\n"
            "5. Click 'Add' or 'Configure'\n"
            "6. Give it a name and click 'Create'\n"
            "7. Copy the webhook URL and paste it above"
        )
        instructions.config(state="disabled")
        instructions.pack(pady=5)
        
        # ============================================================
        # SAVE BUTTON
        # ============================================================
        def save_settings():
            env_file = '.env'
            
            # Create .env if it doesn't exist
            if not os.path.exists(env_file):
                with open(env_file, 'w') as f:
                    f.write("# Notification Settings\n")
            
            # Save email enabled/disabled
            set_key(env_file, 'EMAIL_ENABLED', 'true' if email_enabled_var.get() else 'false')
            
            # Save email settings
            if smtp_server.get():
                set_key(env_file, 'SMTP_SERVER', smtp_server.get())
            if smtp_port.get():
                set_key(env_file, 'SMTP_PORT', smtp_port.get())
            if smtp_user.get():
                set_key(env_file, 'SMTP_USERNAME', smtp_user.get())
            if smtp_pass.get():
                set_key(env_file, 'SMTP_PASSWORD', smtp_pass.get())
            if from_email.get():
                set_key(env_file, 'FROM_EMAIL', from_email.get())
            if to_email.get():
                set_key(env_file, 'TO_EMAIL', to_email.get())
            
            # Save Teams enabled/disabled
            set_key(env_file, 'TEAMS_ENABLED', 'true' if teams_enabled_var.get() else 'false')
            
            # Save Teams settings
            if teams_webhook.get():
                set_key(env_file, 'TEAMS_WEBHOOK_URL', teams_webhook.get())
            
            messagebox.showinfo("Success", "Settings saved successfully!\n\nNotifications will be sent based on your enabled settings.")
            settings_window.destroy()
        
        button_frame = tk.Frame(settings_window)
        button_frame.pack(pady=10)
        
        tk.Button(
            button_frame, 
            text="Save Settings", 
            command=save_settings,
            width=15,
            height=2,
            bg="#2E7D32",
            fg="white",
            font=("Arial", 10, "bold")
        ).pack(side="left", padx=5)
        
        tk.Button(
            button_frame, 
            text="Cancel", 
            command=settings_window.destroy,
            width=15,
            height=2,
            bg="#757575",
            fg="white",
            font=("Arial", 10, "bold")
        ).pack(side="left", padx=5)
    
    
    def cancel_export(self):
        """
        Sets the cancel flag to stop the export process.
        Called when the Cancel button is clicked.
        """
        if self.is_exporting:
            self.cancel_requested = True
            self.progress_var.set("Cancelling...")
            self.root.update()
    
    
    def set_ui_state(self, exporting):
        """
        Enable/disable UI elements based on whether export is in progress.
        
        Args:
            exporting: True if export is running, False otherwise
        """
        self.is_exporting = exporting
        
        if exporting:
            self.export_btn.config(state="disabled")
            self.cancel_btn.config(state="normal")
        else:
            self.export_btn.config(state="normal")
            self.cancel_btn.config(state="disabled")
        
        self.root.update()
    
    
    def update_progress(self, file_count):
        """
        Callback function to update progress display.
        
        Args:
            file_count: Number of files scanned so far
        """
        self.progress_var.set(f"Scanned {file_count} files...")
        self.root.update()
    
    
    def check_cancel(self):
        """
        Callback function to check if cancellation was requested.
        
        Returns:
            bool: True if cancel was requested
        """
        return self.cancel_requested
    
    
    def check_network_drive(self, directory):
        """
        Check if directory is on a network drive and warn user.
        
        Args:
            directory: Path to check
            
        Returns:
            bool: True if user wants to continue, False to cancel
        """
        # Check for UNC paths
        if directory.startswith('\\\\'):
            response = messagebox.askyesno(
                "Network Drive Detected",
                "This appears to be a network drive (UNC path).\n\n"
                "The scan will use network-safe settings:\n"
                "• Throttled file access\n"
                "• Error recovery\n"
                "• Connection monitoring\n\n"
                "This may take longer than local drives.\n\n"
                "Continue?",
                icon='warning'
            )
            return response
        
        # Check for mapped network drives on Windows
        if os.name == 'nt':
            try:
                import subprocess
                drive = os.path.splitdrive(directory)[0]
                if drive:
                    result = subprocess.run(['net', 'use', drive], 
                                          capture_output=True, 
                                          text=True, 
                                          timeout=2)
                    if 'Remote name' in result.stdout or 'Remote' in result.stdout:
                        response = messagebox.askyesno(
                            "Network Drive Detected",
                            f"Drive {drive} appears to be a mapped network drive.\n\n"
                            "The scan will use network-safe settings:\n"
                            "• Throttled file access\n"
                            "• Error recovery\n"
                            "• Connection monitoring\n\n"
                            "This may take longer than local drives.\n\n"
                            "Continue?",
                            icon='warning'
                        )
                        return response
            except:
                pass
        
        return True  # Not a network drive or couldn't determine
    
    
    def export(self):
        """
        Main export function that:
        1. Validates user inputs
        2. Checks for network drives
        3. Scans the selected directory for files
        4. Exports the results to an Excel file
        5. Sends Teams notification on success or failure
        """
        
        try:
            # ============================================================
            # INPUT VALIDATION
            # Ensure a valid directory is selected before proceeding
            # ============================================================
            directory = self.directory_var.get()
            if not directory:
                messagebox.showerror("Error", "Please select a directory")
                return
            
            if not os.path.exists(directory):
                messagebox.showerror("Error", "Directory does not exist")
                return
            
            # ============================================================
            # NETWORK DRIVE CHECK
            # Warn user if scanning network drive
            # ============================================================
            if not self.check_network_drive(directory):
                return
            
            # ============================================================
            # OUTPUT FILE SELECTION
            # Prompt user to choose where to save the Excel file
            # ============================================================
            output_file = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")],
                initialfile="FileLocations.xlsx"
            )
            if not output_file:
                return
            
            # ============================================================
            # RESET CANCEL FLAG AND UPDATE UI
            # Prepare for new export operation
            # ============================================================
            self.cancel_requested = False
            self.set_ui_state(exporting=True)
            self.progress_var.set("Scanning files...")
            self.root.update()
            
            # ============================================================
            # PARSE SETTINGS
            # ============================================================
            extensions = parse_extensions(self.extensions_var.get())
            root_name = self.root_name_var.get() or get_root_folder_name(directory)
            
            # ============================================================
            # SCAN DIRECTORY
            # Uses core module function with callbacks for progress and cancel
            # ============================================================
            files = scan_directory(
                directory=directory,
                root_name=root_name,
                folder_cols=self.folder_cols_var.get(),
                title_case=self.title_case_var.get(),
                extensions=extensions,
                include_dates=self.include_dates_var.get(),
                include_author=self.include_author_var.get(),
                progress_callback=self.update_progress,
                cancel_check=self.check_cancel
            )
            
            # ============================================================
            # HANDLE CANCELLATION
            # ============================================================
            if self.cancel_requested:
                self.progress_var.set(f"Cancelled. Found {len(files)} files before stopping.")
                self.set_ui_state(exporting=False)
                messagebox.showinfo("Cancelled", f"Export cancelled.\n\n{len(files)} files were found before stopping.")
                return
            
            # ============================================================
            # VALIDATION
            # ============================================================
            if not files:
                messagebox.showwarning("Warning", "No files found")
                self.progress_var.set("")
                self.set_ui_state(exporting=False)
                
                error_msg = "No files found in selected directory"
                if TEAMS_AVAILABLE:
                    teams_failure(error_msg)
                if EMAIL_AVAILABLE:
                    email_failure(error_msg)
                return
            
            # ============================================================
            # EXPORT TO EXCEL
            # ============================================================
            self.progress_var.set("Exporting to Excel...")
            self.root.update()
            
            export_count = export_to_excel(files, output_file)
            
            # Reset UI state
            self.set_ui_state(exporting=False)
            
            # ============================================================
            # SEND SUCCESS NOTIFICATIONS
            # ============================================================
            if TEAMS_AVAILABLE or EMAIL_AVAILABLE:
                self.progress_var.set("Sending notifications...")
                self.root.update()
                
                if TEAMS_AVAILABLE:
                    teams_success(export_count, output_file)
                
                if EMAIL_AVAILABLE:
                    email_success(export_count, output_file)
            
            # Show completion message
            self.progress_var.set(f"Exported {export_count} files")
            messagebox.showinfo("Success", f"Exported {export_count} files to:\n{output_file}")
        
        except Exception as e:
            # ============================================================
            # HANDLE ERRORS AND SEND FAILURE NOTIFICATIONS
            # ============================================================
            error_msg = str(e)
            self.set_ui_state(exporting=False)
            self.progress_var.set("Export failed")
            messagebox.showerror("Error", f"Export failed:\n{error_msg}")
            
            if TEAMS_AVAILABLE:
                teams_failure(error_msg)
            if EMAIL_AVAILABLE:
                email_failure(error_msg)


# ============================================================
# APPLICATION ENTRY POINT
# Creates the main window and starts the application
# ============================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = FileLocationExporter(root)
    root.mainloop()
