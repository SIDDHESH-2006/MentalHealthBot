def get_suggestions(emotion: str):
    data = {
        "sad": ["Try this affirmation", "Listen to relaxing piano"],
        "happy": ["Celebrate with music!", "Take a photo and reflect"],
        "angry": ["Deep breathing exercise", "Go for a walk"],
        "neutral": ["Write 3 good things", "Focus on gratitude"],
    }
    return data.get(emotion.lower(), ["Check in with yourself."])
