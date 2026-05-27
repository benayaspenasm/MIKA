# Welcome to **MIKA** 🤖✨
### AI-Powered Social Media Post Generator

> Built at the **Generative AI Hackathon 2024** — RAG Challenge  
> *By Miguel Benayas Penas & Skarleth Melissa Motiño Flores — Los Chicos de Madriz*

---

## What is MIKA?

MIKA is an MVP application that automatically generates platform-optimised social media content from real-time news. Give it a topic, pick a platform and tone, and MIKA fetches today's relevant news, processes it through an LLM, and produces ready-to-publish content — whether that's a text post, an AI-generated image, a meme, or even a short video.

This AI-powered social media post generator is capable of creating text, images, memes, and videos. Users can select their preferred platform (LinkedIn, Instagram, X, TikTok, or Facebook) and specify the desired tone.

---

## Features

- 📰 **RAG pipeline** — retrieves live news articles via Google News API and grounds all generated content in real, up-to-date information
- ✍️ **Text posts** — platform-aware copy (LinkedIn, Instagram, X, Facebook, TikTok) with tone control (Formal, Casual, Humorous, Professional)
- 🖼️ **AI image generation** — creates topic-relevant visuals from the article content
- 😂 **Meme generation** — selects the best meme template from a curated library and fills it with LLM-generated captions via Imgflip API
- 🎬 **Video generation** — produces short video content from article summaries
- 🔁 **Post refinement** — allows iterative improvement of generated content with additional context
- 💾 **One-click download** — all generated media (images, memes, videos) are downloadable directly from the app

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend / UI | Streamlit |
| LLM | Groq (Llama) |
| News retrieval | Google News API (RAG layer) |
| Image generation | PIL + external image API |
| Meme generation | Imgflip API |
| Video generation | External video API |
| Language | Python 3 |

---

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/benayaspenasm/MIKA.git
cd MIKA
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. (Optional) Refresh the meme template list
Only needed if `meme_templates.txt` doesn't exist or you want to update it:
```bash
python Retrieve_MemeTemplateList.py
```

### 4. Run the app
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

---

## How to Use

1. Enter a topic or prompt (e.g. *"Write a post about the latest breakthroughs in renewable energy"*)
2. Select your **platform**, **tone**, and **content format**
3. Click **Generate Post**
4. MIKA fetches a relevant news article, processes it, and generates your content
5. Optionally refine the result by adding extra context in the refinement box
6. Download the generated media if needed

---

## Project Structure

```
MIKA/
├── app.py                      # Main Streamlit application
├── functions.py                # Core helper functions (API calls, content generation)
├── Retrieve_MemeTemplateList.py # Script to fetch & cache meme templates
├── meme_templates.txt          # Cached meme template library
├── requirements.txt            # Python dependencies
├── logo.png                    # App logo
└── LICENSE                     # Apache 2.0
```

---

## Roadmap / Future Work

- [ ] API key management via `.env` / Streamlit secrets
- [ ] Support for additional LLM providers
- [ ] Persistent post history
- [ ] Scheduled posting via social media APIs
- [ ] Multi-language support

---

## License

Distributed under the [Apache 2.0 License](LICENSE).

---

## Authors

Built with love and a lot of energy during Hackathon Generative AI 2024.

 **Skarleth Melissa Motiño Flores**  ·  **Miguel Benayas Penas**
