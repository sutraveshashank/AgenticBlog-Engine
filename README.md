# <a href="https://kalyanm45.github.io/BlogBoard-AI-Blog-Generator/">BlogBoard — Autonomous AI Article Generator</a>




## About The Project

BlogBoard is an end-to-end, fully automated blogging platform. It autonomously schedules, writes, formats, and publishes deep-dive technical articles on Machine Learning and Artificial Intelligence directly to a fast, static frontend website.

Powered by **LangGraph** for stateful workflow execution and **Groq** for blazing-fast LLM inference, it ensures that high-quality, zero-fluff, production-grade articles are generated and deployed automatically via **GitHub Actions**.


##  Key Features

- 🤖 **Multi-Agent Architecture**
  - Tutorial Agent → Generates topics & content  
  - Validator Agent → Reviews and improves output  
  - Storage Layer → Saves generated blogs  

- 🧩 **LangGraph Workflow**
  - Structured agent orchestration using graph-based execution  

- ✍️ **Automated Blog Generation**
  - Generates full-length technical blogs with subtopics  

- 📊 **Dynamic Topic Selection**
  - Avoids repetition using history + prompt engineering  

- 💾 **Local Storage Support**
  - Saves generated blogs locally (R2 optional)

- ⚡ **LLM Integration**
  - Uses Groq API for fast inference  

---

##  Project Architecture

User Input / Trigger  
          ↓    
🧭 Tutorial Agent (Topic Selection)  
          ↓  
✍️ Content Generation  
          ↓  
✔️ Validator Agent (Quality Check)  
          ↓  
💾 Storage (Local / R2)  

---

##  Tech Stack

- **Backend:** Python  
- **LLM Framework:** LangGraph, LangChain  
- **Model Provider:** Groq API  
- **Data Handling:** Pydantic  
- **Storage:** Local / Cloudflare R2 (optional)  



##  Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/sutraveshashank/AgenticBlog-Engine.git
cd blogboard
```

### 2️⃣ Create Virtual Environment <br>
python -m venv myenv
myenv\Scripts\activate  <br>
### 3️⃣ Install Dependencies  <br>
pip install -r requirements.txt <br>

### 4️⃣ Run the Project
python blogboard/run.py
### 5️⃣ View Generated Blogs

Generated blogs will be saved in:

output/   <br>



## Sample Output
- Topic: Explainable AI Techniques <br>
- Generated Blog: ~600+ words <br>
- Includes:  <br>
    -  Structured headings   <br>
    -  Subtopics  <br>
    -  Read time estimation  <br>


## Use Cases
- Automated content generation platforms <br>
- AI blogging tools  <br>
- Knowledge base generation  <br>
- Educational content systems  
