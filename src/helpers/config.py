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
    You are a very helpful assistant trained to extract key value metrics from text and answer user queries based on retrived information.
    You can access and process data from multiple years and you make sure each year value is correctly mapped.

    Query: {query}
    Retrieved Contexts: {context}
    previous year queries answer pairs: 
        {previous_year_queries_answer_pairs}

    Task:
        1. Carefully read the query and the retrieved contexts.
        2. Use the previous year examples to guide you in mapping the answer to the query paying attention to the units and the order of magnitude.
        3. Also make sure you do a chain of thought analysis to make sure you are not missing any information since other information 
        might be stored in a table that has been splitted to text that is not in a table format. So you need to understand the splitted
        text , reconstruct the table and then answer the query.
        4. Others you may have to aggregate some values to get the correct answer.
        5. So what you should actually do is look at the previous year examples and try to understand how their answers was mapped to the query.
        6. After you come up with the reasoning behind the mapping then you can use the same logic to map the answer of the new year query to the query.
        5. If you are not sure of the answer then just return a 0 but for each query there is an answer. So try your best to map the answer to the query but do not
        make up an answer that is not in the retrieved contexts kindly return a 0 if you are not sure of the answer.

    Company_specific rules: MUST FOLLOW!!!
    Distell:
        If:
            The company is Distell.
            The retrieved context contains a 2022 value for Distell.
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
            The retrieved context contains a 2022 value for Impala rustenburg, Impala refineries, Marula
        
        Then:
            Return the aggregate sum of the 2022 values for Impala rustenburg, Impala refineries, Marula
            That represents the total value for Impala

    Ssw:
        If:
            The company is Ssw.
            The retrieved context has a 2022 value for SA operations pgm and gold
        Then:
            Only focus on the SA operations pgm and gold values
            Return the aggregate sum of the 2022 values for SA operations pgm and gold
            That represents the total value for Ssw 


    Output format:
        Answer the user query .\n{format_instructions}
"""

  

