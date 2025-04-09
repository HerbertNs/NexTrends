#9TH APRIL 4:51 PM

from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re

# Initialize VADER sentiment analyzer
sentiment_analyzer = SentimentIntensityAnalyzer()

""" In case the code doesnt work for you remove the comment to download the files.
They're kept here just in case."""

#import nltk
#nltk.download('vader_lexicon')
#nltk.download('punkt')
#nltk.download('wordnet')

# Contextual emotion patterns. This is just from an old bot. They will be optimized with better keywords soon
contextual_patterns = {
    "sad": [
        r"(?:i|me|my|we).*(?:sad|depress|down|upset|hurt|cry|tears|alone|lonely|miss|lost|glum)",
        r"(?:i|me).*(?:want to|wanna) (?:die|disappear|end it|give up)",
        r"(?:i|me).*(?:no|don't|won't|can't).*(?:happy|joy|hope)",
        r"(?:i|me).*(?:tired of|sick of|hate) (?:life|living|myself|everything)",
        r"(?:nothing|no one).*(?:matters|cares|loves)",
        r"(?:i'll|i will) be (?:happy|better|fine) when (?:i|me|we) (?:don't|do not|no longer) exist"
        r"(?:i|me|my).*(?:heartbroken|broken heart|devastated|grieving|mourning)",
        r"(?:i|me).*(?:can't stop|crying all|tears streaming)",
        r"(?:i|me).*(?:feel|am) (?:empty|numb|hopeless|worthless)",
        r"(?:i|me).*(?:regret|wish i hadn't|shouldn't have)",
        r"(?:i|me).*(?:lost my|death of|passed away|no longer with us)"
    ],
    "happy": [
        r"(?:i|me|my|we).*(?:happy|joy|excite|love|great|awesome|amazing)",
        r"(?:i|me).*(?:can't wait|excited|looking forward)",
        r"(?:this|that) (?:is|was) (?:great|amazing|wonderful|fantastic)",
        r"(?:i|me).*(?:love|enjoy|appreciate)",
        r"(?:thank|thanks|thx|miss you|aw)"
    ],
    "angry": [
        r"(?:i|me|my|we).*(?:angry|mad|furious|hate|pissed|annoyed)",
        r"(?:i|me).*(?:can't stand|sick of|tired of|fed up)",
        r"(?:this|that|you|they).*(?:stupid|idiot|dumb|moron|ridiculous|destroyed)",
        r"(?:fuck|shit|damn|screw|hell)",
        r"(?:i|me).*(?:kill|punch|slap|hit)"
    ],
    "fear": [
        r"(?:i|me|my|we).*(?:scared|afraid|terrified|worried|anxious|nervous|anxiety|scared)",
        r"(?:i|me).*(?:don't know what|uncertain|unsure|weird)",
        r"(?:what if|oh no|oh god|oh)",
        r"(?:i|me).*(?:panic|stress|worry)",
        r"(?:help|please help|save me)"
    ],
        "neutral": [
        r"(?:i|me).*(?:don't care|not bothered|whatever|meh)",
        r"(?:just saying|for your information|fyi|as a matter of fact)",
        r"(?:this is|that is) (?:okay|fine|acceptable|reasonable)",
        r"(?:i|me).*(?:neither happy nor sad|not emotional|indifferent)",
        r"(?:i|me).*(?:just wondering|curious about|asking about)"
    ]
}

def detect_emotion(text):
    # Convert to lowercase for consistent processing since some people like typing in caps.
    text = text.lower()
    
    # Get VADER sentiment scores
    sentiment_scores = sentiment_analyzer.polarity_scores(text)
    compound_score = sentiment_scores['compound']  # Overall sentiment (-1 to 1)
    
    # Initialize emotion scores
    emotion_scores = {
        "happy": 0,
        "sad": 0,
        "angry": 0,
        "fear": 0,
        "neutral": 0.2  # Small baseline for neutral
    }
    
    # Check for contextual patterns
    for emotion, patterns in contextual_patterns.items():
        for pattern in patterns:
            if re.search(pattern, text):
                emotion_scores[emotion] += 0.4  # Significant boost for matching patterns
    
    # Adjust based on VADER sentiment
    if compound_score >= 0.3:
        emotion_scores["happy"] += 0.3 * compound_score
    elif compound_score <= -0.3:
        # Distribute negative sentiment between sad and angry
        if "!" in text or any(word in text for word in ["hate", "angry", "mad", "fuck", "shit"]):
            emotion_scores["angry"] += 0.4 * abs(compound_score)
        else:
            emotion_scores["sad"] += 0.4 * abs(compound_score)
    
    # Check for question marks (uncertainty/fear). Either its something neutral or weird.
    if "?" in text:
        emotion_scores["fear"] += 0.2
    
    # Check for exclamation marks for intensity.
    exclamation_count = text.count("!")
    if exclamation_count > 0:
        intensity_boost = min(0.3, exclamation_count * 0.1)
        # Apply to the highest non-neutral emotion.
        non_neutral = {k: v for k, v in emotion_scores.items() if k != "neutral"}
        if non_neutral:
            max_emotion = max(non_neutral, key=non_neutral.get)
            emotion_scores[max_emotion] += intensity_boost
    
    dominant_emotion = max(emotion_scores, key=emotion_scores.get)
    
    # Calculate intensity (0-1 scale)
    intensity = emotion_scores[dominant_emotion]
    
    # If no strong emotion is detected, then itdefault to neutral.
    if intensity < 0.4:
        dominant_emotion = "neutral"
        intensity = 0.3
    
    return dominant_emotion, min(1.0, intensity)  # Cap intensity at 1.0

def analyze_emotion(text_input):
    """
    Main function to analyze the emotion of input text.
    Returns a tuple of (emotion_category, intensity)
    """
    emotion_category, emotional_intensity = detect_emotion(text_input)
    return emotion_category, emotional_intensity

if __name__ == "__main__":
    #TRY IT OUT HERE.
    input_text = "i hate everyone"
    emotion, intensity = analyze_emotion(input_text)
    print(f"Detected Emotion: {emotion}")
    print(f"Emotional Intensity: {intensity:.2f}")