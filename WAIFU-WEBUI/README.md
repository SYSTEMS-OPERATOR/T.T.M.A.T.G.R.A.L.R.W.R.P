# Waifu Web UI

A Gradio web UI for Low Res Waifu Models.

Our mission is to become the go-to platform for interacting with AI-generated waifu characters, inspired by manga and anime series.

|![Waifu1](https://github.com/YourRepo/screenshots/raw/main/waifu_instruct.png) | ![Waifu2](https://github.com/YourRepo/screenshots/raw/main/waifu_chat.png) |
|:---:|:---:|
|![Waifu3](https://github.com/YourRepo/screenshots/raw/main/waifu_default.png) | ![Waifu4](https://github.com/YourRepo/screenshots/raw/main/waifu_parameters.png) |

## Features

* 3 interface modes: default (two columns), notebook, and chat - all waifu-themed.
* Manga OCR and Anime Subtitle extraction pipeline integration.
* Chat with AI-generated waifu characters based on series content.
* Customizable waifu character generation with LoRA training on extracted data.
* Integrated with a variety of manga and anime databases for character information and context.
* Fun and engaging cat picture requirement for all contributions (meow! 🐱).

## How to install

1) Clone or [download](https://github.com/YourRepo/waifu-webui/archive/refs/heads/main.zip) the repository.
2) Run the appropriate start script (`start_linux.sh`, `start_windows.bat`, etc.) for your OS.
3) Choose your GPU vendor when prompted.
4) After installation, visit `http://localhost:7860/?__theme=dark`.
5) Begin your waifu interactions!

Check out our [wiki](https://github.com/YourRepo/waifu-webui/wiki) for detailed setup instructions and manual installation options.

## Documentation

Our comprehensive documentation is available [here](https://github.com/YourRepo/waifu-webui/wiki).

## Downloading Waifu Models

Place the waifu models in the folder `waifu-webui/models`. They can be sourced from various manga/anime character databases or created using the provided pipeline.

Example of model directory structure:

```
waifu-webui
├── models
│   ├── low-res-waifu
│   │   ├── config.json
│   │   ├── pytorch_model.bin
│   │   └── tokenizer.json
```

## Google Colab notebook

Access our interactive Colab notebook [here](https://colab.research.google.com/github/YourRepo/waifu-webui/blob/main/Colab-WaifuGen-GPU.ipynb).

## Contributing

Join our fun and innovative project! For contributing guidelines, visit [here](https://github.com/YourRepo/waifu-webui/wiki/Contributing-guidelines). Don't forget your cat pictures!

## Community

* Subreddit: [r/YourWaifuProject](https://www.reddit.com/r/YourWaifuProject/)
* Discord: [Join our Discord community](https://discord.gg/YourLinkHere)

## Acknowledgment & support

Special thanks to [YourSponsor](https://yoursponsor.com/) for their support. If you enjoy our project, consider supporting us on [Patreon](https://www.patreon.com/YourProject).

---

This README retains the structure of the original while reorienting the content to match the themes and specifics of the Waifu Web UI project, preserving its engaging and playful spirit.
