"""
System Manager - Hardware detection and optimization
Handles GPU/CPU detection and provides optimal settings recommendations
"""

import torch
import platform
import os
from typing import Dict, Tuple


class SystemManager:
    """Manages system detection and optimization settings"""

    def __init__(self):
        """Initialize system manager and detect hardware"""
        self.device_info = self._detect_device()
        self.optimal_settings = self._calculate_optimal_settings()

    def _detect_device(self) -> Dict:
        """
        Detect available hardware (GPU/CPU)

        Returns:
            dict: Hardware information
        """
        info = {
            'platform': platform.system(),
            'has_cuda': torch.cuda.is_available(),
            'device_count': 0,
            'device_name': 'CPU',
            'vram_total_gb': 0.0,
            'vram_available_gb': 0.0,
            'cpu_count': os.cpu_count() or 1,
            'ram_total_gb': 0.0
        }

        if torch.cuda.is_available():
            info['device_count'] = torch.cuda.device_count()
            info['device_name'] = torch.cuda.get_device_name(0)
            props = torch.cuda.get_device_properties(0)
            info['vram_total_gb'] = props.total_memory / (1024**3)
            info['vram_available_gb'] = self._get_available_vram()

        # Get RAM info
        try:
            import psutil
            info['ram_total_gb'] = psutil.virtual_memory().total / (1024**3)
        except ImportError:
            # psutil not available, estimate
            info['ram_total_gb'] = 16.0

        return info

    def _get_available_vram(self) -> float:
        """
        Calculate available VRAM in GB

        Returns:
            float: Available VRAM in GB
        """
        if not torch.cuda.is_available():
            return 0.0

        try:
            torch.cuda.empty_cache()
            props = torch.cuda.get_device_properties(0)
            allocated = torch.cuda.memory_allocated(0)
            available = (props.total_memory - allocated) / (1024**3)
            return max(0.0, available)
        except Exception:
            return 0.0

    def _calculate_optimal_settings(self) -> Dict:
        """
        Calculate optimal settings based on hardware

        Returns:
            dict: Recommended settings
        """
        settings = {
            'device': 'cpu',
            'batch_size': 1,
            'use_fp16': False,
            'recommended_model': 'realesrgan',
            'max_scale_factor': 2,
            'enable_temporal_coherence': False,
            'temporal_method': 'ema_filter',
            'tile_size': 256  # For splitting large images
        }

        if self.device_info['has_cuda']:
            vram = self.device_info['vram_available_gb']

            settings['device'] = 'cuda'
            settings['use_fp16'] = True  # Almost always beneficial

            if vram >= 16:
                # High-end GPU (RTX 4090, RTX 3090, etc.)
                settings['batch_size'] = 16
                settings['recommended_model'] = 'realesrgan'  # seedvr2 not yet implemented
                settings['max_scale_factor'] = 8
                settings['enable_temporal_coherence'] = True
                settings['temporal_method'] = 'optical_flow'
                settings['tile_size'] = 512
            elif vram >= 8:
                # Mid-range GPU (RTX 3060, RTX 3070, etc.)
                settings['batch_size'] = 8
                settings['recommended_model'] = 'realesrgan'
                settings['max_scale_factor'] = 4
                settings['enable_temporal_coherence'] = True
                settings['temporal_method'] = 'optical_flow'
                settings['tile_size'] = 384
            elif vram >= 4:
                # Entry-level GPU (GTX 1650, RTX 3050, etc.)
                settings['batch_size'] = 4
                settings['recommended_model'] = 'realesrgan'
                settings['max_scale_factor'] = 2
                settings['enable_temporal_coherence'] = False
                settings['tile_size'] = 256
            else:
                # Very low VRAM, use conservative settings
                settings['batch_size'] = 1
                settings['max_scale_factor'] = 2
                settings['tile_size'] = 128

        return settings

    def adjust_for_video(self, video_resolution: Tuple[int, int], scale_factor: int) -> Dict:
        """
        Adjust settings for specific video resolution

        Args:
            video_resolution: (width, height) tuple
            scale_factor: Upscaling factor (2, 4, or 8)

        Returns:
            dict: Adjusted settings

        Raises:
            ValueError: If output resolution exceeds 8K
        """
        width, height = video_resolution
        output_width = width * scale_factor
        output_height = height * scale_factor

        adjusted = self.optimal_settings.copy()

        # Validate output resolution (8K max)
        if output_width > 7680 or output_height > 4320:
            raise ValueError(
                f"Output resolution ({output_width}x{output_height}) exceeds 8K limit. "
                f"Please reduce scale factor or use lower resolution input."
            )

        # Adjust batch size based on output resolution
        output_pixels = output_width * output_height

        if output_pixels > 3840 * 2160:  # 4K+
            adjusted['batch_size'] = max(1, adjusted['batch_size'] // 2)

        if output_pixels > 7680 * 4320 / 2:  # Near 8K
            adjusted['batch_size'] = 1
            adjusted['tile_size'] = min(adjusted['tile_size'], 256)

        return adjusted

    def get_device(self) -> str:
        """
        Get the device string for PyTorch

        Returns:
            str: 'cuda' or 'cpu'
        """
        return self.optimal_settings['device']

    def get_info_string(self) -> str:
        """
        Get formatted system information string

        Returns:
            str: Formatted system information
        """
        info = self.device_info
        settings = self.optimal_settings

        lines = [
            f"Platform: {info['platform']}",
            f"Device: {info['device_name']}",
        ]

        if info['has_cuda']:
            lines.append(f"CUDA: Available")
            lines.append(f"VRAM: {info['vram_available_gb']:.1f} GB available / {info['vram_total_gb']:.1f} GB total")
        else:
            lines.append(f"CUDA: Not available (CPU mode)")

        lines.extend([
            f"CPU Cores: {info['cpu_count']}",
            f"RAM: {info['ram_total_gb']:.1f} GB",
            "",
            "Recommended Settings:",
            f"  Model: {settings['recommended_model']}",
            f"  Device: {settings['device']}",
            f"  Batch Size: {settings['batch_size']}",
            f"  Max Scale: {settings['max_scale_factor']}x",
            f"  FP16: {'Enabled' if settings['use_fp16'] else 'Disabled'}",
            f"  Temporal Coherence: {settings['temporal_method'] if settings['enable_temporal_coherence'] else 'Disabled'}",
        ])

        return "\n".join(lines)

    def check_vram_requirement(self, required_gb: float) -> Tuple[bool, str]:
        """
        Check if sufficient VRAM is available

        Args:
            required_gb: Required VRAM in GB

        Returns:
            tuple: (is_sufficient, message)
        """
        if not self.device_info['has_cuda']:
            return False, "No CUDA device available. CPU mode will be used (slower)."

        available = self.device_info['vram_available_gb']

        if available >= required_gb:
            return True, f"Sufficient VRAM: {available:.1f} GB available"
        else:
            return False, (
                f"Insufficient VRAM: {available:.1f} GB available, {required_gb:.1f} GB required. "
                f"Consider reducing scale factor or batch size."
            )

    def optimize_batch_size(self, base_batch_size: int, current_vram_usage: float) -> int:
        """
        Dynamically adjust batch size based on VRAM usage

        Args:
            base_batch_size: Initial batch size
            current_vram_usage: Current VRAM usage in GB

        Returns:
            int: Adjusted batch size
        """
        if not self.device_info['has_cuda']:
            return 1

        available = self.device_info['vram_available_gb']

        # If we're using more than 80% of available VRAM, reduce batch size
        if current_vram_usage > available * 0.8:
            return max(1, base_batch_size // 2)

        return base_batch_size

    def clear_cache(self):
        """Clear GPU cache to free memory"""
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.synchronize()


# Global instance
_system_manager = None


def get_system_manager() -> SystemManager:
    """
    Get global SystemManager instance (singleton)

    Returns:
        SystemManager: Global system manager instance
    """
    global _system_manager
    if _system_manager is None:
        _system_manager = SystemManager()
    return _system_manager
