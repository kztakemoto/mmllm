import pandas as pd
import re

import argparse

#### Parameters #############
parser = argparse.ArgumentParser()
parser.add_argument('--model', default='gpt-3.5-turbo-0613', type=str)
parser.add_argument('--nb_scenarios', default='3', type=int)
parser.add_argument('--random_seed', default='123', type=int)
args = parser.parse_args()

df = pd.read_pickle("results_{}_scenarios_seed{}_{}.pickle".format(args.nb_scenario, args.random_seed, args.model))

keywords = ["case 1", "case 2"]

def response_classification(query):
  text = query.lower()
  
  pattern_case1 = re.compile(r"case\s?1")
  pattern_case2 = re.compile(r"case\s?2")

  match_case1 = pattern_case1.search(text) is not None
  match_case2 = pattern_case2.search(text) is not None

  if match_case1 and not match_case2:
      label = 0
  elif not match_case1 and match_case2:
      label = 1
  else:
      label = -1

  return label

# assign the response labels
if 'chat_response' in df.columns:
  df['label'] = df['chat_response'].apply(response_classification)
else:
  if "gpt" in args.model:
    df['label'] = df['chatgpt_response'].apply(response_classification)
  elif "palm" in args.model:
    df['label'] = df['palm2_response'].apply(response_classification)
  elif "llama" in args.model:
    df['label'] = df['llama2_response'].apply(response_classification)
  elif "vicuna" in args.model:
    df['label'] = df['vicuna_response'].apply(response_classification)
  elif "gemini" in args.model:
    df['label'] = df['gemini_response'].apply(response_classification)
  elif "claude" in args.model:
    df['label'] = df['claude_response'].apply(response_classification)

df = df[df["label"] >=0].reset_index(drop=True)
print(df)
#df = df.sample(n = 5000) # for debug

# conver the data into data format for conjoint analysis
CrossingSignal_dict = {
  "NA": 0,
  "green": 1,
  "red": 2, 
}

ScenarioType_dict = {
  "species": "Species",
  "social_value": "Social Value",
  "gender": "Gender",
  "age": "Age",
  "fitness": "Fitness",
  "utilitarianism": "Utilitarian",
  "random": "Random",
}

AttributeLevel_dict = {
  "species": {
    "human": "Hoomans",
    "pet": "Pets",
  },
  "social_value": {
    "lower": "Low",
    "higher": "High",
  },
  "gender": {
    "female": "Female",
    "male": "Male",
  },
  "age": {
    "younger": "Young",
    "older": "Old",
  },
  "fitness": {
    "lower": "Fat",
    "higher": "Fit",
  },
  "utilitarianism": {
    "less": "Less",
    "more": "More",
  },
  "random": {
    "random": "Rand",
  }
}

characters = ["man", "woman", "pregnant woman", "baby", "elderly man", "elderly woman", "boy", "girl", "homeless person", "large woman", "large man", "criminal", "male executive", "female executive", "female athlete", "male athlete", "female doctor", "male doctor", "dog", "cat"]

characters_dict = {
  "man": "Man",
  "woman": "Woman",
  "pregnant woman": "Pregnant",
  "baby": "Stroller",
  "elderly man": "OldMan",
  "elderly woman": "OldWoman",
  "boy": "Boy",
  "girl": "Girl",
  "homeless person": "Homeless",
  "large woman": "LargeWoman",
  "large man": "LargeMan",
  "criminal": "Criminal",
  "male executive": "MaleExecutive",
  "female executive": "FemaleExecutive",
  "female athlete": "FemaleAthlete",
  "male athlete": "MaleAthlete",
  "female doctor": "FemaleDoctor",
  "male doctor": "MaleDoctor",
  "dog": "Dog",
  "cat": "Cat",
}

sharedresponse_list = []
for index, row in df.iterrows():
  # group 1
  sharedresponse = {}
  sharedresponse['ResponseID'] = "res_{:08}_1".format(index)
  sharedresponse['ExtendedSessionID'] = "chatbot_extended"
  sharedresponse['UserID'] = "chatbot"
  sharedresponse['ScenarioOrder'] = 0
  sharedresponse['Intervention'] = int(row['is_interventionism'])
  sharedresponse['PedPed'] = int(not row['is_in_car'])
  if sharedresponse['PedPed'] == 1:
    sharedresponse['Barrier'] = 0
    sharedresponse['CrossingSignal'] = CrossingSignal_dict[row["traffic_light_pattern"][0]]
  else:
    sharedresponse['Barrier'] = 1
    sharedresponse['CrossingSignal'] = 0
  sharedresponse['Saved'] = int(row['label'] != 0)
  sharedresponse['NumberOfCharacters'] = sum(row["count_dict_1"].values())
  sharedresponse['DiffNumberOFCharacters'] = abs(sum(row["count_dict_1"].values()) - sum(row["count_dict_2"].values()))
  sharedresponse['Template'] = "desktop"
  sharedresponse['DescriptionShown'] = 1
  sharedresponse['LeftHand'] = 1
  sharedresponse['UserCountry3'] = "JPN"
  sharedresponse['ScenarioType'] = ScenarioType_dict[row["scenario_dimension"]]
  sharedresponse['ScenarioTypeStrict'] = ScenarioType_dict[row["scenario_dimension"]]
  sharedresponse['AttributeLevel'] = AttributeLevel_dict[row["scenario_dimension"]][row["scenario_dimension_group_type"][0]]
  sharedresponse['DefaultChoice'] = None
  sharedresponse['NonDefaultChoice'] = None
  sharedresponse['DefaultChoiceIsOmission'] = None
  count = {characters_dict[key]: row["count_dict_1"].get(key, 0) for key in characters}
  sharedresponse.update(count)

  sharedresponse_list.append(sharedresponse)

  # group 2
  sharedresponse = {}
  sharedresponse['ResponseID'] = "res_{:08}_2".format(index)
  sharedresponse['ExtendedSessionID'] = "chatbot_extended"
  sharedresponse['UserID'] = "chatbot"
  sharedresponse['ScenarioOrder'] = 0
  sharedresponse['Intervention'] = int(not row['is_interventionism'])
  sharedresponse['PedPed'] = int(not row['is_in_car'])
  sharedresponse['Barrier'] = 0
  sharedresponse['CrossingSignal'] = CrossingSignal_dict[row["traffic_light_pattern"][1]]
  sharedresponse['Saved'] = int(row['label'] != 1)
  sharedresponse['NumberOfCharacters'] = sum(row["count_dict_2"].values())
  sharedresponse['DiffNumberOFCharacters'] = abs(sum(row["count_dict_1"].values()) - sum(row["count_dict_2"].values()))
  sharedresponse['Template'] = "desktop"
  sharedresponse['DescriptionShown'] = 1
  sharedresponse['LeftHand'] = 0
  sharedresponse['UserCountry3'] = "JPN"
  sharedresponse['ScenarioType'] = ScenarioType_dict[row["scenario_dimension"]]
  sharedresponse['ScenarioTypeStrict'] = ScenarioType_dict[row["scenario_dimension"]]
  sharedresponse['AttributeLevel'] = AttributeLevel_dict[row["scenario_dimension"]][row["scenario_dimension_group_type"][1]]
  sharedresponse['DefaultChoice'] = None
  sharedresponse['NonDefaultChoice'] = None
  sharedresponse['DefaultChoiceIsOmission'] = None
  count = {characters_dict[key]: row["count_dict_2"].get(key, 0) for key in characters}
  sharedresponse.update(count)

  sharedresponse_list.append(sharedresponse)


new_index_order = ["ResponseID", "ExtendedSessionID","UserID", "ScenarioOrder", "Intervention", "PedPed", "Barrier", "CrossingSignal", "AttributeLevel", "ScenarioTypeStrict", "ScenarioType", "DefaultChoice", "NonDefaultChoice", "DefaultChoiceIsOmission", "NumberOfCharacters", "DiffNumberOFCharacters", "Saved", "Template", "DescriptionShown", "LeftHand", "UserCountry3", "Man", "Woman", "Pregnant", "Stroller", "OldMan", "OldWoman", "Boy", "Girl", "Homeless", "LargeWoman", "LargeMan", "Criminal", "MaleExecutive", "FemaleExecutive", "FemaleAthlete", "MaleAthlete", "FemaleDoctor", "MaleDoctor", "Dog", "Cat"]

df = pd.DataFrame(sharedresponse_list)
df = df[new_index_order]

df.to_csv("shared_responses_{}.csv".format(args.model), index=False)

print(df)
