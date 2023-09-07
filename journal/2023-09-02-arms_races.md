
## view point of education 

### ACG (A Cloud Guru)

Artificial Intelligence and Machine Learning: AWS vs Azure vs GCP by [ACG Technical Editors Team(Jun 08, 2023 )](https://www.pluralsight.com/resources/blog/cloud/aws-vs-azure-vs-gcp-artificial-intelligence-and-machine-learning#h-speech-to-text-and-text-to-speech)

service|A WS|Azure|GCP
-|-|-|-
Speech to text|[ Amazon Transcribe](https://aws.amazon.com/tw/transcribe/)|[Speech to text]()|[peech to text](https://aws.amazon.com/tw/polly/)
pack|60 分鐘語音轉寫文字服務，使用期限 12 個月||
text to audible|[Amazon Polly](https://aws.amazon.com/tw/polly/)||
pack|每月免費獲得 500 萬個字元，為期 12 個月|||
Chatbots|[ Amazon Lex](https://aws.amazon.com/tw/lex/)||
pack|12 個月 10,000 個文字和 5,000 個語音請求免費。已建有保險、航班、通訊、財務、銷售等5個模版。||
Translation|[ Amazon Translate](https://docs.aws.amazon.com/translate/latest/dg/what-is.html)|
pack|免費:每月最多200萬個字元(12 個月)|
Text Analytics|[Amazon Comprehend](https://aws.amazon.com/tw/comprehend/)關鍵片語、情緒、實體辨識、語言偵測、事件類型偵測、語法分析|
pack|10,000 封意見，每封550 個字元，分析客戶評論需6USD。

### datacamp.com

AWS, Azure and GCP Service Comparison for Data Science & AI by [Richie Cotton(Jun 2023)](https://www.datacamp.com/cheat-sheet/aws-azure-and-gcp-service-comparison-for-data-science-and-ai)

ML & AI
Service type|Description|AWS|Azure|GCP
-|-|-|-|-
Machine Learning|Train, fit, validate, and deploy ML models|[SageMaker](https://aws.amazon.com/sagemaker)|[Machine Learning](https://azure.microsoft.com/en-us/products/machine-learning/)|[Vertex AI](https://cloud.google.com/vertex-ai/)
Jupyter notebooks|Write data analyses and reports|[SageMaker Notebooks](https://aws.amazon.com/sagemaker/notebooks/)|[Notebooks](https://visualstudio.microsoft.com/vs/features/notebooks-at-microsoft/)|[Colab](https://colab.research.google.com/notebook)
Data science/machine learning VM|Virtual machines tailored to data work|[Deep Learning AMIs](https://aws.amazon.com/machine-learning/amis/)|[Data Science Virtual Machines](https://azure.microsoft.com/en-us/products/virtual-machines/data-science-virtual-machines/)|[Deep Learning VM](https://cloud.google.com/deep-learning-vm)
AutoML|Automatically build ML models|[SageMaker](https://aws.amazon.com/sagemaker)|[Machine Learning Studio](https://ml.azure.com/),[Automated ML](https://azure.microsoft.com/en-us/products/machine-learning/automatedml/)|[Vertex AI Workbench](https://cloud.google.com/vertex-ai-workbench)
Natural language Processing AI|Analyze text data|[Comprehend](https://aws.amazon.com/comprehend/)|[Text Analytics](https://azure.microsoft.com/en-us/products/cognitive-services/text-analytics/)|[Natural Language AI](https://cloud.google.com/natural-language)
Recommendation AI|Product recommendation engine|[Personalize](https://aws.amazon.com/personalize/)|[Personalizer](https://azure.microsoft.com/en-us/products/cognitive-services/personalizer/)|[Recommendations AI](https://cloud.google.com/recommendations)
Document capture|Extract text from printed text & handwriting|[Textract](https://aws.amazon.com/textract/)|[Form Recognizer](https://azure.microsoft.com/en-us/products/form-recognizer/)|[Document AI](https://cloud.google.com/document-ai)
Computer vision|Image classification, object detection & other AI with image data|[Rekognition](https://aws.amazon.com/rekognition/), [Panorama](https://aws.amazon.com/panorama/), [Lookout for Vision](https://aws.amazon.com/lookout-for-vision/)|[Cognitive Services for Vision](https://azure.microsoft.com/en-us/products/cognitive-services/vision-services/)|[Vision AI](https://cloud.google.com/vision)
Speech to text|Speech transcription|[Transcribe](https://aws.amazon.com/transcribe/)|[Cognitive Services for Speech to Text](https://azure.microsoft.com/en-us/products/cognitive-services/speech-to-text/), [Cognitive Services for Speaker Recognition](https://azure.microsoft.com/en-us/products/cognitive-services/speaker-recognition/)|[Speech-to-Text](https://cloud.google.com/speech-to-text)
Text to speech|Speech generation|[Polly](https://aws.amazon.com/polly/)|[Cognitive Services for Text to Speech](https://azure.microsoft.com/en-us/products/cognitive-services/text-to-speech/)|[Text-to-Speech](https://cloud.google.com/text-to-speech)
Translation AI|Convert text between human languages|[Translate](https://aws.amazon.com/translate/)|[Cognitive Services for Speech Translation](https://azure.microsoft.com/en-us/products/cognitive-services/speech-translation/), [Translator](https://azure.microsoft.com/en-us/products/cognitive-services/translator/)|[Translation AI](https://cloud.google.com/translate)
Video Intelligence|Video indexing and asset search|[Rekognition Video](https://aws.amazon.com/rekognition/video-features/)|[Video Indexer](https://azure.microsoft.com/en-us/products/video-indexer/)|[Video Intelligence API](https://cloud.google.com/video-intelligence/docs)
AI agents|Virtual assistants and chatbots|[Lex](https://aws.amazon.com/lex/), [Alexa Skills kit](https://developer.amazon.com/en-US/alexa/alexa-skills-kit)|[Bot Service](https://azure.microsoft.com/en-us/products/bot-services/), [Cognitive Services for Conversational Language Understanding](https://azure.microsoft.com/en-us/products/cognitive-services/conversational-language-understanding/)|[Dialogflow](https://cloud.google.com/dialogflow/)
Human-in-the-loop|Human-based quality control for AI|[Augmented AI (A2I)](https://aws.amazon.com/augmented-ai/)|[Cognitive Services Content Monitor](https://azure.microsoft.com/en-us/products/cognitive-services/content-moderator/)|N/A

除了Datacamp之外，類似的知名在線技術培訓平台還有哪些?試舉出前3大公司。

Besides Datacamp, some popular similar online technology training platforms are:

1. Udemy - Offers a wide range of courses in various fields, including programming, IT, design, marketing, and more.
2. Coursera - Provides online courses from top universities and organizations worldwide, focusing on professional development and personal enrichment.
3. edX - A non-profit online learning destination founded by Harvard and MIT, offering courses from leading institutions such as Harvard, MIT, UC Berkeley, and more.

## openAI cookbook

[openAI()](https://github.com/openai/openai-cookbook)

### prompttools

- source code: [prompttools](https://github.com/hegelai/prompttools)
- 因g++不相容，在centos7安裝不起來
- 改在window anaconda安裝。
- 執行

```bash
C:\Users\4139\AppData\Local\anaconda3\envs\LLM\Scripts\jupyter-notebook examples/notebooks/OpenAIChatExperiment.ipynb
```

- 問題與解決
  - 舊函式名稱已改
    - `experiment.visualize_table()` -> `experiment.visualize()`
    - `experiment.evaluate_by_row()` -> `experiment.evaluate()`
    - `similarity.semantic_similarity_by_row` -> `similarity.semantic_similarity`
  - 繪圖時在使用者家目錄下找不到style檔案 -> 由git包內找到

```bash
copy l:/nas2/kuang/prompttools/prompttools/experiment/experiments/style.mplstyle \
C:\Users\4139\AppData\Roaming\Python\Python311\site-packages\prompttools\experiment\experiments
```