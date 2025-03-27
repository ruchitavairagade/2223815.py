import pandas as pd

# Sample data based on the provided image
data = {
    "student_id": [
        101, 101, 101, 101, 101, 101, 102, 102, 102, 102,
        103, 103, 103, 103, 103, 103, 103, 103, 103, 104, 104, 104
    ],
    "attendance_date": [
        "2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05", "2024-01-06",
        "2024-02-01", "2024-02-02", "2024-02-03", "2024-02-04",
        "2024-03-01", "2024-03-02", "2024-03-03", "2024-03-04", "2024-03-05", "2024-03-06", "2024-03-07", "2024-03-08", "2024-03-09",
        "2024-04-01", "2024-04-02", "2024-04-03"
    ],
    "status": [
        "Absent", "Absent", "Absent", "Absent", "Absent", "Present",
        "Absent", "Absent", "Absent", "Present",
        "Absent", "Absent", "Absent", "Absent", "Absent", "Absent", "Absent", "Absent", "Present",
        "Absent", "Absent", "Present"
    ]
}

df = pd.DataFrame(data)
df["attendance_date"] = pd.to_datetime(df["attendance_date"])

# Function to find the latest absence streak
def find_absence_streaks(df):
    result = []
    
    for student_id, group in df.groupby("student_id"):
        group = group.sort_values("attendance_date").reset_index(drop=True)
        
        start_date = None
        prev_date = None
        absence_days = 0
        max_streak = {"start_date": None, "end_date": None, "days": 0}
        
        for _, row in group.iterrows():
            if row["status"] == "Absent":
                if start_date is None:
                    start_date = row["attendance_date"]
                    absence_days = 1
                elif prev_date and (row["attendance_date"] - prev_date).days == 1:
                    absence_days += 1
                else:
                    start_date = row["attendance_date"]
                    absence_days = 1
                
                if absence_days > max_streak["days"]:
                    max_streak = {"start_date": start_date, "end_date": row["attendance_date"], "days": absence_days}
            
            prev_date = row["attendance_date"]
        
        if max_streak["days"] > 3:
            result.append([student_id, max_streak["start_date"], max_streak["end_date"], max_streak["days"]])
    
    return pd.DataFrame(result, columns=["student_id", "absence_start_date", "absence_end_date", "total_absent_days"])

# Getting the result
df_streaks = find_absence_streaks(df)
print(df_streaks)
