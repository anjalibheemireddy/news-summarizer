# 📘 News Summarizer Chat

A simple web-based news summarization tool built with Streamlit, LangGraph, OpenAI, and Tavily Search.

The app lets users ask any news-related question.


## Workflow:

- Takes the user query

- Uses Tavily Search API to fetch relevant articles

- Generates a raw answer

- Uses GPT-4o-mini to produce a clean, well-structured final summary

- Returns the answer + source links

---

## 🛠️ Project Structure
project/
│
├── nodes1.py          # LangGraph workflow (search → answer → format → JSON)
├── streamlit_app.py   # Streamlit UI (chat interface)
├── .env               # API keys
├── README.md



## Installation

1. **Clone the repository**
```bash
git clone <repository_url>

```

2. **Create virtual environment**
```bash
conda create -p venv python=3.12 -y
```
(Any other method to create a Python environment can also be used.)

3. **Activate environment**
```bash
conda activate ./venv
```
4. 🔑 Environment Variables

Create a .env file:

```bash
OPENAI_API_KEY=your_openai_key_here
TAVILY_API_KEY=your_tavily_key_here
```


5. 📦 Install Dependencies

Run:

```bash
pip install -r requirements.txt

```

(Plus any missing packages your environment asks for.)

6. Start Streamlit  
```bash

streamlit run app.py
```


You can now start chatting.

## 🧠 How It Works
### nodes.py (Workflow)

The workflow has 4 nodes:

- Search

- Calls Tavily search

- Fetches up to 3 results with Tavily’s answer

- Generate Answer

- Cleans and formats the search answer

- Adds source URLs

- Format Answer

- Uses GPT-4o-mini for a high-quality final summary

- JSON Output

- Packages summary + structured sources

### streamlit_app.py (UI)

- Displays chat messages

- Sends each query to the agent (agent.invoke)

- Shows a formatted answer with sources

## 💬 Usage Example

Ask:

"What happened in Delhi blast?"

- The app will return a structured multi-paragraph summary plus:

Sources:
- Al Jazeera: https://....
- Economic Times: https://....
- YouTube: https://....

## 🧩 Notes

- Each question is treated independently.

- Works only with valid OpenAI + Tavily API keys.

- Streamlit directly calls the LangGraph agent (no FastAPI required).

## License

This project is licensed under the terms included in the LICENSE file.


## Author

**Anjali Bheemireddy**  
(anjalinature156@gmail.com)
