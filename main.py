import argparse
import pandas as pd
from src.services.retrieval import Retrieval
from src.services.embeddings import Embeddings
from src.services.llms import Llms
from src.helpers.config import Config
from src.helpers.utils import prepare_sub_data, prepare_train_data
from langchain_core.runnables import ConfigurableField 


parser = argparse.ArgumentParser(description='retrieval and generation')
parser.add_argument('--vector_store', type=str, default='chroma', help='vector store')
parser.add_argument('--index_name', type=str, default='index', help='index name')
parser.add_argument('--model_provider', type=str, default='huggingface', help='model provider')
parser.add_argument('--model_name', type=str, default='', help='model name')
parser.add_argument('--embedding_provider', type=str, default='huggingface', help='embedding provider')
parser.add_argument('--year', type=str, default='2022', help='year')
parser.add_argument('--experiment', type=str, default = 'experiment1', help='name of the experiment')

args = parser.parse_args()



if __name__ == "__main__":
    df_valid = prepare_train_data(train_filepath=Config.validation_filepath, synonyms_path=Config.synonyms_filepath, standard_path=Config.standard_filepath)
    df_sub = prepare_sub_data(sub_filepath=Config.submission_filepath, synonyms_path=Config.synonyms_filepath, standard_path=Config.standard_filepath)
    final_sub = pd.merge(df_sub, df_valid[['ID', '2021_Value', '2020_Value', '2019_Value']], how = "left", on = "ID")

    llm = Llms(model_provider=args.model_provider, model_name=args.model_name).get_chat_model() if 'instruct' not in args.model_name else Llms(model_provider=args.model_provider, model_name=args.model_name).get_llm()
    fallback_llm_1 = Llms(model_provider='google', model_name="gemini-pro").get_chat_model()
    df_valid.to_csv("src/data/df_valid.csv", index=False)

    model = (
        llm
        .with_fallbacks([fallback_llm_1])
        .configurable_alternatives(
            ConfigurableField(id = "model"),
            default_key = "llm",
            llm = llm,
            fallback_llm_1 = fallback_llm_1,
        )
    )

    retrieval = Retrieval(vector_store=args.vector_store, index_name=args.index_name)
    embeddings = Embeddings(embedding_provider=args.embedding_provider)

    for _, row in final_sub.iterrows():
        try:
            if row['ID'] not in df_valid['ID'].unique() or 'Tongaat' in row['ID']:
                df_sub.loc[df_sub['ID'] == row['ID'], 'Value'] = 0
            else:
                query = row['query'] + args.year
                print(f"Query: {query}")
                answer = retrieval.retrieve_and_generate(
                    embedding_function=embeddings.get_embedding_function(),
                    query=query,
                    value_2019=row['2019_Value'],
                    value_2020=row['2020_Value'],
                    value_2021=row['2021_Value'],
                    template=Config.unifyai_improved_template,
                    llm=llm
                )
                print(f"Answer: {answer}")
                print()
                df_sub.loc[df_sub['ID'] == row['ID'], 'Value'] = answer['value_2022']
                df_sub.to_csv(f'src/data/{args.experiment}_progress.csv', index=False)
                df_sub[['ID', 'Value']].fillna(0).to_csv(f'src/data/{args.experiment}.csv', index=False)
        except Exception as e:
            print(f"Error: {e} in row: {row}")

        