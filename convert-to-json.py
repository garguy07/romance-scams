import csv
import json
import sys
import os

def csv_to_json(csv_file_path, json_file_path):
    """
    Convert CSV file to JSON format
    
    Args:
        csv_file_path (str): Path to the input CSV file
        json_file_path (str): Path to the output JSON file
    """
    
    # Check if CSV file exists
    if not os.path.exists(csv_file_path):
        print(f"Error: CSV file '{csv_file_path}' not found!")
        return False
    
    try:
        # Read CSV file and convert to JSON
        data = []
        
        with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
            # Use csv.DictReader to automatically use first row as headers
            csv_reader = csv.DictReader(csv_file)
            
            # Convert each row to a dictionary and add to data list
            for row_number, row in enumerate(csv_reader, start=2):  # Start at 2 since row 1 is headers
                try:
                    # Clean up the data - remove leading/trailing whitespace
                    cleaned_row = {key.strip(): value.strip() if value else "" for key, value in row.items()}
                    data.append(cleaned_row)
                except Exception as e:
                    print(f"Warning: Error processing row {row_number}: {e}")
                    continue
        
        # Write JSON file
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=2, ensure_ascii=False)
        
        print(f"✅ Successfully converted CSV to JSON!")
        print(f"📁 Input file: {csv_file_path}")
        print(f"📁 Output file: {json_file_path}")
        print(f"📊 Total records converted: {len(data)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error converting CSV to JSON: {e}")
        return False

def main():
    """
    Main function to run the CSV to JSON conversion
    """
    
    # Define file paths
    csv_file = "Romance Scam Dataset - Sheet1.csv"
    json_file = "Romance_Scam_Dataset.json"
    
    # Get current directory
    current_dir = os.getcwd()
    csv_path = os.path.join(current_dir, csv_file)
    json_path = os.path.join(current_dir, json_file)
    
    print("🔄 Starting CSV to JSON conversion...")
    print(f"📂 Working directory: {current_dir}")
    
    # Convert CSV to JSON
    success = csv_to_json(csv_path, json_path)
    
    if success:
        print("\n✨ Conversion completed successfully!")
        
        # Display some sample data
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                sample_data = json.load(f)
                
            print(f"\n📋 Sample of converted data (first record):")
            if sample_data:
                print(json.dumps(sample_data[0], indent=2, ensure_ascii=False)[:500] + "...")
        except Exception as e:
            print(f"Note: Could not display sample data: {e}")
    else:
        print("\n❌ Conversion failed!")

if __name__ == "__main__":
    main()