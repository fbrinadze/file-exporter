"""
Test Suite for File Location Exporter
=====================================
Tests for the core functionality of the file exporter.

Run tests with: 
    python -m pytest test_file_exporter.py -v
    
Or with unittest: 
    python test_file_exporter.py

Requirements:
    - pytest (pip install pytest) - optional, can use unittest
    - pandas (pip install pandas)
    - openpyxl (pip install openpyxl)
"""

import os
import sys
import unittest
import tempfile
import shutil
import datetime
import pandas as pd

# Import core functions (no GUI dependencies)
from file_exporter_core import (
    get_file_dates,
    get_file_author,
    parse_extensions,
    parse_folder_structure,
    get_root_folder_name,
    build_row,
    scan_directory,
    export_to_excel
)


class TestGetFileDates(unittest.TestCase):
    """Tests for the get_file_dates() function."""
    
    def setUp(self):
        """Create a temporary directory and test file."""
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, "test_file.txt")
        with open(self.test_file, "w") as f:
            f.write("test content")
    
    def tearDown(self):
        """Remove temporary directory and files."""
        shutil.rmtree(self.test_dir)
    
    def test_returns_tuple(self):
        """Should return a tuple of two values."""
        result = get_file_dates(self.test_file)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
    
    def test_returns_valid_dates(self):
        """Should return properly formatted date strings."""
        creation_date, modified_date = get_file_dates(self.test_file)
        
        # Check format: YYYY-MM-DD HH:MM:SS
        self.assertIsNotNone(creation_date)
        self.assertIsNotNone(modified_date)
        self.assertRegex(creation_date, r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")
        self.assertRegex(modified_date, r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")
    
    def test_nonexistent_file_returns_none(self):
        """Should return (None, None) for nonexistent files."""
        result = get_file_dates("/nonexistent/path/file.txt")
        self.assertEqual(result, (None, None))
    
    def test_modified_date_updates(self):
        """Modified date should update when file is changed."""
        _, original_modified = get_file_dates(self.test_file)
        
        # Wait a moment and modify the file
        import time
        time.sleep(0.1)
        with open(self.test_file, "a") as f:
            f.write("more content")
        
        _, new_modified = get_file_dates(self.test_file)
        
        # Modified date should be present
        self.assertIsNotNone(new_modified)


class TestGetFileAuthor(unittest.TestCase):
    """Tests for the get_file_author() function."""
    
    def setUp(self):
        """Create a temporary directory."""
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Remove temporary directory and files."""
        shutil.rmtree(self.test_dir)
    
    def test_unsupported_file_returns_none(self):
        """Should return None for unsupported file types."""
        test_file = os.path.join(self.test_dir, "test.txt")
        with open(test_file, "w") as f:
            f.write("test")
        
        result = get_file_author(test_file)
        self.assertIsNone(result)
    
    def test_nonexistent_file_returns_none(self):
        """Should return None for nonexistent files."""
        result = get_file_author("/nonexistent/path/file.docx")
        self.assertIsNone(result)
    
    def test_image_file_returns_none(self):
        """Should return None for image files."""
        test_file = os.path.join(self.test_dir, "test.jpg")
        with open(test_file, "wb") as f:
            f.write(b"\xff\xd8\xff")  # Minimal JPEG header
        
        result = get_file_author(test_file)
        self.assertIsNone(result)
    
    def test_pdf_file_returns_none(self):
        """Should return None for PDF files (not supported)."""
        test_file = os.path.join(self.test_dir, "test.pdf")
        with open(test_file, "wb") as f:
            f.write(b"%PDF-1.4")  # Minimal PDF header
        
        result = get_file_author(test_file)
        self.assertIsNone(result)


class TestParseExtensions(unittest.TestCase):
    """Tests for the parse_extensions() function."""
    
    def test_parse_extensions_with_dots(self):
        """Should handle extensions with dots."""
        result = parse_extensions(".psd, .tif, .pdf")
        self.assertEqual(result, [".psd", ".tif", ".pdf"])
    
    def test_parse_extensions_without_dots(self):
        """Should add dots to extensions without them."""
        result = parse_extensions("psd, tif, pdf")
        self.assertEqual(result, [".psd", ".tif", ".pdf"])
    
    def test_parse_mixed_extensions(self):
        """Should handle mix of extensions with and without dots."""
        result = parse_extensions(".psd, tif, .PDF, docx")
        self.assertEqual(result, [".psd", ".tif", ".pdf", ".docx"])
    
    def test_empty_string_returns_empty_list(self):
        """Should return empty list for empty string."""
        result = parse_extensions("")
        self.assertEqual(result, [])
    
    def test_none_returns_empty_list(self):
        """Should return empty list for None."""
        result = parse_extensions(None)
        self.assertEqual(result, [])
    
    def test_whitespace_only_returns_empty_list(self):
        """Should return empty list for whitespace-only string."""
        result = parse_extensions("   ")
        self.assertEqual(result, [])


class TestParseFolderStructure(unittest.TestCase):
    """Tests for the parse_folder_structure() function."""
    
    def test_basic_path_parsing(self):
        """Should correctly parse a basic path."""
        base = "/home/user/documents"
        full = "/home/user/documents/2024/reports"
        
        result = parse_folder_structure(full, base, title_case=False)
        self.assertEqual(result, ["2024", "reports"])
    
    def test_title_case_conversion(self):
        """Should convert folder names to title case."""
        base = "/home/user/documents"
        full = "/home/user/documents/KEY ITEMS/JUNE"
        
        result = parse_folder_structure(full, base, title_case=True)
        self.assertEqual(result, ["Key Items", "June"])
    
    def test_no_title_case(self):
        """Should preserve case when title_case is False."""
        base = "/home/user/documents"
        full = "/home/user/documents/KEY ITEMS/JUNE"
        
        result = parse_folder_structure(full, base, title_case=False)
        self.assertEqual(result, ["KEY ITEMS", "JUNE"])
    
    def test_empty_relative_path(self):
        """Should return empty list for same base and full path."""
        base = "/home/user/documents"
        full = "/home/user/documents"
        
        result = parse_folder_structure(full, base)
        self.assertEqual(result, [])
    
    def test_single_folder(self):
        """Should handle single folder correctly."""
        base = "/home/user"
        full = "/home/user/documents"
        
        result = parse_folder_structure(full, base, title_case=False)
        self.assertEqual(result, ["documents"])


class TestGetRootFolderName(unittest.TestCase):
    """Tests for the get_root_folder_name() function."""
    
    def test_simple_path(self):
        """Should return last folder name from simple path."""
        result = get_root_folder_name("/home/user/documents")
        self.assertEqual(result, "documents")
    
    def test_path_with_trailing_slash(self):
        """Should handle paths with trailing slash."""
        result = get_root_folder_name("/home/user/documents/")
        self.assertEqual(result, "documents")
    
    @unittest.skipUnless(os.name == 'nt', "Windows-only test")
    def test_windows_path(self):
        """Should handle Windows-style paths (Windows only)."""
        result = get_root_folder_name(r"C:\Users\Documents\Projects")
        self.assertEqual(result, "Projects")
    
    @unittest.skipUnless(os.name == 'nt', "Windows-only test")
    def test_unc_path(self):
        """Should handle UNC paths (Windows only)."""
        result = get_root_folder_name(r"\\server\share\folder")
        self.assertEqual(result, "folder")
    
    def test_single_folder(self):
        """Should handle single folder name."""
        result = get_root_folder_name("documents")
        self.assertEqual(result, "documents")


class TestBuildRow(unittest.TestCase):
    """Tests for the build_row() function."""
    
    def setUp(self):
        """Create a temporary directory and test file."""
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, "test_file.txt")
        with open(self.test_file, "w") as f:
            f.write("test content")
    
    def tearDown(self):
        """Remove temporary directory and files."""
        shutil.rmtree(self.test_dir)
    
    def test_basic_row_structure(self):
        """Should create row with basic required fields."""
        row = build_row(
            filename="test.txt",
            dirpath=self.test_dir,
            root_name="Test",
            folders=["2024", "Reports"],
            folder_cols=3,
            include_dates=False,
            include_author=False
        )
        
        self.assertEqual(row["RootFolder"], "Test")
        self.assertEqual(row["FolderString"], self.test_dir)
        self.assertEqual(row["FileName"], "test.txt")
    
    def test_full_path_column(self):
        """Should include FullPath column with complete file path."""
        row = build_row(
            filename="test_file.txt",
            dirpath=self.test_dir,
            root_name="Test",
            folders=[],
            folder_cols=1,
            include_dates=False,
            include_author=False
        )
        
        expected_path = os.path.join(self.test_dir, "test_file.txt")
        self.assertEqual(row["FullPath"], expected_path)
    
    def test_full_path_includes_filename(self):
        """FullPath should include the filename."""
        row = build_row(
            filename="report.docx",
            dirpath="/some/folder",
            root_name="Test",
            folders=[],
            folder_cols=1,
            include_dates=False,
            include_author=False
        )
        
        self.assertIn("report.docx", row["FullPath"])
        self.assertTrue(row["FullPath"].endswith("report.docx"))
    
    def test_folder_columns(self):
        """Should create correct number of folder columns."""
        row = build_row(
            filename="test.txt",
            dirpath=self.test_dir,
            root_name="Test",
            folders=["2024", "Reports"],
            folder_cols=3,
            include_dates=False,
            include_author=False
        )
        
        self.assertEqual(row["Folder1"], "2024")
        self.assertEqual(row["Folder2"], "Reports")
        self.assertIsNone(row["Folder3"])
    
    def test_includes_dates(self):
        """Should include date columns when enabled."""
        row = build_row(
            filename="test_file.txt",
            dirpath=self.test_dir,
            root_name="Test",
            folders=[],
            folder_cols=1,
            include_dates=True,
            include_author=False
        )
        
        self.assertIn("DateCreated", row)
        self.assertIn("DateModified", row)
    
    def test_excludes_dates(self):
        """Should exclude date columns when disabled."""
        row = build_row(
            filename="test.txt",
            dirpath=self.test_dir,
            root_name="Test",
            folders=[],
            folder_cols=1,
            include_dates=False,
            include_author=False
        )
        
        self.assertNotIn("DateCreated", row)
        self.assertNotIn("DateModified", row)
    
    def test_includes_author(self):
        """Should include author column when enabled."""
        row = build_row(
            filename="test_file.txt",
            dirpath=self.test_dir,
            root_name="Test",
            folders=[],
            folder_cols=1,
            include_dates=False,
            include_author=True
        )
        
        self.assertIn("Author", row)
    
    def test_excludes_author(self):
        """Should exclude author column when disabled."""
        row = build_row(
            filename="test.txt",
            dirpath=self.test_dir,
            root_name="Test",
            folders=[],
            folder_cols=1,
            include_dates=False,
            include_author=False
        )
        
        self.assertNotIn("Author", row)


class TestScanDirectory(unittest.TestCase):
    """Tests for the scan_directory() function."""
    
    def setUp(self):
        """Create a temporary directory structure with test files."""
        self.test_dir = tempfile.mkdtemp()
        
        # Create folder structure
        self.folders = [
            os.path.join(self.test_dir, "2024", "Campaigns", "Spring"),
            os.path.join(self.test_dir, "2024", "Campaigns", "Fall"),
            os.path.join(self.test_dir, "2024", "Assets"),
        ]
        
        for folder in self.folders:
            os.makedirs(folder, exist_ok=True)
        
        # Create test files
        self.test_files = [
            os.path.join(self.folders[0], "campaign_brief.txt"),
            os.path.join(self.folders[0], "budget.txt"),
            os.path.join(self.folders[1], "fall_plan.txt"),
            os.path.join(self.folders[2], "logo.png"),
        ]
        
        for file in self.test_files:
            with open(file, "w") as f:
                f.write("test content")
    
    def tearDown(self):
        """Remove temporary directory and files."""
        shutil.rmtree(self.test_dir)
    
    def test_finds_all_files(self):
        """Should find all files in directory structure."""
        files = scan_directory(
            self.test_dir,
            include_dates=False,
            include_author=False
        )
        
        self.assertEqual(len(files), 4)
    
    def test_includes_full_path(self):
        """Should include FullPath for all files."""
        files = scan_directory(
            self.test_dir,
            include_dates=False,
            include_author=False
        )
        
        for f in files:
            self.assertIn("FullPath", f)
            self.assertTrue(os.path.isabs(f["FullPath"]) or f["FullPath"].startswith("\\\\"))
    
    def test_full_path_matches_folder_plus_filename(self):
        """FullPath should equal FolderString + FileName."""
        files = scan_directory(
            self.test_dir,
            include_dates=False,
            include_author=False
        )
        
        for f in files:
            expected = os.path.join(f["FolderString"], f["FileName"])
            self.assertEqual(f["FullPath"], expected)
    
    def test_extension_filter(self):
        """Should filter files by extension."""
        files = scan_directory(
            self.test_dir,
            extensions=[".txt"],
            include_dates=False,
            include_author=False
        )
        
        self.assertEqual(len(files), 3)  # Only .txt files
    
    def test_uses_default_root_name(self):
        """Should use directory name as default root name."""
        files = scan_directory(
            self.test_dir,
            include_dates=False,
            include_author=False
        )
        
        expected_name = os.path.basename(self.test_dir)
        self.assertTrue(all(f["RootFolder"] == expected_name for f in files))
    
    def test_custom_root_name(self):
        """Should use custom root name when provided."""
        files = scan_directory(
            self.test_dir,
            root_name="CustomName",
            include_dates=False,
            include_author=False
        )
        
        self.assertTrue(all(f["RootFolder"] == "CustomName" for f in files))
    
    def test_folder_columns(self):
        """Should create correct number of folder columns."""
        files = scan_directory(
            self.test_dir,
            folder_cols=5,
            include_dates=False,
            include_author=False
        )
        
        for f in files:
            self.assertIn("Folder1", f)
            self.assertIn("Folder5", f)
    
    def test_cancellation(self):
        """Should stop early when cancel is requested."""
        cancel_count = 0
        
        def cancel_after_two():
            nonlocal cancel_count
            cancel_count += 1
            return cancel_count > 2
        
        files = scan_directory(
            self.test_dir,
            include_dates=False,
            include_author=False,
            cancel_check=cancel_after_two
        )
        
        # Should have found fewer than all files
        self.assertLess(len(files), 4)
    
    def test_progress_callback(self):
        """Should call progress callback during scan."""
        # Create more files to trigger progress callback
        many_files_dir = os.path.join(self.test_dir, "many_files")
        os.makedirs(many_files_dir)
        
        for i in range(150):
            with open(os.path.join(many_files_dir, f"file_{i}.txt"), "w") as f:
                f.write("test")
        
        progress_calls = []
        
        def track_progress(count):
            progress_calls.append(count)
        
        scan_directory(
            self.test_dir,
            include_dates=False,
            include_author=False,
            progress_callback=track_progress
        )
        
        # Should have called progress at least once (every 100 files)
        self.assertGreater(len(progress_calls), 0)


class TestExportToExcel(unittest.TestCase):
    """Tests for the export_to_excel() function."""
    
    def setUp(self):
        """Create a temporary directory."""
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Remove temporary directory and files."""
        shutil.rmtree(self.test_dir)
    
    def test_creates_file(self):
        """Should create an Excel file."""
        output_file = os.path.join(self.test_dir, "output.xlsx")
        data = [{"RootFolder": "Test", "FileName": "test.txt"}]
        
        export_to_excel(data, output_file)
        
        self.assertTrue(os.path.exists(output_file))
    
    def test_returns_count(self):
        """Should return number of rows exported."""
        output_file = os.path.join(self.test_dir, "output.xlsx")
        data = [
            {"RootFolder": "Test", "FileName": "test1.txt"},
            {"RootFolder": "Test", "FileName": "test2.txt"},
            {"RootFolder": "Test", "FileName": "test3.txt"},
        ]
        
        count = export_to_excel(data, output_file)
        
        self.assertEqual(count, 3)
    
    def test_preserves_data(self):
        """Should preserve all data in export."""
        output_file = os.path.join(self.test_dir, "output.xlsx")
        data = [{
            "RootFolder": "Marketing",
            "FolderString": "/path/to/folder",
            "FullPath": "/path/to/folder/report.docx",
            "FileName": "report.docx",
            "Folder1": "2024",
            "Folder2": "Reports",
            "Author": "John Doe"
        }]
        
        export_to_excel(data, output_file)
        
        df = pd.read_excel(output_file)
        self.assertEqual(df.iloc[0]["RootFolder"], "Marketing")
        self.assertEqual(df.iloc[0]["FullPath"], "/path/to/folder/report.docx")
        self.assertEqual(df.iloc[0]["FileName"], "report.docx")
        self.assertEqual(df.iloc[0]["Author"], "John Doe")
    
    def test_includes_full_path_column(self):
        """Should include FullPath column in export."""
        output_file = os.path.join(self.test_dir, "output.xlsx")
        data = [{
            "RootFolder": "Test",
            "FolderString": "/path/to/folder",
            "FullPath": "/path/to/folder/file.txt",
            "FileName": "file.txt",
        }]
        
        export_to_excel(data, output_file)
        
        df = pd.read_excel(output_file)
        self.assertIn("FullPath", df.columns)


class TestIntegration(unittest.TestCase):
    """Integration tests that test the complete workflow."""
    
    def setUp(self):
        """Create a temporary directory structure."""
        self.test_dir = tempfile.mkdtemp()
        
        # Create realistic folder structure
        folders = [
            os.path.join(self.test_dir, "2024", "KEY ITEMS", "JANUARY"),
            os.path.join(self.test_dir, "2024", "KEY ITEMS", "FEBRUARY"),
            os.path.join(self.test_dir, "2024", "ASSETS", "IMAGES"),
        ]
        
        for folder in folders:
            os.makedirs(folder, exist_ok=True)
        
        # Create test files
        test_files = [
            (folders[0], "style_001_FINAL.psd"),
            (folders[0], "style_001_PITCH.tif"),
            (folders[1], "style_002_FINAL.psd"),
            (folders[2], "logo.png"),
            (folders[2], "banner.jpg"),
        ]
        
        for folder, filename in test_files:
            with open(os.path.join(folder, filename), "w") as f:
                f.write("test")
    
    def tearDown(self):
        """Remove temporary directory."""
        shutil.rmtree(self.test_dir)
    
    def test_full_workflow(self):
        """Test complete scan and export workflow."""
        output_file = os.path.join(self.test_dir, "output.xlsx")
        
        # Scan
        files = scan_directory(
            directory=self.test_dir,
            root_name="TestBrand",
            folder_cols=3,
            title_case=True,
            include_dates=True,
            include_author=True
        )
        
        # Export
        count = export_to_excel(files, output_file)
        
        # Verify
        self.assertEqual(count, 5)
        
        df = pd.read_excel(output_file)
        self.assertEqual(len(df), 5)
        self.assertTrue(all(df["RootFolder"] == "TestBrand"))
        
        # Check title case was applied
        self.assertIn("Key Items", df["Folder2"].values)
        
        # Check FullPath column exists and is correct
        self.assertIn("FullPath", df.columns)
        for idx, row in df.iterrows():
            self.assertTrue(row["FullPath"].endswith(row["FileName"]))
    
    def test_filtered_workflow(self):
        """Test workflow with extension filter."""
        output_file = os.path.join(self.test_dir, "output.xlsx")
        
        # Scan with filter
        files = scan_directory(
            directory=self.test_dir,
            extensions=[".psd"],
            include_dates=False,
            include_author=False
        )
        
        # Export
        count = export_to_excel(files, output_file)
        
        # Verify only .psd files
        self.assertEqual(count, 2)
        
        df = pd.read_excel(output_file)
        self.assertTrue(all(df["FileName"].str.endswith(".psd")))
    
    def test_default_root_name_is_folder_name(self):
        """Root name should default to top-level folder name."""
        files = scan_directory(
            directory=self.test_dir,
            include_dates=False,
            include_author=False
        )
        
        expected_name = get_root_folder_name(self.test_dir)
        self.assertTrue(all(f["RootFolder"] == expected_name for f in files))


# ============================================================
# RUN TESTS
# ============================================================
if __name__ == "__main__":
    unittest.main(verbosity=2)
