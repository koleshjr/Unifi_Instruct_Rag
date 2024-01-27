class Config:
  # data configs
  folder_path = "src/data/"
  validation_filepath = "src/Competition_data\Train.csv"
  submission_filepath = "src/Competition_data\SampleSubmission.csv"
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


    Output format:
        {
            prev_years_reasoning: "reasoning behind the mapping of the previous year queries answer pairs",
            answer: "answer to the query",
            reasoning: "reasoning behind the mapping of the answer to the query",
        }










"""

  

