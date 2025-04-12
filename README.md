# 🕸️ Arachnaradio

**Arachnaradio** is a Python-based tool for capturing, identifying, and archiving content from live radio streams. It’s designed to help listeners rediscover the serendipity of real radio, while surfacing songs and interviews that align with their personal taste.

---

## 🧠 Inspiration

This project was inspired by a serendipitous moment I had while listening to KALX Berkeley in my car on my way home from work, where I happened to catch the tail end of a live interview with folk legend Bridget St. John. While tuned to 90.7FM and stuck in 580 traffic on this fateful day, I was actually leaving work early due to illness, so I was not listening during my typical timeframe. After texting a friend about the St. John interview that was airing live, I wondered, *"How many interviews with my favorite artists am I missing because I simply didn't know they were happening?"* Rhetorical question-- the answer is of course: a lot!

This lead me to want to develop an app that would ...
1. :radio:  **Connect people to their local radiostations based on their own personal music taste profile**

    I love my local radio stations here in the Bay. In the era of streaming services a la Spotify and Apple Music, bonafide radio stations are at risk of falling to the wayside. At the same time, I do believe that many people would be willing and excited to find new music on their local radio stations if they knew *how* to find a station that matches their taste. Therein lies the grounds for Goal #1 of Arachnaradio: Take a user's existing music taste data (last.fm, spotify, apple music, etc.) and suggest local radio stations customized to the user's interests.

2. 🕷️ **Provide realtime notifications when a favorite artist is mentioned on air:**

   During non-music segments of a radio broadcast, Arachnaradio will be listening quietly for mentions of a user's favorite artists by name... Once an artist mention is caught in its web, a notification will go out to the user, categorizing the mention as either a) a live interview airing on channel XY.Z FM, b) information about local live shows with that artist, or c) something else that doesn't fit those two criteria! Tentatively, this feature is to be called a ⚡ *tingle* 🕸️ (yes I am leaning heavily into the spider imagery here. Let me have fun.)

3. 🧵 **Transcribe live artist interviews to create a cultural archive for fans, journalists, and music historians of the future:**

   This is the most ambitious aspect that will be implemented, but also the most important. Especially for smaller radio stations and indie artists, interviews are often lost to time. Creating a cumulative archive of artist interviews will require AI transcription of interviews following live detection of an artist's name on air, as well as an efficient way to store these transcripts so that they may be accessed by anyone. 

--- 

## 🎯 Current Project Milestones

- [x] Stream and save live radio audio (KALX)
- [x] Identify music clips via audio recognition (ACRCloud or AudD)
- [x] Transcribe speech using Whisper
- [ ] Detect mentions of artists from user's listening history
- [ ] Notify or log when relevant content is detected
- [ ] Clean up clips after parsing to manage storage

---

## 🚀 How to Run

1. Clone the repo and create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Start capturing radio clips:
    ```bash
    python arachnaradio/stream_capture_to_recog.py
    ```
3. 

---
## 🛠️ Dependencies
ffmpeg (must be installed system-wide)

Python packages:

    pydub

    requests

    python-dotenv

See requirements.txt for a full list.

---

## 💭 Ideas / Future Features
- [x] Log song IDs
- [x] Log artist mentions from a user provided list
- [x] Log venue mentions from a user provided list
- [x] Map venue mentions on dashboard
- [ ] Compare identified songs to user’s Spotify profile
- [ ] Trigger push/email/desktop notifications for matches
- [ ] Web dashboard for browsing matches and logs
- [ ] Archive and index interviews with full transcripts
- [ ] “Trending artists by song appearance on radio station X"
- [ ] "Sift" feature to check out radiostation stats/songs
- [ ] On the sift idea -- scrollable up-down thing for more/less obscure
- [ ] station: Most frequently played artists
- [ ] station: Venues most often mentioned

