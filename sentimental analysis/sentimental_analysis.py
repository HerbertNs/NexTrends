#14TH APRIL 4:51 PM

""" In case the code doesnt work for you remove the comment to download the files.
They're kept here just in case.

The regex patterns used will be updated to use data files for more patterns."""

#import nltk
#nltk.download('vader_lexicon')
#nltk.download('punkt')
#nltk.download('wordnet')

from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re
from spellchecker import SpellChecker

spell = SpellChecker()

sentiment_analyzer = SentimentIntensityAnalyzer()

# Contextual emotion patterns.
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

# YouTube-specific patterns
youtube_contextual_patterns = {
    "clickbait": [
        r"(?:you won't believe|shocking|amazing|incredible|unbelievable|must see|watch this|going viral)",
        r"(?:top \d+|best \d+|worst \d+|most \d+)",
        r"(?:before you die|life changing|mind blowing|game changing)",
        r"(?:exposed|revealed|truth about|secret of|they don't want you to know)",
        r"(?:never seen before|first look|exclusive|leaked|unveiled)",
        r"(?:must watch|must see|must see this|must see this video|must see this video)",
    ],
    "educational": [
        r"(?:how to|tutorial|guide|step by step|explained|tips and tricks|learn|master)",
        r"(?:beginner's guide|advanced techniques|complete guide|ultimate guide)",
        r"(?:what is|why does|how does|understanding|basics of|what makes|what's|what are|what's the|what is the)",
        r"(?:learn about|explore|discover|understand|study|investigate|research|explore|learn from)",
        r"(?:mastering|advanced|proficiency|skill|knowledge|understanding|explanation|explanation|explanation)",
    ],
    "entertainment": [
        r"(?:funny|hilarious|comedy|prank|challenge|react to|try not to laugh)",
        r"(?:epic fails|best moments|highlight reel|compilation|montage)",
        r"(?:storytime|my experience|what happened|behind the scenes|upcoming|films|movie)"
    ]
}

# Enhanced YouTube category patterns
youtube_category_patterns = {
    "Film_and_Animation": r"(?:film|movie|animation|cinema|director|actor|actress|scene|shot|trailer|review)",
    "Autos_and_Vehicles": r"(?:car|truck|motorcycle|vehicle|auto|driving|race|engine|modification|review|test drive)",
    "Music": r"(?:song|music|album|artist|band|concert|performance|lyrics|instrument|dj|remix|cover|playlist)",
    "Pets_and_Animals": r"(?:pet|dog|cat|animal|wildlife|nature|zoo|veterinary|training|care|rescue|adoption)",
    "Sports": r"(?:sport|football|basketball|baseball|tennis|golf|olympics|training|match|game|highlight|analysis)",
    "Travel_and_Events": r"(?:travel|trip|vacation|destination|event|festival|tour|adventure|explore|vlog|guide)",
    "Gaming": r"(?:game|gaming|playthrough|walkthrough|review|stream|esports|console|pc|mobile|mod|cheat|tips)",
    "News_and_Politics": r"(?:news|politics|current events|election|government|policy|debate|analysis|breaking news)",
    "How_to_and_Style": r"(?:how to|tutorial|guide|tips|tricks|style|fashion|makeup|hairstyle|DIY|craft|design)",
    "Education": r"(?:education|learning|school|university|course|lecture|study|knowledge|skill|tutorial|explanation)",
    "Science_and_Technology": r"(?:science|technology|tech|innovation|research|discovery|invention|future|AI|machine learning)",
    "Nonprofits_and_Activism": r"(?:nonprofit|charity|activism|cause|fundraising|awareness|social justice|volunteer|donate)",
    "Comedy": r"(?:comedy|funny|joke|humor|standup|skit|parody|satire|prank|laugh|roast|meme)",
    "Entertainment": r"(?:entertainment|show|performance|variety|reality|talent|competition|award|celebrity|gossip)",
    "Anime_and_Animation": r"(?:anime|animation|manga|cartoon|character|story|episode|series|otaku|cosplay|review|oc)",
    "Action_and_Adventure": r"(?:action|adventure|thrill|excitement|danger|quest|mission|exploration|survival|challenge)",
    "Documentary": r"(?:documentary|factual|real story|investigation|expose|report|truth|reality|history|biography)",
    "Family": r"(?:family|children|parenting|kids|home|relationship|bonding|generation|activities|fun|education)",
    "Horror": r"(?:horror|scary|frightening|terrifying|creepy|monster|ghost|haunted|paranormal|thriller|suspense)",
    "Sci_Fi_and_Fantasy": r"(?:sci-fi|science fiction|fantasy|futuristic|space|alien|robot|magic|superhero|dystopia)",
    "Shorts": r"(?:short|quick|brief|mini|snapshot|moment|clip|highlight|reel|story|idea|tip|trick)",
    "Thriller": r"(?:thriller|mystery|horror|suspense|surreal|dark|psychological|psychological thriller|murder|crime|detective)",
    "Programming": r"(?:python|java|c\+\+|javascript|typescript|ruby|php|go|rust|kotlin|swift|programming|coding|developer|software|algorithm|data structure|debug|api|framework|library|package|module)",
    "Web_Development": r"(?:html|css|javascript|react|angular|vue|node|express|django|flask|laravel|web development|frontend|backend|full stack|responsive design|web app|website|web service|api|rest|graphql)",
    "Data_Science": r"(?:data science|machine learning|artificial intelligence|ai|ml|deep learning|neural network|data analysis|data visualization|pandas|numpy|tensorflow|pytorch|keras|scikit-learn|jupyter|notebook|data mining|big data|data engineering)",
    "DevOps": r"(?:devops|docker|kubernetes|ci/cd|continuous integration|continuous deployment|jenkins|gitlab|github actions|terraform|ansible|puppet|chef|infrastructure as code|cloud computing|aws|azure|google cloud|gcp|serverless|microservices)",
    "Mobile_Development": r"(?:android|ios|flutter|react native|swift|kotlin|mobile development|mobile app|cross platform|native app|hybrid app|app development|app store|play store|mobile ui|mobile ux|mobile design)",
    "Game_Development": r"(?:game development|unity|unreal engine|godot|cryengine|game design|game programming|game engine|3d modeling|2d animation|game physics|game ai|vr|ar|virtual reality|augmented reality|game assets|game art)",
    "3D_Modeling": r"(?:3d modeling|3d design|3d art|3d animation|blender|maya|3ds max|zbrush|cinema 4d|houdini|substance painter|texturing|uv mapping|rigging|character modeling|environment modeling|hard surface modeling|sculpting|digital sculpting|3d printing|3d rendering|vfx|visual effects)"
}

# Add to calculate_emotion_scores function
def calculate_emotion_scores(text, compound_score):
    # Initialize emotion scores
    emotion_scores = {
        "happy": 0,
        "sad": 0,
        "angry": 0,
        "fear": 0,
        "neutral": 0.2,
        "clickbait": 0,
        "educational": 0,
        "entertainment": 0
    }
    
    # Check for YouTube-specific patterns
    for category, patterns in youtube_contextual_patterns.items():
        for pattern in patterns:
            if re.search(pattern, text):
                emotion_scores[category] += 0.5  # Higher boost for YouTube patterns
    
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
    
    # Contextual word weighting
    weighted_words = {
        "love": {"happy": 0.5},
        "hate": {"angry": 0.5, "sad": 0.3},
        "terrified": {"fear": 0.6},
        "ecstatic": {"happy": 0.7},
        "devastated": {"sad": 0.8}
    }
    
    for word, emotions in weighted_words.items():
        if word in text:
            for emotion, weight in emotions.items():
                emotion_scores[emotion] += weight
                
    return emotion_scores

def predict_category(text):
    """Predict the YouTube category based on the text using a scoring system."""
    text = text.lower()
    category_scores = {category: 0 for category in youtube_category_patterns.keys()}
    
    # Score each category based on pattern matches
    for category, pattern in youtube_category_patterns.items():
        matches = re.findall(pattern, text)
        category_scores[category] += len(matches) 
    
    # Normalize scores
    total_matches = sum(category_scores.values())
    if total_matches > 0:
        for category in category_scores:
            category_scores[category] /= total_matches
    
    # Return the category with the highest score
    if max(category_scores.values()) > 0:
        return max(category_scores, key=category_scores.get)
    return "Unknown"

# Add to detect_emotion function
def detect_emotion(text):
    # Convert to lowercase for consistent processing
    text = text.lower()
    
    # Get VADER sentiment scores
    sentiment_scores = sentiment_analyzer.polarity_scores(text)
    compound_score = sentiment_scores['compound']
    
    emotion_scores = calculate_emotion_scores(text, compound_score)
    
    predicted_category = predict_category(text)
    if predicted_category != "Unknown":
        # Count matches instead of summing strings
        category_score = len(re.findall(youtube_category_patterns[predicted_category], text))
        if category_score > 0:
            if predicted_category in ["Comedy", "Entertainment"]:
                emotion_scores["happy"] += 0.2 * category_score
            elif predicted_category in ["News_and_Politics", "Documentary"]:
                emotion_scores["neutral"] += 0.1 * category_score
            elif predicted_category in ["Horror", "Action_and_Adventure"]:
                emotion_scores["fear"] += 0.15 * category_score
    
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
    
    # Intensity modifiers
    intensity_modifiers = {
        "very": 0.3,
        "really": 0.3,
        "extremely": 0.4,
        "absolutely": 0.4,
        "totally": 0.3,
        "completely": 0.3
    }
    
    for modifier, boost in intensity_modifiers.items():
        if modifier in text:
            # Apply boost to the dominant emotion
            non_neutral = {k: v for k, v in emotion_scores.items() if k != "neutral"}
            if non_neutral:
                max_emotion = max(non_neutral, key=non_neutral.get)
                emotion_scores[max_emotion] += boost
                
    dominant_emotion = max(emotion_scores, key=emotion_scores.get)
    
    # Calculate intensity (0-1 scale)
    intensity = emotion_scores[dominant_emotion]
    
    # If no strong emotion is detected, then it defaults to neutral.
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

def correct_text(text):
    words = re.findall(r'\w+|\W+', text)
    
    # Correcting each word, not highly efficient.
    corrected_words = []
    for word in words:
        if word.strip() and word[0].isalpha():  # Only correct alphabetic words
            corrected_word = spell.correction(word)
            corrected_words.append(corrected_word if corrected_word else word)
        else:
            corrected_words.append(word)  # Keep punctuation and numbers

    return ''.join(corrected_words)

if __name__ == "__main__":
    #TRY IT OUT HERE.
    input_text = """ Why i love to play on bedrock edition minecraft"""
    
    # Correct the text before analysis
    corrected_text = correct_text(input_text)
    print(f"Original Text: {input_text}")
    print(f"Corrected Text: {corrected_text}")
    
    # Analyze emotion and predict category
    emotion, intensity = analyze_emotion(corrected_text)
    category = predict_category(corrected_text)
    
    print(f"\nDetected Emotion: {emotion}")
    print(f"Emotional Intensity: {intensity:.2f}")
    print(f"Predicted Category: {category}")