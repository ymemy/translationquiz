generated_sentence, translated_sentence = generate_sentences(language)
print(f"Generated sentence in {language.capitalize()}: {generated_sentence}")
print(f"Translated to English: {translated_sentence}")

from transformers import MarianMTModel, MarianTokenizer
from transformers import AutoTokenizer, AutoModelForCausalLM

"""
Tokenizer converts raw text into tokens that the model can process.
Model processes the tokens and generates an output (e.g., translation, text generation).

"""

def load_french_sentences():
    """Loads french statements"""
    tokenizer = AutoTokenizer.from_pretrained("dbddv01/gpt2-french-small")
    model = AutoModelForCausalLM.from_pretrained("dbddv01/gpt2-french-small")
    return(tokenizer,model)

def load_spanish_sentences():
    """Loads spanish statements"""
    tokenizer = AutoTokenizer.from_pretrained("DeepESP/gpt2-spanish")
    model = AutoModelForCausalLM.from_pretrained("DeepESP/gpt2-spanish")
    return(tokenizer,model)

def load_japanese_sentences():
    """Loads japanese statements"""
    tokenizer = AutoTokenizer.from_pretrained("abeja/gpt2-large-japanese")
    model = AutoModelForCausalLM.from_pretrained("abeja/gpt2-large-japanese")
    return(tokenizer,model)
def load_mandarin_sentences():
    """Loads chinese statements"""
    tokenizer = AutoTokenizer.from_pretrained("uer/gpt2-chinese-cluecorpussmall")
    model = AutoModelForCausalLM.from_pretrained("uer/gpt2-chinese-cluecorpussmall")
    return(tokenizer,model)

def load_german_sentences():
    """Loads german statements"""
    tokenizer = AutoTokenizer.from_pretrained("stefan-it/german-gpt2-larger")
    model = AutoModelForCausalLM.from_pretrained("stefan-it/german-gpt2-larger")
    return(tokenizer,model)


def load_translation_model():

    model_name = "Helsinki-NLP/opus-mt-mul-en"
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    return tokenizer, model

"""Function to translate text to English"""
def translate_to_english(text, tokenizer, model):
    try:
        # Tokenize the input text
        inputs = tokenizer(text, return_tensors="pt", padding=True)
        # Translate the input text
        translated = model.generate(**inputs)
        # Decode the translated text
        output = tokenizer.decode(translated[0], skip_special_tokens=True)
        return output
    except Exception as e:
        return f"Error in translation: {str(e)}"

def generate_sentences(language):
    """Generates a sentence in the specified language."""
    # Language model mapping
    model_loaders = {
        'french': load_french_sentences,
        'spanish': load_spanish_sentences,
        'japanese': load_japanese_sentences,
        'mandarin': load_mandarin_sentences,
        'german': load_german_sentences
    }

    # Validate language 
    language = language.lower()
    if language not in model_loaders:
        return f"Unsupported language: {language}"

"""Load model and tokenizer"""
    tokenizer, model = model_loaders[language]()

    input_prompt = f"Please generate a sentence in {language}: "
    inputs = tokenizer(input_prompt, return_tensors="pt")
    output = model.generate(inputs["input_ids"], max_length=50, num_return_sequences=1)
    generated_sentence = tokenizer.decode(output[0], skip_special_tokens=True)

    # Translate the sentence to English
    translation_tokenizer, translation_model = load_translation_model()
    translated_sentence = translate_to_english(generated_sentence, translation_tokenizer, translation_model)

    return generated_sentence, translated_sentence

language = input("Language:")
generated_sentence, translated_sentence = generate_sentences(language)
print(f"Generated sentence {language.capitalize()}: {generated_sentence}")
print(f"Translated to English: {translated_sentence}")