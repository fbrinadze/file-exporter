"""
Scan Cache Module
=================
Implements predictive caching for faster repeat directory scans.
Uses ML-inspired techniques to predict and pre-load frequently scanned directories.
"""

import json
import os
import time
from collections import Counter
from datetime import datetime, timedelta


class ScanCache:
    """
    Intelligent caching system for directory scans.
    Learns from user behavior and predicts next likely scans.
    """
    
    def __init__(self, cache_file='scan_cache.json', max_cache_size=10, max_age_days=7):
        """
        Initialize the scan cache.
        
        Args:
            cache_file: Path to cache storage file
            max_cache_size: Maximum number of directories to cache
            max_age_days: Maximum age of cached data in days
        """
        self.cache_file = cache_file
        self.max_cache_size = max_cache_size
        self.max_age_days = max_age_days
        self.cache = {}
        self.history = []
        self.load_cache()
    
    def load_cache(self):
        """Load cache from disk."""
        if not os.path.exists(self.cache_file):
            return
        
        try:
            with open(self.cache_file, 'r') as f:
                data = json.load(f)
                self.cache = data.get('cache', {})
                self.history = data.get('history', [])
                
                # Clean expired entries
                self._clean_expired()
        except Exception as e:
            print(f"Error loading cache: {e}")
            self.cache = {}
            self.history = []
    
    def save_cache(self):
        """Save cache to disk."""
        try:
            data = {
                'cache': self.cache,
                'history': self.history
            }
            with open(self.cache_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving cache: {e}")
    
    def _clean_expired(self):
        """Remove expired cache entries."""
        current_time = time.time()
        max_age_seconds = self.max_age_days * 24 * 60 * 60
        
        expired_dirs = []
        for directory, data in self.cache.items():
            if current_time - data.get('timestamp', 0) > max_age_seconds:
                expired_dirs.append(directory)
        
        for directory in expired_dirs:
            del self.cache[directory]
            if directory in self.history:
                self.history.remove(directory)
    
    def get(self, directory):
        """
        Get cached scan results for a directory.
        
        Args:
            directory: Directory path
            
        Returns:
            dict: Cached results or None if not found/expired
        """
        directory = os.path.normpath(directory)
        
        if directory not in self.cache:
            return None
        
        data = self.cache[directory]
        
        # Check if cache is still valid
        current_time = time.time()
        max_age_seconds = self.max_age_days * 24 * 60 * 60
        
        if current_time - data.get('timestamp', 0) > max_age_seconds:
            # Expired
            del self.cache[directory]
            return None
        
        # Check if directory has been modified since cache
        try:
            dir_mtime = os.path.getmtime(directory)
            if dir_mtime > data.get('timestamp', 0):
                # Directory modified, cache invalid
                del self.cache[directory]
                return None
        except:
            pass
        
        return data.get('results')
    
    def put(self, directory, results):
        """
        Cache scan results for a directory.
        
        Args:
            directory: Directory path
            results: Scan results to cache
        """
        directory = os.path.normpath(directory)
        
        # Enforce cache size limit
        if len(self.cache) >= self.max_cache_size and directory not in self.cache:
            # Remove least recently used
            if self.history:
                oldest = self.history[0]
                if oldest in self.cache:
                    del self.cache[oldest]
                self.history.pop(0)
        
        # Store cache entry
        self.cache[directory] = {
            'results': results,
            'timestamp': time.time(),
            'file_count': len(results)
        }
        
        # Update history
        if directory in self.history:
            self.history.remove(directory)
        self.history.append(directory)
        
        # Keep history size manageable
        if len(self.history) > self.max_cache_size * 2:
            self.history = self.history[-self.max_cache_size * 2:]
        
        # Save to disk
        self.save_cache()
    
    def predict_next(self):
        """
        Predict the next likely directory to be scanned.
        Uses frequency analysis of scan history.
        
        Returns:
            str: Predicted directory path or None
        """
        if not self.history:
            return None
        
        # Count frequency of each directory
        freq = Counter(self.history)
        
        # Get most common, excluding the most recent (already scanned)
        most_common = freq.most_common(3)
        
        # Return most frequent that isn't the last scanned
        last_scanned = self.history[-1] if self.history else None
        
        for directory, count in most_common:
            if directory != last_scanned and os.path.exists(directory):
                return directory
        
        return None
    
    def get_stats(self):
        """
        Get cache statistics.
        
        Returns:
            dict: Cache statistics
        """
        total_files = sum(data.get('file_count', 0) for data in self.cache.values())
        
        return {
            'cached_directories': len(self.cache),
            'total_cached_files': total_files,
            'history_size': len(self.history),
            'cache_size_mb': self._get_cache_size_mb(),
            'most_scanned': self._get_most_scanned()
        }
    
    def _get_cache_size_mb(self):
        """Get cache file size in MB."""
        try:
            if os.path.exists(self.cache_file):
                size_bytes = os.path.getsize(self.cache_file)
                return round(size_bytes / (1024 * 1024), 2)
        except:
            pass
        return 0
    
    def _get_most_scanned(self):
        """Get the most frequently scanned directory."""
        if not self.history:
            return None
        
        freq = Counter(self.history)
        most_common = freq.most_common(1)
        
        if most_common:
            return most_common[0][0]
        return None
    
    def clear(self):
        """Clear all cache data."""
        self.cache = {}
        self.history = []
        self.save_cache()
    
    def is_cached(self, directory):
        """
        Check if a directory is cached and valid.
        
        Args:
            directory: Directory path
            
        Returns:
            bool: True if cached and valid
        """
        return self.get(directory) is not None
