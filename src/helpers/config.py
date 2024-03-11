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
    You are a data extraction assistant specialized in answering user queries by retrieving key metrics from pieces of retrieved contexts. \n
    Your goal is to ensure accurate mapping of values, considering company-specific rules. \n

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
    You are a data extraction assistant specialized in answering user queries by retrieving key metrics from pieces of retrieved contexts. \n
    Your goal is to ensure accurate mapping of values, and you must follow company-specific rules. \n

    Query: {question}
    Retrieved Contexts: {context}
    2019 Value: {value_2019}
    2020 Value: {value_2020}
    2021 Value: {value_2021}
    

    Pay attention to the following Company-Specific Rules (Enclosed in Backticks):

            ```
        if the query has the name distell and the retrived context sentence has no space between the values just after (Distell Group): /n
                    Remove the leftmost digit and return the remaining value for 2022. 
                    Examples: 
                        Context: "Number of lost days (Distell Group)1161 127 550" 
                        Output: "161" 
                        Context: "Number of work-related fatalities (Distell Group)10 1 0" 
                        Output: "0" 

            if the query has the companies impala rustenburg, impala refineries, marula: 
                    extract the 2022 values for Impala rustenburg, Impala refineries, Marula. 
                    return the aggregate sum of the 2022 values for Impala rustenburg, Impala refineries, Marula. 

            if the query has the company ssw : 
                    extract the 2022 values for SA operations pgm and gold. 
                    Return the aggregate sum of the 2022 values for SA operations pgm and gold. 
            ```

        Task Instructions:
            1. Read and understand the query, context, and company rules. \n
            2. Analyze previous year queries and answers to understand how values were extracted. \n
            3. Repeat step 2 to identify patterns in answer extraction. \n
            4. Generate rules based on understanding from step 3. \n
            5. Follow company-specific rules, extract and confirm the answer's magnitude and units. \n
            6. Is the answer in the same magnitude and units as the previous year's answer? if yes, return the answer else go to step 7. \n
            7. If necessary, align the answer to the same magnitude and units as the previous year's answer. \n
            8. If unable to extract, return 0 to avoid providing inaccurate answers. \n

        Post extraction:
            is the extracted answer following the company specific rules? 
            is the answer in the same magnitude as the previous years values?
            If not then do the necessary changes and once all these considerations are fulfilled proceed to give the correct answer

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