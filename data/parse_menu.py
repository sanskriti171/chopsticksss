import re
import json
import os

def parse_menu():
    filepath = r"H:\My Drive\new-coding-stuff\data.md"
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract the menu items section (after '## Menu items with prices')
    parts = content.split("## Menu items with prices")
    if len(parts) < 2:
        print("Could not find '## Menu items with prices' in data.md")
        return
    menu_section = parts[-1].strip()

    # Clean up HTML entities
    menu_section = menu_section.replace("&pound;", "£").replace("&pound", "£")
    
    # Match item number, name/desc, and price
    # e.g., "1 Chicken Sweet Corn Soup £4.30"
    # We use a negative lookbehind to avoid matching decimals (like .50 in 8.50)
    # and restrict numbers to 1-3 digits with 0-2 trailing letters.
    pattern = r"(?<!\.)\b(\d{1,3}[A-Za-z]{0,2})\s+(.*?)\s*£\s*(\d+\.\d{2})"
    matches = list(re.finditer(pattern, menu_section))

    menu_data = {}
    current_category = "Chinese Soup"
    
    categories = [
        "Chinese Soup", "Appetisers", "Fried Rice Dishes", "Chow Mein Dishes (Soft Noodles)",
        "Salt & Pepper Dishes", "Curry Dishes", "Sweet & Sour Dishes", "Spare Ribs Dishes",
        "Chicken Dishes", "Beef Dishes", "Pork Dishes", "King Prawn Dishes", "Duck Dishes",
        "Vegetables Dishes", "Chop Suey Dishes (Beansprouts)", "Pineapple & Tomato Dishes",
        "Satay Dishes", "Szechuan Dishes", "Egg Foo Yung Dishes", "English Dishes (Chips Includes)",
        "Chopstick Special Dishes", "Side Orders", "Special Set Dinner"
    ]

    for i, match in enumerate(matches):
        num = match.group(1)
        name_desc = match.group(2).strip()
        price = match.group(3)
        
        # Check text preceding the match for a category name
        if i == 0:
            pre_text = menu_section[:match.start()].strip()
        else:
            pre_text = menu_section[matches[i-1].end():match.start()].strip()
        
        for cat in categories:
            # We match by looking for category headers in the intermediate text
            if cat.lower() in pre_text.lower():
                current_category = cat
                break
        
        # Parse description if present
        name = name_desc
        description = ""
        
        # Split description based on common text cues
        if "Served with" in name_desc:
            parts = name_desc.split("Served with", 1)
            name = parts[0].strip()
            description = "Served with " + parts[1].strip()
        elif "wrapped in" in name_desc:
            parts = name_desc.split("wrapped in", 1)
            name_words = parts[0].strip().split(" ")
            name = " ".join(name_words[:-2]).strip()
            description = " ".join(name_words[-2:]).strip() + " wrapped in " + parts[1].strip()
        elif "Accompanied by" in name_desc:
            parts = name_desc.split("Accompanied by", 1)
            name_words = parts[0].strip().split(" ")
            name = " ".join(name_words[:-2]).strip()
            description = " ".join(name_words[-2:]).strip() + " Accompanied by " + parts[1].strip()
        elif "Stir Fried with" in name_desc:
            parts = name_desc.split("Stir Fried with", 1)
            name_words = parts[0].strip().split(" ")
            name = " ".join(name_words[:-2]).strip()
            description = " ".join(name_words[-2:]).strip() + " Stir Fried with " + parts[1].strip()
        elif "Wok Fried with" in name_desc:
            parts = name_desc.split("Wok Fried with", 1)
            name_words = parts[0].strip().split(" ")
            name = " ".join(name_words[:-2]).strip()
            description = " ".join(name_words[-2:]).strip() + " Wok Fried with " + parts[1].strip()
        
        # If there's an allergy note in the name, e.g. "(For 2 Person)", keep it in the name.
        
        item = {
            "number": num,
            "name": name,
            "description": description,
            "price": f"£{price}"
        }
        
        if current_category not in menu_data:
            menu_data[current_category] = []
        menu_data[current_category].append(item)

    # Save to JSON
    os.makedirs(r"H:\My Drive\new-coding-stuff\data", exist_ok=True)
    out_path = r"H:\My Drive\new-coding-stuff\data\menu.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(menu_data, f, indent=4, ensure_ascii=False)
    
    print(f"Successfully parsed {len(matches)} items into {len(menu_data)} categories.")

if __name__ == "__main__":
    parse_menu()
