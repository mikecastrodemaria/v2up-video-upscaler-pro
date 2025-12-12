"""
Gradio UI for Video Upscaler Pro
"""

import gradio as gr
import torch
import sys
import os

def get_system_info():
    """Get system information for display"""
    info = []

    # Python version
    info.append(f"Python: {sys.version.split()[0]}")

    # PyTorch version
    info.append(f"PyTorch: {torch.__version__}")

    # CUDA availability
    if torch.cuda.is_available():
        info.append(f"CUDA: Available")
        info.append(f"GPU: {torch.cuda.get_device_name(0)}")
        vram = torch.cuda.get_device_properties(0).total_memory / (1024**3)
        info.append(f"VRAM: {vram:.1f} GB")
    else:
        info.append(f"CUDA: Not available (CPU mode)")

    # CPU info
    import psutil
    info.append(f"CPU Cores: {psutil.cpu_count()}")
    ram = psutil.virtual_memory().total / (1024**3)
    info.append(f"RAM: {ram:.1f} GB")

    return "\n".join(info)

def on_video_upload(video):
    """Called when a video is uploaded"""
    if video is None:
        return "No video uploaded", ""

    # Get video info using cv2
    import cv2
    cap = cv2.VideoCapture(video)

    if not cap.isOpened():
        return "Error: Could not open video", ""

    # Get video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps if fps > 0 else 0

    cap.release()

    # Format info
    info = f"Resolution: {width}x{height}\n"
    info += f"FPS: {fps:.2f}\n"
    info += f"Duration: {int(duration//60)}:{int(duration%60):02d}\n"
    info += f"Frames: {frame_count}"

    # Calculate output resolution (example: 2x scale)
    output_res = f"{width*2}x{height*2}"

    return info, output_res

def toggle_interpolation(enabled):
    """Show/hide interpolation options"""
    return (
        gr.update(visible=enabled),  # interpolation_model
        gr.update(visible=enabled),  # fps_multiplier
        gr.update(visible=enabled)   # target_fps
    )

def process_preview(video, model, scale, interp_enabled, interp_model, fps_mult):
    """Process video preview"""
    if video is None:
        return None, "Please upload a video first"

    return None, "Preview feature coming soon!\n\nThis will process the first 5 seconds of your video."

def process_full_video(video, model, scale, interp_enabled, interp_model, fps_mult, temporal):
    """Process full video"""
    if video is None:
        return None, "Please upload a video first", []

    return None, "Full processing feature coming soon!\n\nThis will upscale your entire video.", []

def create_interface():
    """Create the main Gradio interface"""

    with gr.Blocks(
        theme=gr.themes.Soft(),
        title="Video Upscaler Pro",
        css="""
        .main-header {
            text-align: center;
            margin-bottom: 2rem;
        }
        """
    ) as app:

        gr.Markdown("# 🎬 Video Upscaler Pro", elem_classes="main-header")
        gr.Markdown(
            "### Open Source Video Upscaling using Real-ESRGAN, SwinIR, and more\n"
            "Upload a video, choose your settings, and enhance your footage with AI."
        )

        with gr.Tabs():
            # ============================================================
            # TAB 1: PROCESSING
            # ============================================================
            with gr.Tab("🚀 Processing"):
                with gr.Row():
                    with gr.Column(scale=2):
                        # Video upload
                        video_input = gr.Video(
                            label="📹 Video Source",
                            format="mp4",
                            include_audio=True
                        )

                        # Video info
                        video_info = gr.Textbox(
                            label="📊 Video Information",
                            interactive=False,
                            placeholder="Upload a video to see details...",
                            lines=4
                        )

                        # Main settings
                        with gr.Group():
                            gr.Markdown("### ⚙️ Upscaling Settings")

                            spatial_model = gr.Dropdown(
                                choices=[
                                    "Real-ESRGAN (Fast, Excellent Quality)",
                                    "SwinIR (Slow, Maximum Quality)",
                                    "SeedVR2 (Temporal Coherence, High VRAM)"
                                ],
                                label="AI Model",
                                value="Real-ESRGAN (Fast, Excellent Quality)",
                                info="Choose the model based on your needs and hardware"
                            )

                            scale_factor = gr.Slider(
                                minimum=2,
                                maximum=8,
                                step=2,
                                value=4,
                                label="Scale Factor",
                                info="2x = 1080p→4K, 4x = 540p→4K"
                            )

                            output_resolution = gr.Textbox(
                                label="Output Resolution",
                                interactive=False,
                                placeholder="Will be calculated automatically"
                            )

                        # Interpolation settings
                        with gr.Group():
                            gr.Markdown("### 🎞️ FPS Interpolation (Optional)")

                            enable_interpolation = gr.Checkbox(
                                label="Enable FPS Interpolation",
                                value=False
                            )

                            interpolation_model = gr.Dropdown(
                                choices=["RIFE (Fast)", "DAIN (Maximum Quality)"],
                                label="Interpolation Model",
                                value="RIFE (Fast)",
                                visible=False
                            )

                            fps_multiplier = gr.Slider(
                                minimum=2,
                                maximum=4,
                                step=2,
                                value=2,
                                label="FPS Multiplier",
                                visible=False
                            )

                            target_fps = gr.Textbox(
                                label="Target FPS",
                                interactive=False,
                                visible=False
                            )

                    with gr.Column(scale=1):
                        # Preview and results
                        gr.Markdown("### 👁️ Preview / Result")

                        video_preview = gr.Video(
                            label="Preview (5 seconds)",
                            interactive=False
                        )

                        video_output = gr.Video(
                            label="Final Result",
                            interactive=False
                        )

                # Action buttons
                with gr.Row():
                    preview_btn = gr.Button(
                        "🔍 Preview (5 seconds)",
                        variant="secondary",
                        size="lg"
                    )
                    process_btn = gr.Button(
                        "🚀 Process Full Video",
                        variant="primary",
                        size="lg"
                    )

                # Progress and status
                with gr.Row():
                    eta_text = gr.Textbox(
                        label="⏱️ Estimated Time",
                        interactive=False,
                        scale=1
                    )
                    elapsed_text = gr.Textbox(
                        label="⏳ Elapsed Time",
                        interactive=False,
                        scale=1
                    )

                status_text = gr.Textbox(
                    label="📝 Status",
                    interactive=False,
                    lines=3
                )

            # ============================================================
            # TAB 2: COMPARISON
            # ============================================================
            with gr.Tab("📊 Comparison"):
                gr.Markdown("### Before / After Comparison")

                with gr.Row():
                    original_video = gr.Video(label="Original")
                    processed_video = gr.Video(label="Upscaled")

                comparison_slider = gr.Slider(
                    minimum=0,
                    maximum=100,
                    value=50,
                    label="Comparison Slider",
                    info="Adjust to see the difference"
                )

                metrics_display = gr.Dataframe(
                    headers=["Metric", "Value"],
                    label="Quality Metrics",
                    value=[
                        ["PSNR", "N/A"],
                        ["SSIM", "N/A"],
                        ["Flickering Score", "N/A"],
                        ["Processing Time", "N/A"]
                    ]
                )

            # ============================================================
            # TAB 3: SETTINGS
            # ============================================================
            with gr.Tab("⚙️ Advanced Settings"):
                gr.Markdown("### Advanced Configuration")

                with gr.Group():
                    gr.Markdown("#### 🎯 Temporal Coherence")

                    temporal_method = gr.Radio(
                        choices=[
                            "Auto (Recommended)",
                            "SeedVR2",
                            "Optical Flow",
                            "EMA Filter"
                        ],
                        value="Auto (Recommended)",
                        label="Temporal Coherence Method"
                    )

                    flickering_threshold = gr.Slider(
                        minimum=0.0,
                        maximum=1.0,
                        value=0.1,
                        label="Acceptable Flickering Threshold"
                    )

                with gr.Group():
                    gr.Markdown("#### 🖥️ Performance")

                    device_choice = gr.Radio(
                        choices=[
                            "Auto (Recommended)",
                            "GPU (CUDA)",
                            "CPU"
                        ],
                        value="Auto (Recommended)",
                        label="Processing Device"
                    )

                    batch_size = gr.Slider(
                        minimum=1,
                        maximum=32,
                        value=8,
                        step=1,
                        label="Batch Size (frames processed simultaneously)"
                    )

                    use_fp16 = gr.Checkbox(
                        label="Use FP16 (Faster, slight quality loss)",
                        value=True
                    )

                with gr.Group():
                    gr.Markdown("#### 💾 Export")

                    output_format = gr.Dropdown(
                        choices=[
                            "MP4 (H.264)",
                            "MP4 (H.265/HEVC)",
                            "AVI",
                            "MKV"
                        ],
                        value="MP4 (H.264)",
                        label="Output Format"
                    )

                    output_quality = gr.Slider(
                        minimum=0,
                        maximum=51,
                        value=18,
                        label="Quality CRF (0=lossless, 18=high, 28=medium, 51=low)"
                    )

            # ============================================================
            # TAB 4: SYSTEM INFO
            # ============================================================
            with gr.Tab("💻 System"):
                gr.Markdown("### System Information")

                system_info = gr.Textbox(
                    label="Detected Configuration",
                    lines=10,
                    interactive=False,
                    value=get_system_info()
                )

                refresh_btn = gr.Button("🔄 Refresh Information")

                gr.Markdown("### 📜 Application Logs")

                log_output = gr.Textbox(
                    label="Logs",
                    lines=15,
                    interactive=False,
                    placeholder="Logs will appear here during processing...",
                    autoscroll=True
                )

        # ============================================================
        # EVENT HANDLERS
        # ============================================================

        video_input.change(
            fn=on_video_upload,
            inputs=[video_input],
            outputs=[video_info, output_resolution]
        )

        enable_interpolation.change(
            fn=toggle_interpolation,
            inputs=[enable_interpolation],
            outputs=[interpolation_model, fps_multiplier, target_fps]
        )

        preview_btn.click(
            fn=process_preview,
            inputs=[
                video_input,
                spatial_model,
                scale_factor,
                enable_interpolation,
                interpolation_model,
                fps_multiplier
            ],
            outputs=[video_preview, status_text]
        )

        process_btn.click(
            fn=process_full_video,
            inputs=[
                video_input,
                spatial_model,
                scale_factor,
                enable_interpolation,
                interpolation_model,
                fps_multiplier,
                temporal_method
            ],
            outputs=[video_output, status_text, metrics_display]
        )

        refresh_btn.click(
            fn=get_system_info,
            outputs=[system_info]
        )

    return app


if __name__ == "__main__":
    app = create_interface()
    app.launch()
