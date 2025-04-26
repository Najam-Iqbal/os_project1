import pandas as pd

def parse_schedule(file_path):
    try:
        # Read the Excel file
        df = pd.read_excel(file_path, sheet_name='Sheet1', header=0)
        
        output = []
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        for day in days:
            start_col = f"{day}-start"
            end_col = f"{day}-end"
            day_schedule = []
            
            # Process time slots if columns exist
            if start_col in df.columns and end_col in df.columns:
                time_pairs = df[[start_col, end_col]].dropna(how='all')
                
                if not time_pairs.empty:
                    for _, row in time_pairs.iterrows():
                        for col, marker in [(start_col, '1'), (end_col, '0')]:
                            if pd.notna(row[col]):
                                time_str = (row[col].strftime('%-I:%M') 
                                          if hasattr(row[col], 'strftime') 
                                          else str(row[col]).split()[0][:-3])
                                day_schedule.append(f"{time_str}={marker}")
                else:
                    day_schedule.append("1:00=0")
            else:
                day_schedule.append("1:00=0")
            
            output.append(f"{day}: {', '.join(day_schedule)}")
        
        return "\n".join(output)
    
    except Exception as e:
        return f"Error processing file: {str(e)}"
