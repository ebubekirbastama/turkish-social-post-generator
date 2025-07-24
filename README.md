# Social Media Post Generator for Turkish News

An intelligent application that automatically generates optimized social media posts from Turkish news content using NLP techniques.

## Features

- Automatic hashtag generation (#Beykoz, #Gündem, etc.)
- Named Entity Recognition for organizations/persons
- YAKE! keyword extraction for relevant tags
- Professional post template with consistent formatting
- One-click copy functionality
- Modern Windows 11 style UI

## Installation

1. Clone the repository:
git clone https://github.com/ebubekirbastama/social-media-post-generator.git
cd social-media-post-generator

2. Install dependencies:
pip install -r requirements.txt

3. Download Turkish NLP model:
python -c "import stanza; stanza.download('tr')"

## Usage

python post_generator.py

Input Format Example:
#SonDakika Beykoz Belediyesi yeni park projesini açıkladı: https://ornek.com/haber

Output Example:
🔥 #SonDakika | Beykoz Belediyesi:
📝 "Yeni park projesini açıkladı"

🌲 Detaylar ve gelişmeler için:
👉 https://ornek.com/haber

🔖 Hashtagler: #Beykoz #Gündem #İstanbulHaber #YerelHaber #SonDakika #BeykozBelediyesi #ParkProjesi

## Technologies Used

- NLP Processing:
  - Stanza (Turkish NER)
  - YAKE! (Keyword extraction)
  
- GUI:
  - Tkinter (Modern Windows 11 style)
  - ttk widgets

- Core:
  - Python 3.7+
  - Regular Expressions

## Contributing

Contributions are welcome! Please open an issue or submit a PR for any:
- Bug fixes
- Feature requests
- Documentation improvements



Made with ❤️ in Turkey
