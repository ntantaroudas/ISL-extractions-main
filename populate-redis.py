import json
import os
import redis

# Connect to Redis (adjust host/port as needed)
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Loop over all files in the landmarks directory
# The file name is the word and the content is the hand positions
# We'll store these in Redis
for filename in os.listdir("landmarks"):
    # Extract the word from the filename (without the .json extension)
    word = filename.split(".")[0]
    with open(f"landmarks/{filename}", "r") as f:
        hand_positions = json.load(f)
        # Store the hand positions in Redis
        r.set(word.lower(), json.dumps(hand_positions))
        print(f"Stored mapping for: {word}")

print("All mappings have been loaded into Redis.")
