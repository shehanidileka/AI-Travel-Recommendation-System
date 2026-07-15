import pandas as pd
import os
from app import db, Place, app 

df = pd.read_csv(r'C:\Users\Hp\Desktop\Travel Project\sri_lanka_travel_data_cleaned.csv')

with app.app_context():
    db.create_all() 
    db.session.query(Place).delete()
    
    image_folder = r'C:\Users\Hp\Desktop\Travel Project\static\images'
    
    for index, row in df.iterrows():
        # 1. පින්තූරේ නම ලබාගන්න
       # මේ පේළිය වෙනස් කරන්න
        raw_name = str(row['Destination']).replace(" ", "") # නමේ තියෙන space අයින් කරනවා
        img_name = raw_name + ".jpg" # නැත්නම් .jpeg වෙන්නත් පුළුවන්
        
        # පින්තූරේ ඇත්තටම තියෙනවද බලන්න
        file_path = os.path.join(image_folder, img_name)
        if not os.path.exists(file_path):
            print(f"පින්තූරේ හමු වුණේ නැහැ: {img_name} (පාර: {file_path})")
            final_image = 'default.jpg'
        else:
            final_image = img_name
        
        # 2. පින්තූරේ ඇත්තටම ෆෝල්ඩරේ තියෙනවාද බලන්න
        if img_name and os.path.exists(os.path.join(image_folder, img_name)):
            final_image = img_name
        else:
            final_image = 'default.jpg' 
            
        # 3. Database එකට දත්ත ඇතුලත් කරන්න
        new_place = Place(
            name=row['Destination'],
            budget=row['Budget'],
            weather=row['Weather'],
            travel_method=row['Travel_Method'],
            duration=int(row['Duration']),
            image_name=final_image,
            description=row.get('Description', 'No description available'),
            location=row.get('Location', 'Sri Lanka'),
            rating=float(row.get('Rating', 0.0))
        )
        db.session.add(new_place)
        
        # 4. පින්තූරේ නම Terminal එකේ Print කරලා බලන්න
        print(f"Adding: {new_place.name} | Image Name in DB: {new_place.image_name}")
    
    db.session.commit()
    print("වැඩේ සාර්ථකයි! දත්ත ටික Database එකට දැම්මා.")