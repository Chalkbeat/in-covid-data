import requests
import pandas as pd
from datetime import date

url = "https://www.coronavirus.in.gov/map/covid-19-indiana-school-report.json"

r = requests.get(url)
json = r.json()

# Collect and format school listing data
school_id = pd.DataFrame(json["school_listing"]["school_id"])
school_name = pd.DataFrame(json["school_listing"]["school_name"])
county_fips = pd.DataFrame(json["school_listing"]["county_fips"])
suppress_student_new = pd.DataFrame(json["school_listing"]["suppress_student_new"])
suppress_student_existing = pd.DataFrame(json["school_listing"]["suppress_student_existing"])
suppress_teacher_new = pd.DataFrame(json["school_listing"]["suppress_teacher_new"])
suppress_teacher_existing = pd.DataFrame(json["school_listing"]["suppress_teacher_existing"])
suppress_staff_new = pd.DataFrame(json["school_listing"]["suppress_staff_new"])
suppress_staff_existing = pd.DataFrame(json["school_listing"]["suppress_staff_existing"])
longitude = pd.DataFrame(json["school_listing"]["longitude"])
latitude = pd.DataFrame(json["school_listing"]["latitude"])

df = pd.concat([school_id, school_name, county_fips, suppress_student_new, suppress_student_existing, suppress_teacher_new,
                suppress_teacher_existing, suppress_staff_new, suppress_staff_existing, longitude, latitude], axis=1)
df.columns = ["school_id", "school_name", "county_fips", "suppress_student_new", "suppress_student_existing", "suppress_teacher_new",
              "suppress_teacher_existing", "suppress_staff_new", "suppress_staff_existing", "longitude", "latitude"]

# Collect and format aggregate cases data
school_id = pd.DataFrame(json["aggregate_cases"]["school_id"])
student_new_cases = pd.DataFrame(json["aggregate_cases"]["student_new_cases"])
student_total_cases = pd.DataFrame(json["aggregate_cases"]["student_total_cases"])
teacher_new_cases = pd.DataFrame(json["aggregate_cases"]["teacher_new_cases"])
teacher_total_cases = pd.DataFrame(json["aggregate_cases"]["teacher_total_cases"])
staff_new_cases = pd.DataFrame(json["aggregate_cases"]["staff_new_cases"])
staff_total_cases = pd.DataFrame(json["aggregate_cases"]["staff_total_cases"])

df2 = pd.concat([school_id, student_new_cases, student_total_cases, teacher_new_cases, teacher_total_cases, staff_new_cases, staff_total_cases], axis=1)
df2.columns = ["school_id", "student_new_cases", "student_total_cases", "teacher_new_cases", "teacher_total_cases", "staff_new_cases", "staff_total_cases"]

df2_schools = df2.iloc[1:,:]

df_full = df.merge(df2_schools, how="outer", on="school_id")

df_full.to_csv("school_data.csv", index=False)

# Collect and format statewide data
df2_statewide = df2.iloc[0:1,:]
df2_statewide.head()

df2_statewide.to_csv("statewide_data.csv", index=False)

# Save weekly statewide version
statewide_weekly = pd.read_csv("statewide_data_weekly.csv")
latest = statewide_weekly.iloc[len(statewide_weekly)-1,1]
if latest != student_total_cases.iloc[0,0]:
    today = date.today()
    date_formatted = today.strftime("%m/%d/%Y")
    sw_row = pd.DataFrame({"date":date_formatted, "students":student_total_cases.iloc[0,0], "teachers":teacher_total_cases.iloc[0,0], "staff":staff_total_cases.iloc[0,0]}, index=[0])
    statewide_weekly = statewide_weekly.append(sw_row)
    statewide_weekly.to_csv("statewide_data_weekly.csv", index=False)


# Collect and format daily school data
date = pd.DataFrame(json["daily_school_cases"]["date"])
school_id = pd.DataFrame(json["daily_school_cases"]["school_id"])
staff_existing_cases = pd.DataFrame(json["daily_school_cases"]["staff_existing_cases"])
staff_new_cases = pd.DataFrame(json["daily_school_cases"]["staff_new_cases"])
student_existing_cases = pd.DataFrame(json["daily_school_cases"]["student_existing_cases"])
student_new_cases = pd.DataFrame(json["daily_school_cases"]["student_new_cases"])
teacher_existing_cases = pd.DataFrame(json["daily_school_cases"]["teacher_existing_cases"])
teacher_new_cases = pd.DataFrame(json["daily_school_cases"]["teacher_new_cases"])
moving_average_cases_staff = pd.DataFrame(json["daily_school_cases"]["moving_average_cases_staff"])
moving_average_cases_student = pd.DataFrame(json["daily_school_cases"]["moving_average_cases_student"])
moving_average_cases_teacher = pd.DataFrame(json["daily_school_cases"]["moving_average_cases_teacher"])

df3 = pd.concat([date, school_id, staff_existing_cases, staff_new_cases, student_existing_cases, student_new_cases, teacher_existing_cases,
                 teacher_new_cases, moving_average_cases_staff, moving_average_cases_student, moving_average_cases_teacher], axis=1)
df3.columns = ["date", "school_id", "staff_existing_cases", "staff_new_cases", "student_existing_cases", "student_new_cases", "teacher_existing_cases",
               "teacher_new_cases", "moving_average_cases_staff", "moving_average_cases_student", "moving_average_cases_teacher"]

df3.to_csv("daily_school_cases.csv", index=False)
