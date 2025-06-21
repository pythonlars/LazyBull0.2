import os
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
import sys
import datetime

# Configuration
IMAGE_PATH = "Screenshot 2025-06-17 120645.png"
OUTPUT_FILE = "output.txt"

def log_and_print(message):
    """Print message to console and append to output file"""
    print(message)
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {message}\n")

def analyze_image_with_gemini(api_key, image_path):
    """Use Google's Gemini API to analyze an image and describe it"""
    try:
        # Configure the generative AI client
        genai.configure(api_key=api_key)
        
        # Try available models if one doesn't work
        models = ["gemini-1.5-flash", "gemini-pro-vision", "gemini-1.0-pro-vision"]
        
        for model_name in models:
            try:
                log_and_print(f"Trying model: {model_name}")
                # Create the model
                model = genai.GenerativeModel(model_name)
                
                # Load the image
                img = Image.open(image_path)
                
                # Generate the prompt
                prompt = """
                You are a professional day trader with over 20 years of experience. You are also knowledgeable about the four stages of the market: Accumulation, Advancing, Distribution, and Declining. Each stage has specific characteristics and trading implications. This framework helps in making educated trading decisions without relying solely on indicators. 

                ## Key Market Stages:

                1.  **Accumulation Stage:**
                    *   **Characteristics:** Market in a range, typically after a downtrend. 200-period Moving Average (MA) flattens out, price chops above and below the 200MA.
                    *   **Trading Implication:** Potential for an uptrend breakout. Look for buying opportunities on retests of support or false breakouts.

                2.  **Advancing Stage (Uptrend):**
                    *   **Characteristics:** Market breaks out of accumulation, forming a series of higher highs and higher lows.
                    *   **Trading Implication:** Avoid shorting. Look for buying opportunities, e.g., at support/resistance levels, trendlines, or moving averages (like the 50 MA).

                3.  **Distribution Stage:**
                    *   **Characteristics:** Market enters a range during an uptrend. Traders take profits, sellers enter the market.
                    *   **Trading Implication:** Potential for a downtrend breakout.

                4.  **Declining Stage (Downtrend):**
                    *   **Characteristics:** Market breaks down from distribution, forming a series of lower highs and lower lows.
                    *   **Trading Implication:** Avoid buying (unless an investor). Look for shorting opportunities, e.g., at resistance levels, trendlines, or bearish flag patterns.

                Analyze the uploaded stock chart image using advanced technical analysis, incorporating the understanding of these four market stages.

                Your task:

                Identify all visible patterns, including:

                Candlestick formations (e.g. Doji, Engulfing, Hammer)

                Chart patterns (e.g. Head and Shoulders, Triangles, Flags, Double Tops/Bottoms)

                Trendlines, moving averages, volume changes

                Support/resistance levels, indicator signals (RSI, MACD, EMA/SMA if visible)

                For each identified pattern, output:

                Pattern name

                What it indicates (bullish/bearish/neutral)

                One-line explanation

                Based only on the image data, give a short-term price prediction:

                Direction: UP, DOWN, or STABLE

                Time frame until move completes: e.g. 15 min, 1 hour, 2 hours, 1 day, etc.

                Confidence level: percentage estimate (e.g. 80%) based on historical accuracy of detected patterns and clarity of signals

                Format your output exactly like this:

                yaml
                Kopieren
                Bearbeiten
                Patterns:
                - Bullish Flag → Bullish → Price consolidating before breakout
                - Rising Volume → Bullish → Increasing buying pressure during flag
                - RSI ~70 → Neutral → No clear divergence

                Prediction: UP  
                Time Frame: 1–2 hours  
                Confidence: 78%  
                Reason: Bullish continuation pattern with rising volume and strong trend support suggests near-term breakout likely.
                Do not speculate beyond what's visible. No filler. No assumptions. Be concise, professional, and data-driven."""
                
                # Generate content with the image
                response = model.generate_content([prompt, img])
                
                # If we got here without an exception, we have a successful response
                log_and_print(f"Success with model: {model_name}")
                return response.text
                
            except Exception as model_error:
                log_and_print(f"Error with model {model_name}: {str(model_error)}")
                # Continue to the next model if this one fails
        
        # If we've tried all models and none worked
        return "Error: All models failed to analyze the image."
        
    except Exception as e:
        log_and_print(f"Unexpected error in analyze_image: {str(e)}")
        return f"Error: {str(e)}"

def main():
    """Main function to load environment variables, check image and analyze it"""
    # Clear the output file at the start
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("")
        
    log_and_print("=== Image Analysis with Google Gemini ===\n")
    
    # Load environment variables
    log_and_print("Loading environment variables...")
    load_dotenv()
    
    # Get API key from environment
    api_key = os.getenv("GOOGLE_API_KEY")
    
    # Check if API key exists
    if not api_key:
        log_and_print("Error: Google API key not found.")
        log_and_print("Please set GOOGLE_API_KEY in your .env file.")
        return False
    else:
        log_and_print("API key loaded successfully.")
    
    # Check if image exists
    if not os.path.exists(IMAGE_PATH):
        log_and_print(f"Error: Image not found at path: {IMAGE_PATH}")
        return False
    else:
        log_and_print(f"Image found: {IMAGE_PATH}")
    
    # Analyze the image
    log_and_print("\nAnalyzing image...")
    description = analyze_image_with_gemini(api_key, IMAGE_PATH)
    
    # Print the results with clearer formatting
    log_and_print("\n" + "="*50)
    log_and_print("GEMINI AI RESPONSE - DIRECT OUTPUT:")
    log_and_print("="*50)
    log_and_print(f"{description}")
    log_and_print("="*50)
    
    # Save the raw AI output to a separate file for easy access
    raw_output_file = "ai_response.txt"
    with open(raw_output_file, "w", encoding="utf-8") as f:
        f.write(description)
    
    log_and_print(f"\nComplete logs have been saved to: {OUTPUT_FILE}")
    log_and_print(f"Raw AI response has been saved to: {raw_output_file}")
    
    return True

# Execute main function
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log_and_print(f"An unexpected error occurred: {e}")
        sys.exit(1)