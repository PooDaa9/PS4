#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import hashlib
from datetime import datetime

def get_file_hash(filepath):
    """حساب SHA-256 هاش للملف"""
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except FileNotFoundError:
        return None

def generate_cache_manifest():
    """توليد ملف cache.appcache مع الهاش"""
    
    # الملفات المطلوبة
    files = [
        'index.html',
        'run_lapse.html',
        'PS4_13.00_Webkit.html',
        'chain_lapse.js',
        'chain_poops.js',
        'sysctl.html',
        'sysctl.js',
        'core.js',
        'mem.js',
        'int64.js',
        'ps4_offsets.js',
        'rpc_worker.js',
        'payload.bin',
        'patches/1100.bin',
        'patches/1150.bin',
        'patches/1200.bin',
        'patches/1300.bin'
    ]
    
    content = "CACHE MANIFEST\n"
    content += f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    for f in files:
        hash_val = get_file_hash(f)
        if hash_val:
            content += f"/{f} #{hash_val}\n"
        else:
            content += f"/{f} #FILE_NOT_FOUND\n"
    
    content += "\nNETWORK:\n*\n"
    content += "\nFALLBACK:\n"
    content += "/index.html /index.html\n"
    content += "/run_lapse.html /run_lapse.html\n"
    content += "/PS4_13.00_Webkit.html /PS4_13.00_Webkit.html\n"
    
    with open('cache.appcache', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ تم إنشاء cache.appcache مع الهاش")

if __name__ == "__main__":
    generate_cache_manifest()