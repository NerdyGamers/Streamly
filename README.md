<h1><span style="color: crimson;">ServUO Assistant</span> <img src="imgs/slogo.png" alt="ServUO logo" width="50" style="border-radius: 25px;"/></h1>

<p align="center">
  <img src="imgs/streamly_readme.png" alt="Streamly image" width="300" style="border-radius: 45px;"/>
</p>

ServUO Assistant is an AI companion built to support ServUO shard administrators and Ultima Online players. It offers on-the-fly assistance 🚀, script snippets ✂️, and the latest news from the ServUO and Ultima Online communities. 🧪

## Dynamic Features:

- Interactive Chat Interface 💬: Ask anything from simple how-tos to complex ServUO questions. The assistant understands context and responds with pertinent information, making the interaction both enriching and delightful.

- Script Snippet Wizardry 🧙‍♂️: The assistant conjures up ready-to-use ServUO script snippets. This magic helps both newcomers and seasoned shard admins speed up their development.

- Update Oracle 📜: Always in the loop, the assistant taps into the latest happenings of the ServUO and Ultima Online worlds. Whether it's a fresh publish or a minor tweak, it's your go-to source for the most recent and relevant information.

- A Personal Touch 🎨: Decked out with custom CSS and the potential for further personalization, the assistant's UI/UX shines, offering a user experience that's both engaging and aesthetically pleasing.

## Insightful Logic and Capabilities:

At the heart of the assistant lies a sophisticated AI engine 🤖, trained on a plethora of data, including the vast expanses of Streamlit's documentation, forums, and community contributions. This training enables it to understand context, maintain conversational flow, and provide accurate, context-aware advice.

The assistant's backend is a creative use of session state management, providing it with a memory, making for a consistent and coherent conversation for all your coding assistances 🧠.

With Streamlit's caching mechanisms under the hood for performance optimization, and a comprehensive error handling protocol 🛠️, the assistant ensures a smooth sail through the sometimes choppy waters of coding challenges.

The assistant embraces the future with open arms, designed to be extensible and modular. The integration of LangChain adds for a fuller and seamless conversational experience, making it not just an assistant but a developer's companion 🤝.

In the vibrant world of ServUO development, the assistant shines as a beacon of innovation and practicality. It's not just an AI assistant; it's a testament to the harmonious blend of human creativity and artificial intelligence, all wrapped up in a user-friendly package 🎁. Whether you're a novice coder or a seasoned developer, the ServUO Assistant is here to light up your coding journey with a spark of AI brilliance ✨.

## Setup Instructions

To get the ServUO Assistant up and running on your local machine, follow these steps:

### Prerequisites

- Python 3.10 or higher
- Pip package manager

### API Keys

Use secrets.toml an add your OpenAI API key or set your enviroment variable OPENAI_API_KEY to your API key.

### Installation

1. Clone the repository:

```bash
git clone https://github.com/AdieLaine/Streamly.git
cd streamly
```

2. Create and activate a virtual environment (optional but recommended):
```bash
python3 -m venv venv
source venv/bin/activate # On Windows use venv\Scripts\activate
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

### Running the Application

To run the ServUO Assistant, execute the following command:

```bash
streamlit run servuo_assistant.py
```

This will start the Streamlit server, and you should see output indicating the local URL where the app is being served, typically `http://localhost:8501`.

## Using the ServUO Assistant

After launching the assistant, you can interact with it in the following ways:

- **Chat Interface**: Type your ServUO or Ultima Online questions into the chat interface and hit send. The assistant will respond with insights, script snippets, or guidance based on your questions.

- **Script Examples**: Ask for script examples by typing queries such as "How do I create a custom item?" and the assistant will provide you with relevant code.

- **Latest Updates**: To get the latest updates from ServUO or Ultima Online, type "What's new with ServUO?" or similar questions.

Remember to check the sidebar for additional features and settings that you can customize according to your needs.

## Contributions

If you'd like to contribute, please fork the repository and create a pull request with your features or fixes.

## License

ServUO Assistant is released under the [MIT License](LICENSE). See the `LICENSE` file for more details.
