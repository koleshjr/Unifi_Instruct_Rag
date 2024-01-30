class Config:
  # data configs
  folder_path = "src/data/"
  validation_filepath = "src/Competition_data\Train.csv"
  submission_filepath = "src/competition_data/SampleSubmission.csv"
  synonyms_filepath = "src/Competition_data\ActivityMetricsSynonyms.csv"
  standard_filepath = "src/Competition_data\AMKEY_GoldenStandard.csv"

  # processed data configs
  df_valid_path = "src/data/df_valid.csv"
  sub_path = "src/data/sub.csv"
  
  # unify instruct template
  unifyai_template = """

    You are a data extraction assistant specialized in answering user queries by retrieving key metrics from pieces of retrieved contexts. \n
    Your goal is to ensure accurate mapping of values, considering company-specific rules. \n

    Query: {query}
    Retrieved Contexts: {context}
    Previous Year Queries & Answer Pairs:
        {previous_year_queries_answer_pairs}
    Company-Specific Rules (Enclosed in Backticks):

        ```
       if the query has the company distell and the retrived context sentence has no space between the values just after the company name: /n
                Remove the leftmost digit and return the remaining value for 2022. /n
                Examples: /n
                    Context: "Number of lost days (Distell Group)1161 127 550" /n
                    Output: "161" /n
                    Context: "Number of work-related fatalities (Distell Group)10 1 0" /n
                    Output: "0" /n

        if the query has the companies impala rustenburg, impala refineries, marula: /n
                extract the 2022 values for Impala rustenburg, Impala refineries, Marula. /n
                return the aggregate sum of the 2022 values for Impala rustenburg, Impala refineries, Marula. /n

        if the query has the company ssw : /n
                extract the 2022 values for SA operations pgm and gold. /n
                Return the aggregate sum of the 2022 values for SA operations pgm and gold. /n
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
        9. You must return a floating-point number as the answer, the extracted floating-point number OR 0 if unable to extract.\n
            do not add any additional text or characters to the answer.\n

    answer: "extracted floating point number as the answer"

    Please Please Please always format the answer like this.\n{format_instructions}
    """

  

