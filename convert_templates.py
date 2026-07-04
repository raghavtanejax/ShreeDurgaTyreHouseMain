import os
import re

def convert_html_files():
    templates_dir = 'c:/Users/RAGHAV TANEJA/OneDrive/Desktop/Saharanpur/ShreeDurgaTyreHouseMain/templates'
    
    # Mapping of files to their respective base templates
    public_files = [
        '9_home.html', '2_bike_scooter_tyres.html', '4_select_tyre_category.html', 
        '5_truck_crane_tyres.html', '7_car_suv_tyres.html', '8_contact_us.html'
    ]
    admin_files = [
        '1_admin_dashboard.html', '3_inventory_manager.html', '6_site_settings.html'
    ]

    for filename in os.listdir(templates_dir):
        if not filename.endswith('.html') or filename in ['base.html', 'admin_base.html', 'login.html']:
            continue
            
        filepath = os.path.join(templates_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract main content
        main_match = re.search(r'<main[^>]*>(.*?)</main>', content, flags=re.DOTALL | re.IGNORECASE)
        if not main_match:
            print(f"Could not find <main> in {filename}")
            continue

        main_content = main_match.group(1)

        # Fix image paths
        # From src="https://lh3.googleusercontent.com/..." to src="{{ url_for('static', filename='images/filename.png') }}"
        # Wait, the images I downloaded were named 1_admin_dashboard.png, etc.
        # But in the HTML, they have long googleusercontent URLs.
        # It's better to just use the images they already have (the hosted ones) or replace them.
        # The prompt says: "I have a workspace containing 9 static HTML files and their corresponding images generated from Google Stitch... Convert these static frontend assets..."
        # If I want to replace the image tags with the downloaded ones, it's tricky because I downloaded 9 images (screenshots of the full page, not the individual images!).
        # Wait, the prompt says "9 static HTML files and their corresponding images generated from Google Stitch". The images generated from Stitch are the SCREENSHOTS, not the embedded assets. The embedded assets are still hosted on googleusercontent.
        # I should just leave the `src` as is, they are valid remote URLs, OR they meant the screenshots.
        # Actually, let's leave the `src` untouched to ensure Pixel-Perfect design!
        
        base_ext = 'admin_base.html' if filename in admin_files else 'base.html'
        
        new_content = f"{{% extends '{base_ext}' %}}\n{{% block content %}}\n{main_content}\n{{% endblock %}}"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"Converted {filename}")

if __name__ == '__main__':
    convert_html_files()
