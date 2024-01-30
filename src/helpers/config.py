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
        Distell:
            If the company is Distell and 2022 value is present in the context:
                Remove the leftmost digit and return the remaining value for 2022.
                Examples:
                    Context: "Number of lost days (Distell Group)1161 127 550"
                    Output: "161"
                    Context: "Number of work-related fatalities (Distell Group)10 1 0"
                    Output: "0"

        Impala:
            If the company is Impala and 2022 values are present for specified locations:
                extract the 2022 values for Impala rustenburg, Impala refineries, Marula.
                return the aggregate sum of the 2022 values for Impala rustenburg, Impala refineries, Marula.

        Ssw:
            If the company is Ssw and 2022 values are present for SA operations pgm and gold:
                extract the 2022 values for SA operations pgm and gold.
                Return the aggregate sum of the 2022 values for SA operations pgm and gold.
        ```

    Task Instructions:
        1. Read and understand the query, context, and company rules.
        2. Analyze previous year queries and answers to understand how values were extracted.
        3. Repeat step 2 to identify patterns in answer extraction.
        4. Generate rules based on understanding from step 3.
        5. Follow company-specific rules, extract and confirm the answer's magnitude and units.
        6. If necessary, align the answer to the same magnitude and units as the previous year's answer.
        7. If unable to extract, return 0 to avoid providing inaccurate answers.

    Output Format:
        Answer the user query.\n{format_instructions}
    """


  

