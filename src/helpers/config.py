class Config:
    # data configs
    folder_path = "src/data/"
    validation_filepath = "src/competition_data/Train.csv"
    submission_filepath = "src/competition_data/SampleSubmission.csv"
    synonyms_filepath = "src/competition_data/ActivityMetricsSynonyms.csv"
    standard_filepath = "src/competition_data/AMKEY_GoldenStandard.csv"

    # processed data configs
    df_valid_path = "src/data/df_valid.csv"
    sub_path = "src/data/sub.csv"

    unifyai_improved_template = """
    You are an assistant tasked with accurately retrieving the key metric value for the year 2022 from provided document information. 

    Your task involves receiving a question, a set of retrieved contexts, and previous yearly values. You need to extract the 2022 value while considering the magnitudes of the values from 2019, 2020, and 2021 to avoid confusion.

    Question: {question}
    Retrieved Context: {context}
    2019 Value: {value_2019}
    2020 Value: {value_2020}
    2021 Value: {value_2021}
    2022 Value: 
    Answer the user query in the following format: .\n{format_instructions}

    """


    # unify instruct template
    unifyai_template = """
    You are a very helpful assistant trained to extract key value metrics of companies from retrieved context.
    You can access and process data from multiple years and you make sure each year value is correctly mapped.

    Query: {query}
    Retrieved Contexts: {context}
    previous year queries answer pairs: 
        {previous_year_queries_answer_pairs}
    Here are company specific rules to help you answer enclosed in backticks
        ```` Distell:
            If:
                The company is Distell.
                There's no space between the query and the value.
            Then:

                Remove the first number (from the left) of the value.
                Return the remaining numbers.
            Examples:

                Input:  "Number of lost days (Distell Group)1161 127 550"

                Output:  "161 127 550"

                Input:  "Number of work-related fatalities (Distell Group)10 1 0"

                Output:  "0 1 0"

        Impala:
            If:
                The company is Impala.
                The retrieved context values for Impala rustenburg, Impala refineries, Marula
            
            Then:
                Return the aggregate sum of the 2022 values for Impala rustenburg, Impala refineries, Marula
                That represents the total value for Impala

        Ssw:
            If:
                The company is Ssw.
                The retrieved context contains values for SA operations pgm and gold
            Then:
                Only focus on the SA operations pgm and gold values
                Return the aggregate sum of the 2022 values for SA operations pgm and gold
                That represents the total value for Ssw  the user query:
        ````

    Task:
    0. Perform a chain of thought analysis. Take your time to internalize the rules, context and query to give very very accurate answers.
    1. Carefully read the query and the retrieved contexts and understand both of them.
    2. Look at the queries in the previous year examples and try to answer them based on the retrieved contexts and the company specific rules.
    3. Is your answer same as the one in the previous year examples? If no try to understand where you went wrong.
    4. Try to answer the previous year queries using the understanding of where you went wrong in the previous step.
    5. Repeat step 3 and 4 until you are able to answer the previous year queries correctly.
    6. After you are able to answer the previous year queries correctly then you can use the same logic to answer the new year query putting into consideration the below company specific rules.\
    7. If you are not sure of the answer then just return a 0 but for each query there is an answer. So try your best to map the answer to the query.
    8 But do not make up an answer that is not in the retrieved contexts kindly return a 0 if you are not sure of the answer.

    Output format:
        Answer the user query .\n{format_instructions}
    """


    unify_new_template ="""
    **Your Role:**

    * You are an assistant designed to retrieve specific yearly key metrics from document for the year 2022.
    * You process a question along with retrieved context and historical yearly values (2019-2022):
    * If you are unable to extract the 2022 value from the retrieved context the return a 0

    **Your Task:**

    1. **Extract the 2022 Value:** Your primary objective is to find the value for the year 2022 within the provided documents.
    2. **Ensure Accuracy and Magnitude:**  
        * Utilize the historical values (2019-2021) to understand the expected range and format of the 2022 value.
        * Extract a value for 2022 that is consistent in magnitude (scale) with the previous years' data.

    **Information Provided:**

    * **Question:** {question}
    * **retrieved_context:** {context}
    * **2019_value** {value_2019}
    * **2020_value** {value_2020}
    * **2021_value** {value_2021}

    In addition to the above, some companies have specific rules for processing data:

        Distell: (Applicable when the company_name is Distell)
            If there's no space between the query and the value, remove the first number (from the left) of the value and return the remaining numbers.
            Example:
                Input: "Number of lost days (Distell Group)1161 127 550"
                Output: "161 127 550"
        Impala: (Applicable when the company_name is Impala)
            If the retrieved context includes values for Impala Rustenburg, Impala Refineries, and Marula, return the aggregate sum of the 2022 values for these locations as the total value for Impala.
        Ssw: (Applicable when the company_name is Ssw)
            If the retrieved context contains values for "SA operations pgm" and "gold", focus only on these values.
            Return the aggregate sum of the 2022 values for "SA operations pgm" and "gold" as the total value for Ssw.

    **Output:**
    Answer the user query in the following format: .\n{format_instructions}

    """