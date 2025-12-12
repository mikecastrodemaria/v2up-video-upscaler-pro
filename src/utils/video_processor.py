"""
Video Processor - Handle video I/O and FFmpeg operations
Extract frames, get metadata, and encode videos
"""

import cv2
import numpy as np
import os
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Generator
import logging

logger = logging.getLogger(__name__)


class VideoProcessor:
    """Handle video processing operations"""

    def __init__(self, video_path: str):
        """
        Initialize video processor

        Args:
            video_path: Path to video file

        Raises:
            FileNotFoundError: If video file doesn't exist
            ValueError: If video file cannot be opened
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")

        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)

        if not self.cap.isOpened():
            raise ValueError(f"Cannot open video file: {video_path}")

        self._metadata = self._extract_metadata()

    def _extract_metadata(self) -> Dict:
        """
        Extract video metadata

        Returns:
            dict: Video metadata
        """
        metadata = {
            'width': int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            'height': int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            'fps': self.cap.get(cv2.CAP_PROP_FPS),
            'frame_count': int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT)),
            'codec': int(self.cap.get(cv2.CAP_PROP_FOURCC)),
        }

        metadata['duration'] = metadata['frame_count'] / metadata['fps'] if metadata['fps'] > 0 else 0
        metadata['resolution'] = (metadata['width'], metadata['height'])

        return metadata

    def get_metadata(self) -> Dict:
        """
        Get video metadata

        Returns:
            dict: Video metadata including resolution, fps, duration, etc.
        """
        return self._metadata.copy()

    def get_frame_count(self) -> int:
        """Get total number of frames"""
        return self._metadata['frame_count']

    def get_fps(self) -> float:
        """Get video FPS"""
        return self._metadata['fps']

    def get_resolution(self) -> Tuple[int, int]:
        """Get video resolution as (width, height)"""
        return self._metadata['resolution']

    def get_duration(self) -> float:
        """Get video duration in seconds"""
        return self._metadata['duration']

    def read_frame(self, frame_number: Optional[int] = None) -> Optional[np.ndarray]:
        """
        Read a single frame

        Args:
            frame_number: Frame index to read (if None, reads next frame)

        Returns:
            numpy.ndarray: Frame as BGR image, or None if failed
        """
        if frame_number is not None:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

        ret, frame = self.cap.read()
        return frame if ret else None

    def extract_frames(
        self,
        start_frame: int = 0,
        end_frame: Optional[int] = None,
        step: int = 1
    ) -> Generator[Tuple[int, np.ndarray], None, None]:
        """
        Extract frames from video

        Args:
            start_frame: Starting frame index
            end_frame: Ending frame index (None = all frames)
            step: Frame step (1 = every frame, 2 = every other frame, etc.)

        Yields:
            tuple: (frame_index, frame_data)
        """
        if end_frame is None:
            end_frame = self.get_frame_count()

        self.cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

        for frame_idx in range(start_frame, end_frame, step):
            ret, frame = self.cap.read()
            if not ret:
                break

            yield frame_idx, frame

            # Skip frames if step > 1
            if step > 1:
                for _ in range(step - 1):
                    self.cap.read()

    def extract_frames_list(
        self,
        start_frame: int = 0,
        end_frame: Optional[int] = None,
        max_frames: Optional[int] = None
    ) -> List[np.ndarray]:
        """
        Extract frames as a list

        Args:
            start_frame: Starting frame index
            end_frame: Ending frame index (None = all frames)
            max_frames: Maximum number of frames to extract

        Returns:
            list: List of frames
        """
        frames = []

        if end_frame is None:
            end_frame = self.get_frame_count()

        if max_frames:
            end_frame = min(end_frame, start_frame + max_frames)

        for _, frame in self.extract_frames(start_frame, end_frame):
            frames.append(frame)

            if max_frames and len(frames) >= max_frames:
                break

        return frames

    def extract_segment(
        self,
        start_time: float,
        duration: float,
        output_path: str
    ) -> bool:
        """
        Extract a video segment using FFmpeg

        Args:
            start_time: Start time in seconds
            duration: Duration in seconds
            output_path: Output file path

        Returns:
            bool: True if successful
        """
        try:
            cmd = [
                'ffmpeg',
                '-i', self.video_path,
                '-ss', str(start_time),
                '-t', str(duration),
                '-c', 'copy',
                '-y',
                output_path
            ]

            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )

            return os.path.exists(output_path)

        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg error: {e.stderr.decode()}")
            return False
        except FileNotFoundError:
            logger.error("FFmpeg not found. Please install FFmpeg.")
            return False

    def has_audio(self) -> bool:
        """
        Check if video has audio track

        Returns:
            bool: True if audio exists
        """
        try:
            cmd = [
                'ffprobe',
                '-i', self.video_path,
                '-show_streams',
                '-select_streams', 'a',
                '-loglevel', 'error'
            ]

            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return len(result.stdout) > 0

        except FileNotFoundError:
            # FFprobe not available, assume audio exists
            return True

    def close(self):
        """Release video capture"""
        if self.cap is not None:
            self.cap.release()
            self.cap = None

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()

    def __del__(self):
        """Destructor"""
        self.close()


class VideoWriter:
    """Write frames to video file"""

    def __init__(
        self,
        output_path: str,
        fps: float,
        resolution: Tuple[int, int],
        codec: str = 'mp4v',
        audio_source: Optional[str] = None
    ):
        """
        Initialize video writer

        Args:
            output_path: Output video path
            fps: Frames per second
            resolution: (width, height)
            codec: Video codec fourcc
            audio_source: Path to video with audio to copy
        """
        self.output_path = output_path
        self.fps = fps
        self.resolution = resolution
        self.audio_source = audio_source

        # Create temporary file for video without audio
        self.temp_path = None
        if audio_source:
            self.temp_path = output_path.replace('.mp4', '_temp.mp4')
            actual_output = self.temp_path
        else:
            actual_output = output_path

        # Initialize VideoWriter
        fourcc = cv2.VideoWriter_fourcc(*codec)
        self.writer = cv2.VideoWriter(
            actual_output,
            fourcc,
            fps,
            resolution
        )

        if not self.writer.isOpened():
            raise ValueError(f"Cannot create video writer for: {output_path}")

        self.frame_count = 0

    def write_frame(self, frame: np.ndarray):
        """
        Write a single frame

        Args:
            frame: Frame to write (BGR format)
        """
        # Ensure frame is correct size
        if frame.shape[1] != self.resolution[0] or frame.shape[0] != self.resolution[1]:
            frame = cv2.resize(frame, self.resolution)

        self.writer.write(frame)
        self.frame_count += 1

    def write_frames(self, frames: List[np.ndarray]):
        """
        Write multiple frames

        Args:
            frames: List of frames to write
        """
        for frame in frames:
            self.write_frame(frame)

    def close(self, copy_audio: bool = True):
        """
        Finalize video and optionally copy audio

        Args:
            copy_audio: Whether to copy audio from source
        """
        if self.writer is not None:
            self.writer.release()
            self.writer = None

        # Copy audio if source provided
        if copy_audio and self.audio_source and self.temp_path:
            self._copy_audio()

    def _copy_audio(self):
        """Copy audio from source video using FFmpeg"""
        try:
            cmd = [
                'ffmpeg',
                '-i', self.temp_path,
                '-i', self.audio_source,
                '-c:v', 'copy',
                '-c:a', 'aac',
                '-map', '0:v:0',
                '-map', '1:a:0?',
                '-shortest',
                '-y',
                self.output_path
            ]

            subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )

            # Remove temporary file
            if os.path.exists(self.temp_path):
                os.remove(self.temp_path)

        except subprocess.CalledProcessError as e:
            logger.warning(f"Failed to copy audio: {e.stderr.decode()}")
            # Copy temp file as final output
            if os.path.exists(self.temp_path):
                shutil.move(self.temp_path, self.output_path)

        except FileNotFoundError:
            logger.warning("FFmpeg not found. Video will not have audio.")
            if os.path.exists(self.temp_path):
                shutil.move(self.temp_path, self.output_path)

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()

    def __del__(self):
        """Destructor"""
        self.close(copy_audio=False)


def get_video_info(video_path: str) -> Dict:
    """
    Get video information without opening VideoProcessor

    Args:
        video_path: Path to video file

    Returns:
        dict: Video information
    """
    with VideoProcessor(video_path) as vp:
        return vp.get_metadata()


def format_duration(seconds: float) -> str:
    """
    Format duration as HH:MM:SS

    Args:
        seconds: Duration in seconds

    Returns:
        str: Formatted duration
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes}:{secs:02d}"
