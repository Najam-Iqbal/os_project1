import pandas as pd

def excel_to_timetable_string(file_path):
    try:
        # Read the Excel file
        df = pd.read_excel(file_path, sheet_name='Sheet1', header=0)
        
        output = []
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        for day in days:
            start_col = f"{day}-start"
            end_col = f"{day}-end"
            day_schedule = []
            
            if start_col in df.columns and end_col in df.columns:
                time_pairs = df[[start_col, end_col]].dropna(how='all')
                
                if not time_pairs.empty:
                    for _, row in time_pairs.iterrows():
                        for col, marker in [(start_col, '1'), (end_col, '0')]:
                            if pd.notna(row[col]):
                                # Format correctly
                                if isinstance(row[col], pd.Timestamp):
                                    time_str = row[col].strftime('%H:%M')
                                else:
                                    time_str = str(row[col]).strip()
                                day_schedule.append(f"{time_str}={marker}")
                else:
                    day_schedule.append("")
            else:
                day_schedule.append("")
            
            output.append(f"{day}: {', '.join(day_schedule)}")
        
        return "\n".join(output)
    
    except Exception as e:
        return f"Error processing file: {str(e)}"
