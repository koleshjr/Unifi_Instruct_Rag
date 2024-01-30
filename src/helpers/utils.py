import pandas as pd
import numpy as np 
import warnings
warnings.filterwarnings("ignore")

def prepare_train_data(train_filepath: str, synonyms_path: str, standard_path: str)-> pd.DataFrame:
    file = pd.read_csv(train_filepath)
    synonyms = pd.read_csv(synonyms_path)
    standard = pd.read_csv(standard_path)

    file.dropna(subset = ['2021_Value'], inplace = True)
    file.drop(columns = ['2019_Value'], inplace = True)
    synonyms['ID'] = synonyms['AMKEY'].astype('str') + '_X_' + synonyms['Group']
    file = pd.merge(file, synonyms[['ID', 'ActivityMetric', 'ClientMetric']], how = "left", on = "ID") 
    valid_1 = file.dropna(subset = ['ClientMetric']).drop(columns = ['ActivityMetric'])
    valid_1.rename(columns = {'ClientMetric': 'ActivityMetric'}, inplace = True)
    valid_2 = file[pd.isnull(file['ClientMetric'])]
    valid_2['AMKEY'] = valid_2['ID'].apply(lambda x: x.split("_")[0]).astype('int')
    valid_2.drop(columns = ['ActivityMetric', 'ClientMetric'], inplace = True)
    valid_2 = pd.merge(valid_2, standard[["AMKEY", "ActivityMetric"]], how = "left", on = "AMKEY")

    final_valid = pd.concat([valid_1, valid_2]).reset_index(drop=True)
    final_valid['group'] = final_valid['ID'].apply(lambda x: x.split("_")[2])

    conditions = [
        (final_valid['group'] == 'Impala'),
        (final_valid['group'] == 'Ssw'),
    ]
    choices = [
        final_valid['ActivityMetric'] + " for Impala Rustenburg, Impala Refineries, Marula ",
        final_valid['ActivityMetric'] + " in Ssw for SA Operations PGM and Gold ",
    ]
    default = final_valid['ActivityMetric'] + " in " + final_valid['group']
    final_valid['query'] = np.where(conditions[0], choices[0],
                                np.where(conditions[1], choices[1], default))
    
    final_valid = pd.melt(final_valid, id_vars = ["ID", "ActivityMetric", "AMKEY", "group", "query"], 
                          var_name = "Year", value_name = "Value")
    final_valid['Year'] = final_valid['Year'].str.extract('(\d{4})')
    final_valid = final_valid.sort_values(by=['ID', 'Year']).reset_index(drop=True)
    final_valid.dropna(subset = ['Year'], inplace = True)


    final_valid['example'] ="Query: " + final_valid['query'] + " in the year " + final_valid['Year'] + " ? " + " Answer: " + final_valid['Value']

    return final_valid.dropna(subset = ['example'])

def prepare_sub_data(sub_filepath: str, synonyms_path: str, standard_path: str) -> pd.DataFrame:
    file = pd.read_csv(sub_filepath)
    synonyms = pd.read_csv(synonyms_path)
    standard = pd.read_csv(standard_path)
    synonyms['ID'] = synonyms['AMKEY'].astype('str') + '_X_' + synonyms['Group']
    file = pd.merge(file, synonyms[['ID', 'ActivityMetric', 'ClientMetric']], how ="left", on="ID")
    sub_1 = file.dropna(subset = ['ActivityMetric']).drop(columns = ['ActivityMetric'])
    sub_1.rename(columns = {'ClientMetric': 'ActivityMetric'}, inplace = True)
    sub_2 = file[pd.isnull(file['ActivityMetric'])]
    sub_2['AMKEY'] = sub_2['ID'].apply(lambda x: x.split("_")[0]).astype('int')
    sub_2.drop(columns = ["ActivityMetric", "ClientMetric"], inplace = True)   
    sub_2 = pd.merge(sub_2, standard[['AMKEY', 'ActivityMetric']], how="left", on = "AMKEY")
    final_sub = pd.concat([sub_1, sub_2]).reset_index(drop=True)
    final_sub['group'] = final_sub['ID'].apply(lambda x: x.split("_")[2])

    
    conditions = [
        (final_sub['group'] == 'Impala'),
        (final_sub['group'] == 'Ssw'),
    ]
    choices = [
        final_sub['ActivityMetric'] + " for Impala Rustenburg, Impala Refineries, Marula in the year 2022?",
        final_sub['ActivityMetric'] + " in Ssw for SA Operations PGM and Gold in the year 2022?",
    ]
    default = final_sub['ActivityMetric'] + " in " + final_sub['group'] + " in the year 2022?"

    final_sub['query'] = np.where(conditions[0], choices[0],
                                np.where(conditions[1], choices[1], default))
    return final_sub[['ID', 'query']] 

