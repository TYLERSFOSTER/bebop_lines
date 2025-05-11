"""
Utility for generating filenames
"""
from __future__ import annotations

import os
from datetime import datetime


def get_timestamped_filename(prefix="plot", ext="png", outdir="outputs/figs"):
    """
    Return a string, to be used as a filename, that includes a timestamp

    Args:
      prefix : Prefix for the filename
      ext : Extension for the filename
      outdir : Output irectory to save the file in
    
    Returns
      The filename as a string
    """
    os.makedirs(outdir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    filename = os.path.join(outdir, f"{prefix}_{timestamp}.{ext}")

    return filename