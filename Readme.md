# Document Text Extraction

This project is designed to extract text from images of documents such as passports or driver's licenses. It uses image preprocessing techniques, Optical Character Recognition (OCR), and Fireworks AI for enhanced text extraction and correction.

## Prerequisites

- Python 3.x
- Fireworks API Key

## Installation

```bash
git clone https://github.com/Chandramani05/KYC_Detector.git
cd KYC_Detector

```
Create a virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Add your Fireworks API key:

- Create a .env file in the root directory of the project.
- Add your Fireworks API key to the .env file:


```bash
FIREWORK_AP_KEY=your_fireworks_api_key
```

## Usage
To run the script and extract text from an image, use the following command:

```bash
python GetTexts.py <file_path>
```

- <document_type>: The type of document (e.g., "Passport" or "License").
- <file_path>: The path to the image file.

### Example

```bash
python GetTexts.py License 1.png
```


   
