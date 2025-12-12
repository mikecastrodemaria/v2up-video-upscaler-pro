"""
Temporal Interpolator - FPS interpolation for videos
Increases frame rate using frame interpolation models
"""

import time
import logging
from typing import Dict, Optional, Callable, List
from pathlib import Path

from ..models.rife_model import create_rife_model, SimpleFrameInterpolator
from ..utils.video_processor import VideoProcessor, VideoWriter
from ..utils.system_manager import get_system_manager

logger = logging.getLogger(__name__)


class TemporalInterpolator:
    """
    Handles temporal interpolation (FPS increase) of videos
    """

    def __init__(
        self,
        model_name: str = 'rife',
        device: str = 'auto'
    ):
        """
        Initialize temporal interpolator

        Args:
            model_name: Model to use ('rife', 'simple')
            device: 'cuda', 'cpu', or 'auto'
        """
        self.model_name = model_name
        self.sys_manager = get_system_manager()

        # Determine device
        if device == 'auto':
            device = self.sys_manager.get_device()

        self.device = device

        # Initialize model
        self.model = None
        self._load_model()

    def _load_model(self):
        """Load the interpolation model"""
        logger.info(f"Loading {self.model_name} interpolation model (device={self.device})")

        try:
            if self.model_name.lower() == 'rife':
                self.model = create_rife_model(
                    device=self.device,
                    fp16=self.sys_manager.optimal_settings.get('use_fp16', True)
                )
                logger.info("RIFE interpolation model loaded (using optical flow fallback)")

            elif self.model_name.lower() == 'simple':
                self.model = SimpleFrameInterpolator(device=self.device)
                logger.info("Simple interpolation model loaded")

            else:
                raise ValueError(f"Unknown model: {self.model_name}")

        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            logger.warning("Falling back to simple interpolation")
            self.model = SimpleFrameInterpolator(device=self.device)

    def interpolate_video(
        self,
        input_path: str,
        output_path: str,
        fps_multiplier: int = 2,
        target_fps: Optional[float] = None,
        progress_callback: Optional[Callable[[int, int, float], None]] = None
    ) -> Dict:
        """
        Interpolate video to increase FPS

        Args:
            input_path: Input video path
            output_path: Output video path
            fps_multiplier: FPS multiplier (2, 4, 8)
            target_fps: Target FPS (overrides multiplier)
            progress_callback: Optional callback(current_frame, total_frames, eta)

        Returns:
            dict: Processing results with 'success', 'output_path', 'metrics'
        """
        logger.info(f"Starting FPS interpolation: {input_path}")
        logger.info(f"Output: {output_path}")
        logger.info(f"FPS Multiplier: {fps_multiplier}x")

        start_time = time.time()

        try:
            # Open input video
            with VideoProcessor(input_path) as vp:
                metadata = vp.get_metadata()
                original_fps = metadata['fps']

                logger.info(f"Original FPS: {original_fps}")
                logger.info(f"Resolution: {metadata['width']}x{metadata['height']}")
                logger.info(f"Total frames: {metadata['frame_count']}")

                # Calculate target FPS
                if target_fps is None:
                    target_fps = original_fps * fps_multiplier

                # Validate target FPS
                if target_fps > 240:
                    logger.warning(f"Target FPS {target_fps} is very high, capping at 240")
                    target_fps = 240
                    fps_multiplier = int(target_fps / original_fps)

                logger.info(f"Target FPS: {target_fps}")

                # Calculate actual multiplier
                actual_multiplier = int(round(target_fps / original_fps))

                if actual_multiplier < 2:
                    logger.warning("FPS multiplier < 2, no interpolation needed")
                    # Just copy the video
                    import shutil
                    shutil.copy(input_path, output_path)
                    return {
                        'success': True,
                        'output_path': output_path,
                        'original_fps': original_fps,
                        'new_fps': original_fps,
                        'metrics': {
                            'total_time': time.time() - start_time,
                            'frames_processed': metadata['frame_count'],
                            'original_fps': original_fps,
                            'new_fps': original_fps
                        }
                    }

                # Open output video writer
                output_frame_count = (metadata['frame_count'] - 1) * actual_multiplier + 1

                with VideoWriter(
                    output_path,
                    fps=target_fps,
                    resolution=(metadata['width'], metadata['height']),
                    audio_source=input_path
                ) as writer:

                    # Process frames in batches
                    processed_count = 0
                    output_frame_count_actual = 0
                    frame_times = []

                    # Extract all frames first (for better interpolation)
                    logger.info("Extracting frames...")
                    frames = vp.extract_frames_list(max_frames=metadata['frame_count'])

                    logger.info(f"Interpolating {len(frames)} frames to {len(frames) * actual_multiplier} frames...")

                    # Process frame pairs
                    for i in range(len(frames) - 1):
                        frame_start = time.time()

                        # Write original frame
                        writer.write_frame(frames[i])
                        output_frame_count_actual += 1

                        # Interpolate between this frame and next
                        if actual_multiplier > 1:
                            interpolated = self.model.interpolate_frames(
                                frames[i],
                                frames[i + 1],
                                num_intermediates=actual_multiplier - 1
                            )

                            # Write interpolated frames
                            for interp_frame in interpolated:
                                writer.write_frame(interp_frame)
                                output_frame_count_actual += 1

                        processed_count += 1
                        frame_time = time.time() - frame_start
                        frame_times.append(frame_time)

                        # Calculate ETA
                        if len(frame_times) > 0:
                            avg_time = sum(frame_times[-10:]) / min(len(frame_times), 10)
                            remaining_frames = len(frames) - 1 - processed_count
                            eta = remaining_frames * avg_time
                        else:
                            eta = 0

                        # Progress callback
                        if progress_callback and processed_count % 5 == 0:
                            progress_callback(processed_count, len(frames) - 1, eta)

                        # Log progress
                        if processed_count % 50 == 0:
                            logger.info(f"Processed {processed_count}/{len(frames)-1} frame pairs ({processed_count/(len(frames)-1)*100:.1f}%)")

                    # Write last frame
                    writer.write_frame(frames[-1])
                    output_frame_count_actual += 1

            # Calculate metrics
            total_time = time.time() - start_time

            logger.info(f"FPS interpolation completed in {total_time:.2f}s")
            logger.info(f"Original frames: {metadata['frame_count']}")
            logger.info(f"Output frames: {output_frame_count_actual}")
            logger.info(f"FPS: {original_fps:.2f} -> {target_fps:.2f}")

            return {
                'success': True,
                'output_path': output_path,
                'original_fps': original_fps,
                'new_fps': target_fps,
                'metrics': {
                    'total_time': total_time,
                    'frames_processed': processed_count,
                    'original_frame_count': metadata['frame_count'],
                    'output_frame_count': output_frame_count_actual,
                    'original_fps': original_fps,
                    'new_fps': target_fps,
                    'fps_multiplier': actual_multiplier,
                    'avg_time_per_pair': total_time / processed_count if processed_count > 0 else 0
                }
            }

        except Exception as e:
            logger.error(f"Error during FPS interpolation: {e}", exc_info=True)
            return {
                'success': False,
                'error': str(e),
                'output_path': None,
                'original_fps': None,
                'new_fps': None,
                'metrics': {}
            }

    def interpolate_preview(
        self,
        input_path: str,
        output_path: str,
        fps_multiplier: int = 2,
        duration: float = 5.0,
        progress_callback: Optional[Callable[[int, int, float], None]] = None
    ) -> Dict:
        """
        Interpolate first N seconds for preview

        Args:
            input_path: Input video path
            output_path: Output video path
            fps_multiplier: FPS multiplier
            duration: Duration in seconds to process
            progress_callback: Optional progress callback

        Returns:
            dict: Processing results
        """
        logger.info(f"Creating FPS interpolation preview ({duration}s) of {input_path}")

        try:
            # Create temporary segment
            import tempfile
            temp_segment = tempfile.mktemp(suffix='_segment.mp4')

            # Extract segment
            with VideoProcessor(input_path) as vp:
                fps = vp.get_fps()
                vp.extract_segment(0, duration, temp_segment)

            # Interpolate segment
            result = self.interpolate_video(
                temp_segment,
                output_path,
                fps_multiplier=fps_multiplier,
                progress_callback=progress_callback
            )

            # Clean up
            import os
            if os.path.exists(temp_segment):
                os.remove(temp_segment)

            return result

        except Exception as e:
            logger.error(f"Error creating preview: {e}")
            return {
                'success': False,
                'error': str(e),
                'output_path': None,
                'original_fps': None,
                'new_fps': None,
                'metrics': {}
            }

    def detect_source_fps(self, video_path: str) -> float:
        """
        Detect source video FPS

        Args:
            video_path: Path to video

        Returns:
            float: FPS
        """
        with VideoProcessor(video_path) as vp:
            return vp.get_fps()

    def estimate_processing_time(self, input_path: str, fps_multiplier: int = 2) -> Dict:
        """
        Estimate processing time for a video

        Args:
            input_path: Input video path
            fps_multiplier: FPS multiplier

        Returns:
            dict: Estimated times
        """
        try:
            with VideoProcessor(input_path) as vp:
                metadata = vp.get_metadata()

            # Rough estimates based on hardware
            if self.device == 'cuda':
                vram = self.sys_manager.device_info['vram_total_gb']

                if vram >= 8:
                    time_per_pair = 0.2  # GPU with good VRAM
                elif vram >= 4:
                    time_per_pair = 0.4  # Entry-level GPU
                else:
                    time_per_pair = 0.6  # Low VRAM GPU
            else:
                time_per_pair = 2.0  # CPU is slower

            # Adjust for multiplier (more interpolated frames = more time)
            time_per_pair *= (fps_multiplier / 2.0)

            frame_pairs = metadata['frame_count'] - 1
            total_time = time_per_pair * frame_pairs

            return {
                'frame_pairs': frame_pairs,
                'estimated_time_per_pair': time_per_pair,
                'estimated_total_time': total_time,
                'estimated_total_time_formatted': self._format_time(total_time)
            }

        except Exception as e:
            logger.error(f"Error estimating time: {e}")
            return {
                'error': str(e)
            }

    def _format_time(self, seconds: float) -> str:
        """Format seconds as HH:MM:SS"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)

        if hours > 0:
            return f"{hours}h {minutes}m {secs}s"
        elif minutes > 0:
            return f"{minutes}m {secs}s"
        else:
            return f"{secs}s"


def create_interpolator(
    model_name: str = 'rife',
    device: str = 'auto'
) -> TemporalInterpolator:
    """
    Factory function to create interpolator

    Args:
        model_name: Model name ('rife', 'simple')
        device: Device ('cuda', 'cpu', 'auto')

    Returns:
        TemporalInterpolator: Initialized interpolator
    """
    return TemporalInterpolator(
        model_name=model_name,
        device=device
    )
