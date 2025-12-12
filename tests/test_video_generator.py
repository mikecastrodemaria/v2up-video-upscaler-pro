"""
Test Video Generator
Create test videos with various patterns for testing upscaling and interpolation
"""

import cv2
import numpy as np
import os
from pathlib import Path
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class TestVideoGenerator:
    """Generate test videos for upscaling and interpolation testing"""

    def __init__(self, output_dir: str = "test_videos"):
        """
        Initialize test video generator

        Args:
            output_dir: Directory to save test videos
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True, parents=True)

    def generate_moving_shapes(
        self,
        filename: str = "moving_shapes.mp4",
        resolution: Tuple[int, int] = (640, 480),
        fps: float = 30.0,
        duration: float = 5.0,
        codec: str = 'mp4v'
    ) -> str:
        """
        Generate video with moving shapes

        Args:
            filename: Output filename
            resolution: Video resolution (width, height)
            fps: Frames per second
            duration: Duration in seconds
            codec: Video codec

        Returns:
            str: Path to generated video
        """
        output_path = str(self.output_dir / filename)
        width, height = resolution
        total_frames = int(fps * duration)

        logger.info(f"Generating moving shapes video: {output_path}")
        logger.info(f"Resolution: {width}x{height}, FPS: {fps}, Duration: {duration}s")

        # Initialize video writer
        fourcc = cv2.VideoWriter_fourcc(*codec)
        writer = cv2.VideoWriter(output_path, fourcc, fps, resolution)

        for frame_num in range(total_frames):
            # Create frame
            frame = np.ones((height, width, 3), dtype=np.uint8) * 50  # Dark gray background

            # Calculate positions (circular motion)
            t = frame_num / fps
            angle = 2 * np.pi * t / duration

            # Moving circle (red)
            circle_x = int(width / 2 + width / 4 * np.cos(angle))
            circle_y = int(height / 2 + height / 4 * np.sin(angle))
            cv2.circle(frame, (circle_x, circle_y), 30, (0, 0, 255), -1)

            # Moving square (green)
            square_x = int(width / 2 + width / 4 * np.cos(angle + np.pi))
            square_y = int(height / 2 + height / 4 * np.sin(angle + np.pi))
            cv2.rectangle(frame, (square_x - 25, square_y - 25),
                         (square_x + 25, square_y + 25), (0, 255, 0), -1)

            # Moving triangle (blue)
            tri_x = int(width / 2 + width / 4 * np.cos(angle + np.pi / 2))
            tri_y = int(height / 2 + height / 4 * np.sin(angle + np.pi / 2))
            pts = np.array([[tri_x, tri_y - 30],
                           [tri_x - 25, tri_y + 20],
                           [tri_x + 25, tri_y + 20]], np.int32)
            cv2.fillPoly(frame, [pts], (255, 0, 0))

            # Add frame counter
            cv2.putText(frame, f"Frame: {frame_num}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            writer.write(frame)

        writer.release()
        logger.info(f"Generated: {output_path}")
        return output_path

    def generate_text_scroller(
        self,
        filename: str = "text_scroll.mp4",
        resolution: Tuple[int, int] = (640, 480),
        fps: float = 30.0,
        duration: float = 5.0,
        codec: str = 'mp4v'
    ) -> str:
        """
        Generate video with scrolling text

        Args:
            filename: Output filename
            resolution: Video resolution
            fps: Frames per second
            duration: Duration in seconds
            codec: Video codec

        Returns:
            str: Path to generated video
        """
        output_path = str(self.output_dir / filename)
        width, height = resolution
        total_frames = int(fps * duration)

        logger.info(f"Generating text scroller video: {output_path}")

        fourcc = cv2.VideoWriter_fourcc(*codec)
        writer = cv2.VideoWriter(output_path, fourcc, fps, resolution)

        text = "VIDEO UPSCALER PRO - TESTING"
        text_width = len(text) * 30

        for frame_num in range(total_frames):
            # Create gradient background
            frame = np.zeros((height, width, 3), dtype=np.uint8)
            for i in range(height):
                color = int(100 + 155 * i / height)
                frame[i, :] = [color // 3, color // 2, color]

            # Calculate text position (horizontal scroll)
            x_pos = int(width - (width + text_width) * frame_num / total_frames)
            y_pos = height // 2

            # Draw text
            cv2.putText(frame, text, (x_pos, y_pos),
                       cv2.FONT_HERSHEY_BOLD, 1.5, (255, 255, 255), 3)

            # Draw frame info
            cv2.putText(frame, f"Frame: {frame_num}/{total_frames}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

            writer.write(frame)

        writer.release()
        logger.info(f"Generated: {output_path}")
        return output_path

    def generate_checkerboard_animation(
        self,
        filename: str = "checkerboard.mp4",
        resolution: Tuple[int, int] = (640, 480),
        fps: float = 30.0,
        duration: float = 5.0,
        codec: str = 'mp4v'
    ) -> str:
        """
        Generate checkerboard pattern animation (good for testing upscaling)

        Args:
            filename: Output filename
            resolution: Video resolution
            fps: Frames per second
            duration: Duration in seconds
            codec: Video codec

        Returns:
            str: Path to generated video
        """
        output_path = str(self.output_dir / filename)
        width, height = resolution
        total_frames = int(fps * duration)

        logger.info(f"Generating checkerboard animation: {output_path}")

        fourcc = cv2.VideoWriter_fourcc(*codec)
        writer = cv2.VideoWriter(output_path, fourcc, fps, resolution)

        cell_size_start = 40
        cell_size_end = 10

        for frame_num in range(total_frames):
            # Animate cell size
            t = frame_num / total_frames
            cell_size = int(cell_size_start + (cell_size_end - cell_size_start) * t)

            frame = np.zeros((height, width, 3), dtype=np.uint8)

            # Draw checkerboard
            for i in range(0, height, cell_size):
                for j in range(0, width, cell_size):
                    if ((i // cell_size) + (j // cell_size)) % 2 == 0:
                        frame[i:i+cell_size, j:j+cell_size] = [255, 255, 255]

            # Add border
            cv2.rectangle(frame, (0, 0), (width-1, height-1), (0, 255, 0), 3)

            # Add info
            cv2.putText(frame, f"Cell Size: {cell_size}px", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

            writer.write(frame)

        writer.release()
        logger.info(f"Generated: {output_path}")
        return output_path

    def generate_color_bars(
        self,
        filename: str = "color_bars.mp4",
        resolution: Tuple[int, int] = (640, 480),
        fps: float = 30.0,
        duration: float = 5.0,
        codec: str = 'mp4v'
    ) -> str:
        """
        Generate SMPTE color bars with animation

        Args:
            filename: Output filename
            resolution: Video resolution
            fps: Frames per second
            duration: Duration in seconds
            codec: Video codec

        Returns:
            str: Path to generated video
        """
        output_path = str(self.output_dir / filename)
        width, height = resolution
        total_frames = int(fps * duration)

        logger.info(f"Generating color bars video: {output_path}")

        fourcc = cv2.VideoWriter_fourcc(*codec)
        writer = cv2.VideoWriter(output_path, fourcc, fps, resolution)

        # SMPTE colors (BGR)
        colors = [
            (255, 255, 255),  # White
            (0, 255, 255),    # Yellow
            (255, 255, 0),    # Cyan
            (0, 255, 0),      # Green
            (255, 0, 255),    # Magenta
            (0, 0, 255),      # Red
            (255, 0, 0),      # Blue
        ]

        bar_width = width // len(colors)

        for frame_num in range(total_frames):
            frame = np.zeros((height, width, 3), dtype=np.uint8)

            # Animate brightness
            brightness = 0.5 + 0.5 * np.sin(2 * np.pi * frame_num / fps)

            # Draw color bars
            for i, color in enumerate(colors):
                x1 = i * bar_width
                x2 = (i + 1) * bar_width
                adjusted_color = tuple(int(c * brightness) for c in color)
                frame[:, x1:x2] = adjusted_color

            # Add frame counter
            cv2.putText(frame, f"Frame: {frame_num}", (10, height - 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            writer.write(frame)

        writer.release()
        logger.info(f"Generated: {output_path}")
        return output_path

    def generate_resolution_test(
        self,
        filename: str = "resolution_test.mp4",
        resolution: Tuple[int, int] = (640, 480),
        fps: float = 30.0,
        duration: float = 5.0,
        codec: str = 'mp4v'
    ) -> str:
        """
        Generate resolution test pattern with fine details

        Args:
            filename: Output filename
            resolution: Video resolution
            fps: Frames per second
            duration: Duration in seconds
            codec: Video codec

        Returns:
            str: Path to generated video
        """
        output_path = str(self.output_dir / filename)
        width, height = resolution
        total_frames = int(fps * duration)

        logger.info(f"Generating resolution test pattern: {output_path}")

        fourcc = cv2.VideoWriter_fourcc(*codec)
        writer = cv2.VideoWriter(output_path, fourcc, fps, resolution)

        for frame_num in range(total_frames):
            frame = np.ones((height, width, 3), dtype=np.uint8) * 128

            # Draw concentric circles
            center = (width // 2, height // 2)
            for r in range(10, min(width, height) // 2, 10):
                color = (0, 0, 0) if (r // 10) % 2 == 0 else (255, 255, 255)
                cv2.circle(frame, center, r, color, 2)

            # Draw fine grid
            grid_spacing = 20
            for x in range(0, width, grid_spacing):
                cv2.line(frame, (x, 0), (x, height), (200, 200, 200), 1)
            for y in range(0, height, grid_spacing):
                cv2.line(frame, (0, y), (width, y), (200, 200, 200), 1)

            # Draw text at different sizes
            sizes = [0.3, 0.5, 0.7, 1.0]
            for i, size in enumerate(sizes):
                y_pos = 50 + i * 40
                cv2.putText(frame, f"Size {size}: Fine Detail Test", (10, y_pos),
                           cv2.FONT_HERSHEY_SIMPLEX, size, (0, 0, 255), 1)

            # Add rotating element
            angle = frame_num * 5
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            pts = np.array([[center[0] + 100, center[1]],
                           [center[0], center[1] + 100],
                           [center[0] - 100, center[1]],
                           [center[0], center[1] - 100]], np.float32)
            rotated_pts = cv2.transform(pts.reshape(1, -1, 2), M).reshape(-1, 2).astype(np.int32)
            cv2.polylines(frame, [rotated_pts], True, (255, 0, 0), 2)

            writer.write(frame)

        writer.release()
        logger.info(f"Generated: {output_path}")
        return output_path

    def generate_all_test_videos(
        self,
        resolution: Tuple[int, int] = (640, 480),
        fps: float = 30.0,
        duration: float = 5.0
    ) -> dict:
        """
        Generate all test videos

        Args:
            resolution: Video resolution
            fps: Frames per second
            duration: Duration in seconds

        Returns:
            dict: Dictionary of test video paths
        """
        logger.info("Generating all test videos...")

        videos = {}

        videos['moving_shapes'] = self.generate_moving_shapes(
            resolution=resolution, fps=fps, duration=duration
        )

        videos['text_scroll'] = self.generate_text_scroller(
            resolution=resolution, fps=fps, duration=duration
        )

        videos['checkerboard'] = self.generate_checkerboard_animation(
            resolution=resolution, fps=fps, duration=duration
        )

        videos['color_bars'] = self.generate_color_bars(
            resolution=resolution, fps=fps, duration=duration
        )

        videos['resolution_test'] = self.generate_resolution_test(
            resolution=resolution, fps=fps, duration=duration
        )

        logger.info(f"Generated {len(videos)} test videos in {self.output_dir}")

        return videos


def main():
    """Generate test videos"""
    import argparse

    parser = argparse.ArgumentParser(description="Generate test videos")
    parser.add_argument('--output-dir', default='test_videos', help='Output directory')
    parser.add_argument('--resolution', default='640x480', help='Resolution (WxH)')
    parser.add_argument('--fps', type=float, default=30.0, help='Frames per second')
    parser.add_argument('--duration', type=float, default=5.0, help='Duration in seconds')
    parser.add_argument('--type', choices=['all', 'shapes', 'text', 'checker', 'bars', 'resolution'],
                       default='all', help='Type of video to generate')

    args = parser.parse_args()

    # Parse resolution
    width, height = map(int, args.resolution.split('x'))
    resolution = (width, height)

    # Setup logging
    logging.basicConfig(level=logging.INFO)

    # Create generator
    generator = TestVideoGenerator(args.output_dir)

    # Generate videos
    if args.type == 'all':
        videos = generator.generate_all_test_videos(resolution, args.fps, args.duration)
        print("\nGenerated test videos:")
        for name, path in videos.items():
            print(f"  {name}: {path}")
    elif args.type == 'shapes':
        path = generator.generate_moving_shapes(resolution=resolution, fps=args.fps, duration=args.duration)
        print(f"Generated: {path}")
    elif args.type == 'text':
        path = generator.generate_text_scroller(resolution=resolution, fps=args.fps, duration=args.duration)
        print(f"Generated: {path}")
    elif args.type == 'checker':
        path = generator.generate_checkerboard_animation(resolution=resolution, fps=args.fps, duration=args.duration)
        print(f"Generated: {path}")
    elif args.type == 'bars':
        path = generator.generate_color_bars(resolution=resolution, fps=args.fps, duration=args.duration)
        print(f"Generated: {path}")
    elif args.type == 'resolution':
        path = generator.generate_resolution_test(resolution=resolution, fps=args.fps, duration=args.duration)
        print(f"Generated: {path}")


if __name__ == '__main__':
    main()
