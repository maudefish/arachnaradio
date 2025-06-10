from rapidfuzz import fuzz, process

# Example input strings
venue_name = "Bottom Hill tonight"
# transcript_fragment = " how about some tickets ive got two tickets to go see brontes purnell with black bibles and acid barbie over at the stork club 2330 telegraph avenue in oakland this is happening tuesday april 29th just a few days from now at 8 oclock pm its 21 and up it is wheelchair accessible if you and a friend would like to go to this show give me a call 510642calex 5106425259 ill give him the caller number two once again brontes purnell black bibles and acid barbie caller two two tickets for you okay were going to start off my show here with something new from annadol and mary klok marie klok right here on your kalx berkeley"
transcript_fragment = "Bottom Hill"

# Normalize if needed (optional)
def normalize(text):
    return text.lower().strip()

# Fuzzy match score
score = fuzz.WRatio(normalize(venue_name), normalize(transcript_fragment))
score = fuzz.WRatio(venue_name, transcript_fragment)

print(score)
# print(f"Fuzzy match score: {score}")
choices = [
    "Bottom of the Hill", "Rickshaw Stop", "Stork Club", "Thee Stork Club",
    "DNA Lounge", "Regency Ballroom", "Knockout"
]


for c in choices:
    score = fuzz.WRatio(normalize(c), normalize(transcript_fragment))
    print(f"Fuzzy match of {c} score: {score}")


match, score, _ = process.extractOne(
    normalize(transcript_fragment),
    [normalize(c) for c in choices],
    scorer=fuzz.WRatio
)

print(f"Best match: {match} (score: {score})")
