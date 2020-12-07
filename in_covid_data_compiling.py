import requests
import pandas as pd
import numpy as np

df = pd.read_csv("school_data.csv")

df["student_new_cases_categorized"] = df.apply(lambda x: "0" if x["suppress_student_new"] == 2 else (
                                                         "1-4" if x["suppress_student_new"] == 1 else (
                                                         x["student_new_cases"] if x["suppress_student_new"] == 0 else "not reported")), axis=1)

df["student_existing_cases_categorized"] = df.apply(lambda x: "0" if x["suppress_student_existing"] == 2 else (
                                                         "1-4" if x["suppress_student_existing"] == 1 else (
                                                         x["student_total_cases"] if x["suppress_student_existing"] == 0 else "not reported")), axis=1)

df["teacher_new_cases_categorized"] = df.apply(lambda x: "0" if x["suppress_teacher_new"] == 2 else (
                                                         "1-4" if x["suppress_teacher_new"] == 1 else (
                                                         x["teacher_new_cases"] if x["suppress_teacher_new"] == 0 else "not reported")), axis=1)

df["teacher_existing_cases_categorized"] = df.apply(lambda x: "0" if x["suppress_teacher_existing"] == 2 else (
                                                         "1-4" if x["suppress_teacher_existing"] == 1 else (
                                                         x["teacher_total_cases"] if x["suppress_teacher_existing"] == 0 else "not reported")), axis=1)

df["staff_new_cases_categorized"] = df.apply(lambda x: "0" if x["suppress_staff_new"] == 2 else (
                                                         "1-4" if x["suppress_staff_new"] == 1 else (
                                                         x["staff_new_cases"] if x["suppress_staff_new"] == 0 else "not reported")), axis=1)

df["staff_existing_cases_categorized"] = df.apply(lambda x: "0" if x["suppress_staff_existing"] == 2 else (
                                                         "1-4" if x["suppress_staff_existing"] == 1 else (
                                                         x["staff_total_cases"] if x["suppress_staff_existing"] == 0 else "not reported")), axis=1)


df_trim = df.loc[:,["school_id","school_name","county_fips","longitude","latitude",
                    "student_new_cases_categorized","teacher_new_cases_categorized","staff_new_cases_categorized",
                    "student_existing_cases_categorized","teacher_existing_cases_categorized","staff_existing_cases_categorized"]]


df_trim.to_csv("school_viz_data.csv", index=False)
