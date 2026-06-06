# run_animagine_mac.py
import os
import gc
from datetime import datetime

import torch
from diffusers import StableDiffusionXLPipeline
from PIL import Image

print("=" * 60)
print("ANIMAGINE XL GENERATOR - MAC VERSION")
print("=" * 60)

# Hindari warning/tokenizer error tertentu
os.environ["TOKENIZERS_PARALLELISM"] = "false"

print("\n🔍 System Check:")
print(f"PyTorch version: {torch.__version__}")
print(f"MPS available: {torch.backends.mps.is_available()}")
print(f"CUDA available: {torch.cuda.is_available()}")

# Pilih device otomatis
if torch.backends.mps.is_available():
    device = "mps"
    dtype = torch.float16
    print("✅ Menggunakan Apple GPU / MPS")
elif torch.cuda.is_available():
    device = "cuda"
    dtype = torch.float16
    print(f"✅ Menggunakan CUDA GPU: {torch.cuda.get_device_name(0)}")
else:
    device = "cpu"
    dtype = torch.float32
    print("⚠️ GPU tidak tersedia, menggunakan CPU")

# Bersihkan memori
gc.collect()
if device == "cuda":
    torch.cuda.empty_cache()
    torch.cuda.synchronize()

try:
    print("\n📥 Loading model...")

    pipe = StableDiffusionXLPipeline.from_pretrained(
        "Linaqruf/animagine-xl",
        torch_dtype=dtype,
        use_safetensors=True,
        variant="fp16" if device in ["mps", "cuda"] else None,
        low_cpu_mem_usage=True
    )

    pipe = pipe.to(device)

    # Optimasi aman untuk Mac
    pipe.enable_attention_slicing()
    pipe.enable_vae_slicing()

    print("✅ Model siap digunakan!")

    while True:
        print("\n" + "=" * 60)

        prompt = input("🎨 Prompt atau ketik 'quit' untuk keluar: ").strip()

        if prompt.lower() in ["quit", "exit", "q"]:
            break

        if not prompt:
            prompt = "1girl, anime style, masterpiece, best quality"

        negative = input("📝 Negative prompt, Enter untuk default: ").strip()

        if not negative:
            negative = (
                "low quality, bad anatomy, bad hands, missing fingers, "
                "extra fingers, blurry, worst quality"
            )

        try:
            print("\n⏳ Generating...")

            with torch.no_grad():
                image = pipe(
                    prompt=prompt,
                    negative_prompt=negative,
                    num_inference_steps=20,
                    guidance_scale=7.5,
                    width=512,
                    height=768
                ).images[0]

            os.makedirs("outputs", exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"outputs/animagine_mac_{timestamp}.png"

            image.save(filename)
            print(f"✅ Gambar tersimpan: {filename}")

            try:
                image.show()
            except Exception:
                pass

            # Bersihkan memori setelah generate
            gc.collect()
            if device == "mps":
                torch.mps.empty_cache()
            elif device == "cuda":
                torch.cuda.empty_cache()

        except RuntimeError as e:
            error_text = str(e).lower()

            if "out of memory" in error_text or "mps backend out of memory" in error_text:
                print("❌ Memori GPU tidak cukup.")
                print("Coba turunkan resolusi menjadi 512x512.")
                print("Atau kurangi num_inference_steps menjadi 15.")
            else:
                print(f"❌ Error saat generate: {e}")

    print("\n👋 Sampai jumpa!")

except Exception as e:
    print(f"\n❌ Fatal Error: {e}")

    print("\n🔧 TROUBLESHOOTING MAC:")
    print("1. Install library:")
    print("   pip install torch torchvision torchaudio diffusers transformers accelerate safetensors pillow")

    print("\n2. Cek apakah MPS aktif:")
    print("   python -c \"import torch; print(torch.backends.mps.is_available())\"")

    print("\n3. Kalau Mac Intel, kemungkinan akan jalan di CPU dan sangat lambat.")

    print("\n4. Kalau memori tidak cukup, ubah bagian width/height:")
    print("   width=512")
    print("   height=512")