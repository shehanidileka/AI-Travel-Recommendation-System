import pandas as pd

# 1. CSV දත්ත සමුදාය පද්ධතියට ඇතුළත් කිරීම (Reading the Dataset)
try:
    # ඔබේ Excel ගොනුවේ නම මෙහි නිවැරදිව තිබිය යුතුය
    df = pd.read_csv('travel_data.csv')
except FileNotFoundError:
    print("❌ Error: 'travel_data.csv' ගොනුව සොයාගත නොහැකි විය!")
    print("💡 උපදෙස: මෙම Python කේතය ඇති Folder එක ඇතුළතම ඔබේ CSV ගොනුවද තබන්න.")
    exit()

print("======================================================")
print(" 🌐 SMART TRAVEL PLANNER USING AI - HNDIT PROJECT 🌐 ")
print("======================================================\n")

print("🤖 ඔබගේ සංචාරක මනාපයන් (Preferences) ඇතුළත් කරන්න:\n")

# 2. පරිශීලකයාගෙන් Inputs ලබා ගැනීම (User Inputs)
user_budget = input("1. ඔබගේ අයවැය (Low / Medium / High): ").strip().capitalize()
user_weather = input("2. බලාපොරොත්තු වන දේශගුණය (Hot / Cold): ").strip().capitalize()
user_transport = input("3. ප්‍රිය කරන ගමන් මාධ්‍යය (Train / Bus / Car / Walking): ").strip().capitalize()

# දින ගණන සඳහා අකුරු ඇතුළත් කළහොත් සිදුවන වැරදි වැළැක්වීමට (Error Handling)
try:
    user_days = int(input("4. ගත කිරීමට බලාපොරොත්තු වන උපරිම දින ගණන: "))
except ValueError:
    print("❌ වැරදි ආදානයකි! දින ගණන සඳහා ඉලක්කමක් පමණක් ඇතුළත් කරන්න.")
    exit()

# 3. AI / Rule-based Filtering ක්‍රියාවලිය (Data Processing)
# පරිශීලකයා ලබාදුන් අගයන් CSV එකේ ඇති දත්ත සමඟ සංසන්දනය කර ගැලපෙන ඒවා පමණක් වෙන් කරගනී.
filtered_destinations = df[
    (df['Budget'].str.strip().str.capitalize() == user_budget) & 
    (df['Weather'].str.strip().str.capitalize() == user_weather) & 
    (df['Travel_Method'].str.strip().str.capitalize() == user_transport) & 
    (df['Duration'] <= user_days)
]

# 4. ප්‍රතිඵල නිර්දේශ කිරීම (Output Recommendations)
print("\n------------------------------------------------------")
print("🤖 AI මඟින් ඔබට ගැළපෙනම සංචාරක ස්ථාන නිර්දේශ කරයි:")
print("------------------------------------------------------")

# ගැළපෙන ස්ථාන හමු වී තිබේදැයි පරීක්ෂා කිරීම
if not filtered_destinations.empty:
    count = 1
    for index, row in filtered_destinations.iterrows():
        print(f"{count}) 📍 ස්ථානය: {row['Destination']}")
        print(f"   ℹ️ විස්තරය: දින {row['Duration']} කට සෑහේ | අයවැය: {row['Budget']} | දේශගුණය: {row['Weather']}")
        print("   ---------------------------------------------------")
        count += 1
else:
    print("❌ කණගාටුයි! ඔබ ලබාදුන් සියලුම මනාපයන්ට ගැළපෙන ස්ථානයක් අප සතු දත්තවල නැත.")
    print("💡 උපදෙස: ඔබේ අයවැය, ගමන් මාධ්‍යය හෝ දින ගණන වෙනස් කර නැවත උත්සාහ කරන්න.")