#import ocr
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
def en_sla():
    src = "en"
    tgt = "sla"

    task_name = "translation_en_to_sla"
    model_name = f"Helsinki-NLP/opus-mt-{src}-{tgt}"
    sample_text = "Hello, how are you?"
    translator = pipeline(task_name, model = model_name, tokenizer = model_name)
    translation = translator("Hello, how are you?")[0]["translation_text"]
    print(translation)

def Main():
    #allText = ocr.Main()
    en_sla()
if __name__ == "__main__":
    Main() 