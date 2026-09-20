import os
import requests
# FIXED: Proper class import configuration for pypdf
import pypdf

# Explicit user exceptions to filter out
EXCLUDED_SUBJECTS = {
    "home science", "homescience", 
    "urdu", 
    "botanical education", "botany", "botanical",
    "health education", "healtheducation", "physical education", 
    "skill education", "vocational",
    "arts", "fine arts", "art",
    "sanskrit"
}

# Dictionary mapping allowed subject codes to their structural IDs
# Excluded subjects are omitted from this core target dictionary
ALLOWED_CATALOGS = {
    "Mathematics": ["aamh1", "bemh1", "cemh1"], 
    "Science": ["aes1", "bes1"],
    "Physics": ["aeph1", "beph1"],
    "Chemistry": ["aech1", "bech1"],
    "History": ["aehs1", "behs1"],
    "English": ["aeen1", "been1"]
}

def is_excluded(subject_name):
    return subject_name.lower().strip() in EXCLUDED_SUBJECTS

def fetch_and_compile():
    print("Initializing NCERT individual chapter fetcher...")
    os.makedirs("temp_chapters", exist_ok=True)
    
    # FIXED: Initializing merger class cleanly via root instance reference
    pdf_merger = pypdf.PdfMerger()
    download_counter = 0

    # Iterating classes 1 to 12
    for class_num in range(1, 13):
        for subject_title, book_codes in ALLOWED_CATALOGS.items():
            if is_excluded(subject_title):
                print(f"Skipping exception: {subject_title}")
                continue
                
            for code in book_codes:
                # Loop through standard chapter sequence index structures (up to 15 chapters per book)
                for ch_num in range(1, 16):
                    chapter_str = f"{ch_num:02d}"
                    target_url = f"https://ncert.nic.in{code}{chapter_str}.pdf"
                    
                    try:
                        response = requests.head(target_url, timeout=5)
                        if response.status_code == 200:
                            print(f"Fetching Chapter: Class {class_num} - {subject_title} (Ch {ch_num})")
                            
                            file_data = requests.get(target_url, timeout=10)
                            temp_path = f"temp_chapters/{code}_{chapter_str}.pdf"
                            
                            with open(temp_path, "wb") as f:
                                f.write(file_data.content)
                            
                            pdf_merger.append(temp_path)
                            download_counter += 1
                        else:
                            break
                    except Exception as e:
                        print(f"Skipping unavailable index node: {e}")
                        break

    if download_counter > 0:
        output_filename = "compiled_ncert_library.pdf"
        print(f"Compiling {download_counter} chapters into 1 final document: {output_filename}...")
        
        with open(output_filename, "wb") as out_file:
            pdf_merger.write(out_file)
            
        pdf_merger.close()
        print("Master compilation complete successfully!")
    else:
        print("No match items downloaded. Output generation aborted.")

if __name__ == "__main__":
    fetch_and_compile()
