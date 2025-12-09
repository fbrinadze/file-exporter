"""
Duplicate File Detector
=======================
Detects duplicate files using content hashing.
Finds duplicates even with different names or locations.
"""

import hashlib
import os
from collections import defaultdict


class DuplicateDetector:
    """
    Detects duplicate files using MD5 hashing.
    Groups files by content, not just name.
    """
    
    def __init__(self, chunk_size=8192):
        """
        Initialize the duplicate detector.
        
        Args:
            chunk_size: Size of chunks to read for hashing (bytes)
        """
        self.chunk_size = chunk_size
        self.file_hashes = defaultdict(list)
        self.duplicates = []
    
    def calculate_hash(self, filepath):
        """
        Calculate MD5 hash of a file.
        
        Args:
            filepath: Path to the file
            
        Returns:
            str: MD5 hash or None if error
        """
        try:
            hasher = hashlib.md5()
            
            with open(filepath, 'rb') as f:
                while True:
                    chunk = f.read(self.chunk_size)
                    if not chunk:
                        break
                    hasher.update(chunk)
            
            return hasher.hexdigest()
        except (IOError, OSError, PermissionError) as e:
            print(f"Error hashing {filepath}: {e}")
            return None
    
    def calculate_quick_hash(self, filepath, sample_size=1024):
        """
        Calculate quick hash using first and last bytes.
        Faster for large files, good for initial filtering.
        
        Args:
            filepath: Path to the file
            sample_size: Number of bytes to sample from start/end
            
        Returns:
            str: Quick hash or None if error
        """
        try:
            file_size = os.path.getsize(filepath)
            
            if file_size == 0:
                return "empty_file"
            
            hasher = hashlib.md5()
            
            with open(filepath, 'rb') as f:
                # Hash first bytes
                first_chunk = f.read(min(sample_size, file_size))
                hasher.update(first_chunk)
                
                # Hash last bytes if file is large enough
                if file_size > sample_size * 2:
                    f.seek(-sample_size, 2)  # Seek to end
                    last_chunk = f.read(sample_size)
                    hasher.update(last_chunk)
                
                # Include file size in hash
                hasher.update(str(file_size).encode())
            
            return hasher.hexdigest()
        except (IOError, OSError, PermissionError) as e:
            print(f"Error quick hashing {filepath}: {e}")
            return None
    
    def find_duplicates(self, files, use_quick_hash=True, progress_callback=None):
        """
        Find duplicate files in a list.
        
        Args:
            files: List of file dictionaries with 'FullPath' key
            use_quick_hash: Use quick hash for initial filtering
            progress_callback: Function to call with progress updates
            
        Returns:
            list: List of duplicate groups
        """
        self.file_hashes.clear()
        self.duplicates = []
        
        # Step 1: Group by file size (quick filter)
        size_groups = defaultdict(list)
        
        for file_info in files:
            filepath = file_info.get('FullPath')
            if not filepath or not os.path.exists(filepath):
                continue
            
            try:
                file_size = os.path.getsize(filepath)
                size_groups[file_size].append(file_info)
            except:
                continue
        
        # Step 2: Hash files with same size
        total_files = sum(len(group) for group in size_groups.values() if len(group) > 1)
        processed = 0
        
        for size, group in size_groups.items():
            if len(group) < 2:
                continue  # Skip unique sizes
            
            # Use quick hash first if enabled
            if use_quick_hash:
                quick_hash_groups = defaultdict(list)
                
                for file_info in group:
                    filepath = file_info.get('FullPath')
                    quick_hash = self.calculate_quick_hash(filepath)
                    
                    if quick_hash:
                        quick_hash_groups[quick_hash].append(file_info)
                    
                    processed += 1
                    if progress_callback and processed % 10 == 0:
                        progress_callback(processed, total_files)
                
                # Full hash only for files with matching quick hash
                for quick_hash, quick_group in quick_hash_groups.items():
                    if len(quick_group) < 2:
                        continue
                    
                    for file_info in quick_group:
                        filepath = file_info.get('FullPath')
                        full_hash = self.calculate_hash(filepath)
                        
                        if full_hash:
                            self.file_hashes[full_hash].append(file_info)
            else:
                # Full hash for all files with same size
                for file_info in group:
                    filepath = file_info.get('FullPath')
                    file_hash = self.calculate_hash(filepath)
                    
                    if file_hash:
                        self.file_hashes[file_hash].append(file_info)
                    
                    processed += 1
                    if progress_callback and processed % 10 == 0:
                        progress_callback(processed, total_files)
        
        # Step 3: Identify duplicates
        for file_hash, file_list in self.file_hashes.items():
            if len(file_list) > 1:
                self.duplicates.append({
                    'hash': file_hash,
                    'count': len(file_list),
                    'files': file_list,
                    'total_size': sum(os.path.getsize(f['FullPath']) for f in file_list if os.path.exists(f['FullPath']))
                })
        
        # Sort by count (most duplicates first)
        self.duplicates.sort(key=lambda x: x['count'], reverse=True)
        
        return self.duplicates
    
    def get_duplicate_stats(self):
        """
        Get statistics about duplicates.
        
        Returns:
            dict: Statistics dictionary
        """
        if not self.duplicates:
            return {
                'duplicate_groups': 0,
                'duplicate_files': 0,
                'wasted_space': 0,
                'largest_group': 0
            }
        
        total_duplicate_files = sum(group['count'] - 1 for group in self.duplicates)
        wasted_space = sum(
            (group['count'] - 1) * (group['total_size'] / group['count'])
            for group in self.duplicates
        )
        largest_group = max(group['count'] for group in self.duplicates)
        
        return {
            'duplicate_groups': len(self.duplicates),
            'duplicate_files': total_duplicate_files,
            'wasted_space': int(wasted_space),
            'largest_group': largest_group
        }
    
    def format_size(self, size_bytes):
        """
        Format bytes to human-readable size.
        
        Args:
            size_bytes: Size in bytes
            
        Returns:
            str: Formatted size string
        """
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"
    
    def export_duplicate_report(self, output_file):
        """
        Export duplicate report to text file.
        
        Args:
            output_file: Path to output file
            
        Returns:
            bool: True if successful
        """
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("DUPLICATE FILE REPORT\n")
                f.write("=" * 80 + "\n\n")
                
                stats = self.get_duplicate_stats()
                f.write(f"Duplicate Groups: {stats['duplicate_groups']}\n")
                f.write(f"Duplicate Files: {stats['duplicate_files']}\n")
                f.write(f"Wasted Space: {self.format_size(stats['wasted_space'])}\n")
                f.write(f"Largest Group: {stats['largest_group']} files\n\n")
                
                f.write("=" * 80 + "\n\n")
                
                for i, group in enumerate(self.duplicates, 1):
                    f.write(f"Group {i}: {group['count']} duplicates\n")
                    f.write(f"Hash: {group['hash']}\n")
                    f.write(f"Total Size: {self.format_size(group['total_size'])}\n")
                    f.write(f"Wasted Space: {self.format_size(group['total_size'] - (group['total_size'] / group['count']))}\n\n")
                    
                    for file_info in group['files']:
                        f.write(f"  - {file_info['FullPath']}\n")
                    
                    f.write("\n" + "-" * 80 + "\n\n")
            
            return True
        except Exception as e:
            print(f"Error exporting report: {e}")
            return False
