import csv
import os
from collections import defaultdict

def csv_to_timetable_string(csv_file_path):
    """Convert any CSV timetable to the specified string format"""
    try:
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            # Read CSV and clean rows
            rows = list(csv.reader(file))
            rows = [[cell.strip() for cell in row] for row in rows if any(cell.strip() for cell in row)]
            
            # Detect time slots (looking for time-like patterns)
            time_slots = []
            for cell in rows[1]:  # Assuming header is in row 1
                if any(c.isdigit() for c in cell) and ':' in cell:  # Basic time format detection
                    time_slots.append(cell)
            
            if not time_slots:
                return "Error: No time slots found in header row"
            
            # Process each day
            result = []
            for row in rows[2:]:  # Assuming data starts at row 2
                if not row or not row[0]:  # Skip empty rows
                    continue
                
                day = row[0]
                entries = []
                prev_time = None
                
                # Map cells to time slots
                time_values = defaultdict(lambda: '0')
                for i, time in enumerate(time_slots):
                    if i*2+1 < len(row):  # Check if data exists for this time slot
                        cell_value = row[i*2+1]
                        time_values[time] = '1' if cell_value else '0'
                
                # Generate output string
                for i, time in enumerate(time_slots):
                    # Mark last slot as 0
                    value = '0' if i == len(time_slots)-1 else time_values[time]
                    entries.append(f"{time}={value}")
                
                result.append(f"{day}: {', '.join(entries)}")
            
            return '\n'.join(result)
    
    except Exception as e:
        return f"Error: {str(e)}"
