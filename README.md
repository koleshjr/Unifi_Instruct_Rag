# **Unifi Value Frameworks PDF Lifting Project**

Can you extract existing ESG metrics from static PDF documents?

## **Background**

Many companies are working hard to embed sustainability initiatives into the DNA of their businesses, not just in an attempt to do good but because sustainability is also good for business. Sustainable businesses are often more efficient and effective than their non-sustainable counterparts. This is because sustainable businesses typically use resources more efficiently, have lower waste and energy costs, and have more engaged and productive employees.

The management of sustainability initiatives hinges on collecting and collating business metrics that are often not easily accessible from business enterprise resource planning (ERP) systems. One source of sustainability data is the integrated report that companies publish annually. These annual reports provide a comprehensive overview of a company's performance, financial health, and progress towards sustainability deliverables, and offer transparency into the company's activities to shareholders, investors, regulators, employees, and the public. Annual reports also serve as a historical record of a company's performance over time, and enable comparisons between different periods, helping stakeholders track progress and trends.

Despite all of these documents being in the public domain, extracting and analyzing data from annual reports of large corporations can present several challenges. Annual reports contain unstructured data, don’t follow standardized formats, contain a vast array of information, and differ in structure and presentation between companies.

### **Objective**

The objective of this challenge is to create a solution that parses these annual reports in PDF format and extracts information about predefined activity metrics, in order for Unifi to obtain specific information about sustainability at a given company.

### **How to Run**

There are four stages in a Rag Pipeline: Ingest, Embed, Retrieve, and Answer. This can be condensed to two stages: Ingest + Embed and Retrieve and Answer.

#### **Initial steps**

1. Git clone this repo

2. Setup conda environment or venv. Your choice (Optional)
   
3. Pip install all the requirements in requirements.txt

#### **Ingest and Embed**

Run index.py and pass specified CLI arguments. Specifically:

   a) --vector_store: at the moment the project supports chroma, Milvus, and faiss e.g. faiss
   
   b) --index_name: name it whatever you like as it will be the name of your vector database e.g. faiss_db
   
   c) --embedding_provider: at the moment the project supports OpenAI, Google, Mistral, Hugging Face, and Azure (though not flexible atm) e.g. Hugging Face

#### **Retrieve and Answer**

Run main.py and pass the specified CLI arguments. Specifically:

   a) --vector_store: the vector database you used in the ingest and embed stage e.g. faiss
   
   b) --index_name: the name you gave your vector database index in the ingest and embed stage e.g. faiss_db
   
   c) --model_provider: the model provider you want to use. At the moment the project supports OpenAI, Google, Azure, and Mistral e.g. OpenAI
   
   d) --model_name: Once you have decided which model provider to use then you can choose one of the models they provide e.g. gpt-3.5-turbo-1106
   
   e) --embedding_provider: The embedding provider you used in the embed stage or any since this will be used to embed the query e.g. Hugging Face
   
   f) --year: The year for which you want to extract the metrics e.g. 2022
   
   g) -- experiment: What you want your submission file to be saved as e.g. experiment one

#### **Main takeaways**

* Proprietary models definitely won.
  
   In my case, I had success with Gemini-Pro and GPT-4. GPT-4 is expensive but still doesn't cost more than $11 per extraction. Gemini-Pro, on the other hand, is way cheaper (approximately $0.5 to $1 per experiment) and offers comparable accuracy with GPT-4 although slightly lower.
  
* Large language models love to be shown what to do to increase accuracy.

   Passing the previous year answers definitely helped the model to output more accurate results.
  
* The model was struggling with the units/magnitude despite proper prompts.

   Some of the values were given in different magnitudes, and you had to derive the accurate value by doing some mathematical calculation, for example, 8.8 Rbn (in the PDF), but in the evaluation, you need to pass 8800000000 for it to be accurate.    The models really struggled with this.
  
* Metrics for some companies were not straightforward.
  
   For example, a company like Impala, the accurate values were obtained by adding values for Impala Rustenburg, Impala Refineries, and Marula. For Impala, the model really struggled despite a good prompt.
   Also for SSW, the values we were supposed to extract were for SA operations PGM and gold, and we were supposed to ignore for Europe. This separation proved so hard for the model to get it right.

#### **Potential ways of cheating on this competition**

* One could easily read the PDFs, build a CSV of the accurate values by doing all the calculations mentioned above manually, and embed this CSV. With this approach, you can easily get to >0.94 with even less than $0.20. Doing this, despite giving the best results, doesn't make sense for the competition objective. The objective is not to build a question-answering system as this would be the best way to do it but actually, the objective is to build an extractor. No human should be involved. The human should only be involved after the extraction process for confirmation purposes only. Involving a human before then, what is the point of building a model then? Just let them read the PDFs and get the values then build a question-answering system.

* As you can see in this approach no human is involved in the whole of this Extraction process. No preprocessing, no postprocessing just letting the Model handle everything

#### **Implementation suggestion**

* Build an API where after each year, you could just pass all the company PDFs and then get a list of JSON metadata representing the client metrics and the extracted values.
  
* And then after, since these models are not 100% accurate, involve the human to correct the wrongly predicted values and then build a CSV with these values.
  
* Then embed this CSV and use this for a question-answering system. This will be very accurate and fast as it just has to parse a row of metadata instead of a whole page of text.
