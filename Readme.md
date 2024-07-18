# Document Text Extraction

This project aims to extract text from images of documents, such as passports and driver's licenses. The process involves several stages, including image preprocessing, Optical Character Recognition (OCR), and text enhancement using Fireworks AI.

## Overview

1. **Image Preprocessing**: 
   - **Rotation**: Adjusts the orientation of the image to ensure text is properly aligned.
   - **Smoothing**: Enhances the clarity of the text for better OCR performance.
   - **Morphological Operations**: Highlights text regions and prepares the image for text extraction.

2. **Text Extraction**:
   - **OCR**: Uses pytesseract to extract text from the preprocessed image.
   - **Fireworks AI**:
     - **Visual Language Model (VLM)**: Provides additional information based on the extracted text and the image.
     - **Large Language Model (LLM)**: Corrects and enhances the text information using the VLM output.

## Design Choices and Tradeoffs

- **Preprocessing with OpenCV**: 
  - **Why**: OpenCV provides robust image processing tools to rotate, smooth, and enhance images. These steps are crucial for preparing the image for accurate text extraction.
  - **Tradeoffs**: While effective, the chosen preprocessing methods are not as advanced as some deep learning-based techniques. Better preprocessing could be achieved with models like YOLOv8 for text detection or other pretrained models. However, due to restrictions, only Fireworks API was used, which limited the use of more sophisticated models.

- **OCR with pytesseract**:
  - **Why**: pytesseract is a widely used OCR tool that integrates easily with Python. It is well-suited for extracting text from images.
  - **Tradeoffs**: Although pytesseract is effective, its accuracy can be affected by image quality and preprocessing. Advanced OCR models or fine-tuned models could provide better results but were not used due to API restrictions.

- **Fireworks AI**:
  - **Why**: Fireworks API was used to enhance text extraction by leveraging VLM and LLM. This approach aims to improve the accuracy of extracted information.
  - **Tradeoffs**: The VLM model’s performance is dependent on the quality of the preprocessed image and initial OCR results. The LLM helps correct errors but cannot replace fine-tuning or more advanced models.

- **Time and Data Limitations**:
  - **Preprocessing**: Due to time constraints, the preprocessing steps were not extensively optimized. Improved preprocessing could significantly enhance results.
  - **VLM Fine-Tuning**: The inability to fine-tune the VLM model restricted the potential for better accuracy. Fireworks API did not support fine-tuning.
  - **MRZ Extraction**: Extracting MRZ information from passports was not implemented due to time constraints.

## Prerequisites

- Python 3.x
- Fireworks API Key

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/your-repository.git
   cd your-repository

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
{
  "1. Document Type": "Driver's License",
  "2. Full Name": "Ilva Cordelleiro",
  "3. Date of Birth": "08/31/1977",
  "4. Document Number": "234538",
  "5. Issue Date": "08/31/2014",
  "6. Expiration Date": "08/31/2018",
  "7. Nationality": "",
  "8. Address": "2570 24th Street, Anytown, CA 95818",
  "9. Gender": "M",
  "10. Issuing Authority": "USA",
  "11. Eye and Hair Color": "Brown, Brown",
  "12. Height and Weight": "HT (5'8\" - 5'10\") WGT (128 - 200 lbs)"
}

```

```bash
python GetTexts.py passport-1.png
{
"1. Document Type": "Passport",
"2. Full Name": "John Hye",
"3. Date of Birth": "15 Mar 1996",
"4. Document Number": "545637",
"5. Issue Date": "11/04/2005",
"6. Expiration Date": "09/2027",
"7. Nationality": "United States of America",
"8. Address": "California, U.S.A",
"9. Gender": "Male",
"10. Issuing Authority": "United States Department of State",
"11. Eye and Hair Color": "Black, black",
"12. Height and Weight": "Not available (since not mentioned in the text)",
"13. Class": "Not available (since not mentioned in the text)"
}
```




   
