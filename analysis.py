#!/usr/bin/env python3
"""
Analysis script for the hypoxic spheroid simulation.
Generates plots of cell counts over time and viable rim thickness.
"""

import re
import glob
import os
import subprocess

import numpy as np
import matplotlib.pyplot as plt


def parse_snapshots(output_dir="output"):
    """Parse all SVG snapshots to extract cell statistics."""
    snapshots = sorted(glob.glob(os.path.join(output_dir, "snapshot*.svg")))
    data = []
    for snap in snapshots:
        with open(snap) as f:
            content = f.read()

        # Extract simulated time in minutes from the SVG text
        # e.g. "Current time: 2 days, 3 hours, and 15.00 minutes"
        time_match = re.search(
            r'Current time:\s*(?:(\d+) days?,?\s*)?(?:(\d+) hours?,?\s*)?(?:and\s*)?([\d.]+)\s*minutes?',
            content
        )
        minutes = 0.0
        if time_match:
            days = int(time_match.group(1)) if time_match.group(1) else 0
            hours = int(time_match.group(2)) if time_match.group(2) else 0
            mins = float(time_match.group(3))
            minutes = days * 1440 + hours * 60 + mins

        agents_match = re.search(r'(\d+) agents', content)
        total = int(agents_match.group(1)) if agents_match else 0

        necrotic = len(re.findall(r'rgb\(250,138,38\)', content))
        apoptotic = len(re.findall(r'rgb\(255,0,0\)', content))
        dead = len(re.findall(r'dead="true"', content))
        live = total - dead

        # Compute mean radii for necrotic and live cells
        nec_radii = []
        live_radii = []
        cell_groups = re.findall(r'<g id="cell\d+"[^>]*>(.*?)</g>', content, re.DOTALL)
        for group in cell_groups:
            circle = re.search(r'<circle cx="([^"]+)" cy="([^"]+)"', group)
            if not circle:
                continue
            cx = float(circle.group(1))
            cy = float(circle.group(2))
            ox = cx - 1000.0
            oy = cy - 1140.0
            r = np.hypot(ox, oy)
            if 'rgb(250,138,38)' in group or 'rgb(255,0,0)' in group:
                nec_radii.append(r)
            else:
                live_radii.append(r)

        mean_nec_radius = np.mean(nec_radii) if nec_radii else np.nan
        mean_live_radius = np.mean(live_radii) if live_radii else np.nan
        max_nec_radius = np.max(nec_radii) if nec_radii else np.nan

        data.append({
            'file': os.path.basename(snap),
            'time_min': minutes,
            'total': total,
            'live': live,
            'necrotic': necrotic,
            'apoptotic': apoptotic,
            'dead': dead,
            'mean_nec_radius': mean_nec_radius,
            'mean_live_radius': mean_live_radius,
            'max_nec_radius': max_nec_radius,
        })
    return data


def plot_counts(data, output_path="output/cell_counts.png"):
    """Plot cell counts vs time."""
    times = np.array([d['time_min'] for d in data]) / 60.0  # hours
    live = np.array([d['live'] for d in data])
    necrotic = np.array([d['necrotic'] for d in data])
    apoptotic = np.array([d['apoptotic'] for d in data])

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(times, live, label='Live', color='green', linewidth=2)
    ax.plot(times, necrotic, label='Necrotic', color='brown', linewidth=2)
    ax.plot(times, apoptotic, label='Apoptotic', color='red', linewidth=2)
    ax.set_xlabel('Time (hours)', fontsize=12)
    ax.set_ylabel('Cell count', fontsize=12)
    ax.set_title('Hypoxic Spheroid: Cell Populations', fontsize=14)
    ax.legend()
    ax.set_xlim(0, times[-1])
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    print(f"Saved: {output_path}")


def plot_rim_thickness(data, output_path="output/rim_thickness.png"):
    """Plot viable rim thickness over time."""
    times = np.array([d['time_min'] for d in data]) / 60.0
    max_nec = np.array([d['max_nec_radius'] for d in data])
    # Approximate spheroid radius from max cell distance
    spheroid_r = np.array([d['mean_live_radius'] + 30 for d in data])  # rough
    # Better: use the 95th percentile of live cell radii
    # For simplicity, use mean_live_radius + 1 std as proxy
    rim = np.array([d['mean_live_radius'] - d['mean_nec_radius'] for d in data])
    rim = np.maximum(rim, 0)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(times, rim, color='darkgreen', linewidth=2)
    ax.set_xlabel('Time (hours)', fontsize=12)
    ax.set_ylabel('Viable rim thickness (μm)', fontsize=12)
    ax.set_title('Viable Rim Thickness vs Time', fontsize=14)
    ax.set_xlim(0, times[-1])
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    print(f"Saved: {output_path}")


def make_movie(output_dir="output", framerate=12):
    """Create an MP4 animation from SVG snapshots using ffmpeg."""
    svg_files = sorted(glob.glob(os.path.join(output_dir, "snapshot*.svg")))
    if not svg_files:
        print("No SVG snapshots found.")
        return

    if subprocess.run(["which", "ffmpeg"], capture_output=True).returncode != 0:
        print("ffmpeg not found. Skipping movie generation.")
        return

    # Use rsvg-convert (from librsvg) — handles fonts correctly on macOS
    if subprocess.run(["which", "rsvg-convert"], capture_output=True).returncode != 0:
        print("rsvg-convert not found. Skipping movie generation.")
        print("Install it with: brew install librsvg")
        return

    print(f"Converting {len(svg_files)} SVG files to PNG...")
    for i, svg in enumerate(svg_files):
        png = os.path.join(output_dir, f"frame_{i:04d}.png")
        subprocess.run(
            ["rsvg-convert", "-w", "1200", "-h", "1200", "-o", png, svg],
            check=True, capture_output=True
        )

    movie_path = os.path.join(output_dir, "spheroid.mp4")
    frame_pattern = os.path.join(output_dir, "frame_%04d.png")
    cmd = [
        "ffmpeg", "-y", "-r", str(framerate),
        "-i", frame_pattern,
        "-vcodec", "libx264", "-pix_fmt", "yuv420p",
        "-crf", "18", movie_path
    ]
    print(f"Creating movie: {movie_path}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Saved: {movie_path}")
    else:
        print("ffmpeg failed:", result.stderr)

    # Clean up frame PNGs
    for f in glob.glob(os.path.join(output_dir, "frame_*.png")):
        os.remove(f)


def main():
    print("Parsing snapshots...")
    data = parse_snapshots()
    if not data:
        print("No data found.")
        return

    print(f"Parsed {len(data)} snapshots.")
    print(f"Final time: {data[-1]['time_min'] / 60:.1f} h")
    print(f"Final counts: live={data[-1]['live']}, necrotic={data[-1]['necrotic']}, apoptotic={data[-1]['apoptotic']}")

    print("\nGenerating plots...")
    plot_counts(data)
    plot_rim_thickness(data)

    print("\nGenerating movie...")
    make_movie()

    print("\nDone!")


if __name__ == "__main__":
    main()
