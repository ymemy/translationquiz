from transformers import MarianMTModel, MarianTokenizer
from transformers import AutoTokenizer, AutoModelForCausalLM

def load_french_model():
    """Loads French tokenizer and model."""
    tokenizer = AutoTokenizer.from_pretrained("dbddv01/gpt2-french-small")
    model = AutoModelForCausalLM.from_pretrained("dbddv01/gpt2-french-small")
    return tokenizer, model

def load_spanish_model():
    """Loads Spanish tokenizer and model."""
    tokenizer = AutoTokenizer.from_pretrained("DeepESP/gpt2-spanish")
    model = AutoModelForCausalLM.from_pretrained("DeepESP/gpt2-spanish")
    return tokenizer, model

def load_japanese_model():
    """Loads Japanese tokenizer and model."""
    tokenizer = AutoTokenizer.from_pretrained("abeja/gpt2-large-japanese")
    model = AutoModelForCausalLM.from_pretrained("abeja/gpt2-large-japanese")
    return tokenizer, model

def load_mandarin_model():
    """Loads Mandarin tokenizer and model."""
    tokenizer = AutoTokenizer.from_pretrained("uer/gpt2-chinese-cluecorpussmall")
    model = AutoModelForCausalLM.from_pretrained("uer/gpt2-chinese-cluecorpussmall")
    return tokenizer, model

def load_german_model():
    """Loads German tokenizer and model."""
    tokenizer = AutoTokenizer.from_pretrained("stefan-it/german-gpt2-larger")
    model = AutoModelForCausalLM.from_pretrained("stefan-it/german-gpt2-larger")
    return tokenizer, model

def load_translation_model():

    """Loads the multilingual-to-English translation model."""
    model_name = "Helsinki-NLP/opus-mt-mul-en"
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    return tokenizer, model

# Load the translation model once for reuse
translation_tokenizer, translation_model = load_translation_model()

# Map languages to their respective loading functions
language_model_map = {
    'french': load_french_model,
    'spanish': load_spanish_model,
    'japanese': load_japanese_model,
    'mandarin': load_mandarin_model,
    'german': load_german_model
}

COMMON_WORDS = {
    'french': ["le", "la", "les", "de", "du", "des", "et", "à", "un", "une"],
    'spanish': ["el", "la", "los", "las", "de", "y", "en", "un", "una","es"],
    'japanese': ["の", "に", "は", "を", "が", "と", "も", "で"],
    'mandarin': ["的", "了", "在", "和", "是", "有", "我", "你"],
    'german': ["der", "die", "das", "und", "zu", "ein", "eine", "auf"]
}

# Generate a random word
def generate_random_word(language):
    """Generate a random word in the specified language, excluding common words."""
    if language not in language_model_map:
        return f"Unsupported language: {language}"
    
    # Load model and tokenizer
    tokenizer, model = language_model_map[language]()
    
    # Language-specific prompts
    prompts = {
        'french': "Donne un seul mot en français (pas de phrases ni de ponctuation).",
        'spanish': "Dame una sola palabra en español (sin frases ni puntuación).",
        'japanese': "ランダムな日本語の単語を1つ教えてください（句読点なし）。",
        'mandarin': "给我一个随机的中文单词（不带标点）。",
        'german': "Gib mir ein einziges deutsches Wort (keine Sätze oder Satzzeichen)."
    }
    input_prompt = prompts.get(language, f"Generate a random word in {language}:")
    
    # Retry up to 5 times to generate a valid word
    for _ in range(5):
        inputs = tokenizer(input_prompt, return_tensors="pt", padding=True, truncation=True)
        model.config.pad_token_id = tokenizer.eos_token_id
        output = model.generate(
            inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_new_tokens=1,
            num_return_sequences=1,
            do_sample=True  # Random sampling
        )
        
        # Decode and clean up the generated word
        generated_text = tokenizer.decode(output[0], skip_special_tokens=True).strip()
        generated_word = generated_text.replace(input_prompt, "").strip()
        generated_word = generated_word.split()[0] if generated_word else "No word generated"

        # Validate: exclude common words and non-alphabetic outputs
        if generated_word.isalpha() and generated_word.lower() not in COMMON_WORDS.get(language, []):
            return generated_word.capitalize()

    return "Failed to generate a valid word after multiple attempts."

# Translate text to English
from transformers import MarianMTModel, MarianTokenizer
from transformers import AutoTokenizer, AutoModelForCausalLM

# ... (other functions remain the same)

def translate_to_english(text):
    """Translate text to English with additional checks."""
    try:
        if not text or len(text.strip()) == 0:
            return "No valid input to translate"

        inputs = translation_tokenizer(text, return_tensors="pt", padding=True)
        translated = translation_model.generate(**inputs)
        translated_text = translation_tokenizer.decode(translated[0], skip_special_tokens=True)

        # If translation output matches the input, assume no translation occurred
        if translated_text.strip().lower() == text.strip().lower():
            return f"No translation available for '{text}'"

        return translated_text
    except Exception as e:
        return f"Translation error: {str(e)}"

# Main logic
if __name__ == "__main__":
    language = input("Enter a language (French, Spanish, Japanese, Mandarin, German): ").strip().lower()

    try:
        random_word = generate_random_word(language)

        if "Unsupported" in random_word:
            print(random_word)
        else:
            translated_word = translate_to_english(random_word)
            print(f"Generated word in {language.capitalize()}: {random_word}")
            print(f"Translated to English: {translated_word}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")