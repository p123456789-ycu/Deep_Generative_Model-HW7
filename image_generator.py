import torch
import numpy as np
from PIL import Image
from diffusers import (
    StableDiffusionControlNetPipeline,
    ControlNetModel,
    UniPCMultistepScheduler
)
from controlnet_aux import CannyDetector

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Device: {device}")

# =====================================
# Load ControlNet Canny
# =====================================

print("Loading ControlNet Canny...")

controlnet = ControlNetModel.from_pretrained(
    "lllyasviel/sd-controlnet-canny",
    torch_dtype=torch.float16
)

pipe = StableDiffusionControlNetPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    controlnet=controlnet,
    torch_dtype=torch.float16
)

pipe.scheduler = UniPCMultistepScheduler.from_config(
    pipe.scheduler.config
)

pipe.enable_model_cpu_offload()
pipe.enable_attention_slicing()

print("ControlNet Ready")

# =====================================
# Canny Edge Detector
# =====================================

canny = CannyDetector()


def get_canny_image(image: Image.Image) -> Image.Image:
    """Convert PIL image to Canny edge map."""
    canny_image = canny(image)
    return canny_image


# =====================================
# Generate image with ControlNet
# =====================================

def generate_image(
    prompt: str,
    landmark_image: Image.Image = None
) -> Image.Image:
    """
    Generate a World Cup travel poster using ControlNet Canny.

    Args:
        prompt: Text prompt from LLM agent
        landmark_image: PIL Image of the city landmark (from landmark_fetcher)

    Returns:
        Generated PIL Image
    """

    if landmark_image is None:
        # Fallback: 純文字生成（無 ControlNet）
        print("No landmark image provided, using text-only generation.")
        from diffusers import AutoPipelineForText2Image
        fallback_pipe = AutoPipelineForText2Image.from_pretrained(
            "stabilityai/sdxl-turbo",
            torch_dtype=torch.float16,
            variant="fp16"
        ).to(device)
        image = fallback_pipe(
            prompt,
            num_inference_steps=4,
            guidance_scale=0.0,
            width=512,
            height=512
        ).images[0]
        return image

    # Canny 邊緣偵測
    print("Running Canny edge detection...")
    canny_image = get_canny_image(landmark_image)

    # ControlNet 生成
    print("Generating with ControlNet...")
    result = pipe(
        prompt=prompt,
        image=canny_image,
        num_inference_steps=20,
        guidance_scale=7.5,
        width=512,
        height=512
    )

    return result.images[0]
