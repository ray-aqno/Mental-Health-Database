"""
Automated Script: Scrape and Import College Mental Health Data
Runs the entire pipeline: Scrape → Save JSON → Import to Database
"""

import sys
import time
import json
from pathlib import Path


def check_dependencies():
    """Check if required packages are installed"""
    print("Checking dependencies...")
    required = ['requests', 'bs4']
    missing = []
    
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"❌ Missing packages: {', '.join(missing)}")
        print("Install them with: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies installed\n")
    return True


def run_scraper():
    """Run the simple scraper"""
    print("="*70)
    print("STEP 1: SCRAPING COLLEGE MENTAL HEALTH RESOURCES")
    print("="*70)
    print()
    
    try:
        from simple_scraper import SimpleCollegeScraper
        
        scraper = SimpleCollegeScraper()
        data = scraper.scrape_all_colleges()
        
        if data:
            scraper.save_to_json('scraped_colleges_data.json')
            print(f"\n✅ Successfully scraped {len(data)} colleges")
            return True
        else:
            print("\n❌ No data was scraped")
            return False
            
    except Exception as e:
        print(f"\n❌ Error during scraping: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def verify_scraped_data():
    """Verify the scraped data file exists and is valid"""
    print("\n" + "="*70)
    print("STEP 2: VERIFYING SCRAPED DATA")
    print("="*70)
    print()
    
    json_file = Path('scraped_colleges_data.json')
    
    if not json_file.exists():
        print("❌ scraped_colleges_data.json not found")
        return False
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"✅ JSON file is valid")
        print(f"   Total colleges: {len(data)}")
        
        total_resources = sum(len(college.get('resources', [])) for college in data)
        print(f"   Total resources: {total_resources}")
        
        print("\nColleges found:")
        for college in data:
            resources_count = len(college.get('resources', []))
            print(f"   • {college['name']}: {resources_count} resource(s)")
        
        return True
        
    except json.JSONDecodeError:
        print("❌ Invalid JSON format")
        return False
    except Exception as e:
        print(f"❌ Error reading file: {str(e)}")
        return False


def check_api_status():
    """Check if the API is running"""
    try:
        import requests
        response = requests.get('http://localhost:58346/api/colleges', timeout=3)
        return True
    except:
        return False


def import_to_database():
    """Import scraped data to database via API"""
    print("\n" + "="*70)
    print("STEP 3: IMPORTING TO DATABASE")
    print("="*70)
    print()
    
    # Check if API is running
    if not check_api_status():
        print("⚠️  API is not running!")
        print("\nPlease start the ASP.NET backend in another terminal:")
        print("   cd ..")
        print("   dotnet run")
        print("\nThen run this script again, or manually import with:")
        print("   python -c \"from data_importer import DataImporter; DataImporter().import_colleges_from_json('scraped_colleges_data.json')\"")
        return False
    
    print("✅ API is running\n")
    
    try:
        from importer import run_import
        
        run_import(
            filepath='scraped_colleges_data.json',
            base_url='http://localhost:58346/api',
            api_key='',
        )
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during import: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def display_next_steps():
    """Display next steps for the user"""
    print("\n" + "="*70)
    print("✅ PIPELINE COMPLETE!")
    print("="*70)
    print("\n🎉 Next Steps:")
    print("   1. Open your browser to: http://localhost:58346")
    print("   2. View the interactive map with college pins")
    print("   3. Click on pins to see mental health resources")
    print("   4. Verify all data is accurate")
    print("\n📝 To update data:")
    print("   • Run this script again to re-scrape")
    print("   • Or manually edit scraped_colleges_data.json")
    print("   • Then re-import with importer.py")
    print("\n" + "="*70 + "\n")


def main():
    """Main pipeline execution"""
    print("\n" + "="*70)
    print("COLLEGE MENTAL HEALTH RESOURCE SCRAPER & IMPORTER")
    print("="*70)
    print("\nThis script will:")
    print("   1. Scrape mental health resources from 10 colleges")
    print("   2. Save data to scraped_colleges_data.json")
    print("   3. Import data to your SQL database via API")
    print()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Ask user for confirmation
    print("⚠️  This will take several minutes due to polite scraping delays.")
    response = input("Continue? (y/n): ").strip().lower()
    if response != 'y':
        print("Cancelled.")
        sys.exit(0)
    
    print()
    
    # Step 1: Scrape
    if not run_scraper():
        print("\n❌ Scraping failed. Exiting.")
        sys.exit(1)
    
    # Step 2: Verify
    if not verify_scraped_data():
        print("\n❌ Data verification failed. Exiting.")
        sys.exit(1)
    
    # Step 3: Import
    print("\nReady to import to database.")
    response = input("Continue with import? (y/n): ").strip().lower()
    if response == 'y':
        if import_to_database():
            display_next_steps()
        else:
            print("\n⚠️  Import step failed, but data is saved in scraped_colleges_data.json")
            print("You can manually import later when the API is running.")
    else:
        print("\nImport skipped. Data saved in scraped_colleges_data.json")
        print("To import later, run:")
        print("   python data_importer.py")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Script interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
