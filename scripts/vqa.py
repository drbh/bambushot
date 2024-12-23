from transformers import AutoModelForCausalLM, AutoTokenizer
from PIL import Image

model_id = "vikhyatk/moondream2"
revision = "2024-08-26"
model = AutoModelForCausalLM.from_pretrained(
    model_id, trust_remote_code=True, revision=revision
)
tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision)

image = Image.open("stream-cam/latest_frame_1.jpg")
enc_image = model.encode_image(image)
print(model.answer_question(enc_image, "is the printer bed clear of items and ready to print?", tokenizer))


# print(model.answer_question(enc_image, "hows the print going?", tokenizer))