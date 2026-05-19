import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

'''# Load dataset
df = pd.read_csv("used_car_dataset.csv")

# Print first 5 rows
print(df.head())

# Print dataset shape
print(df.shape)

# Print columns
print(df.columns)'''
import pandas as pd

df = pd.read_csv("used_car_dataset.csv")

# What type is each column?
print("Data Types:")
print(df.dtypes)
print()

# Any missing values?
print("Missing Values:")
print(df.isnull().sum())
print()

# Look at AskPrice and kmDriven closely
print("Sample AskPrice values:")
print(df['AskPrice'].head(5).tolist())
print()

print("Sample kmDriven values:")
print(df['kmDriven'].head(5).tolist())

import pandas as pd

df = pd.read_csv("used_car_dataset.csv")

# Clean AskPrice → remove ₹, commas, spaces → convert to number
df['Price'] = df['AskPrice'].str.replace('₹', '').str.replace(',', '').str.strip().astype(float)

# Clean kmDriven → remove ' km', commas → convert to number
df['km'] = df['kmDriven'].str.replace(' km', '').str.replace(',', '').str.strip()
df['km'] = pd.to_numeric(df['km'], errors='coerce')

# Verify it worked
print("Sample cleaned prices:")
print(df['Price'].head(5).tolist())
print()
print("Sample cleaned km:")
print(df['km'].head(5).tolist())
print()
print("Price column type:", df['Price'].dtype)
print("km column type:", df['km'].dtype)

print()
# How does transmission type affect price?
transmission = df.groupby('Transmission')['Price'].agg(['median', 'mean', 'count'])
print("Transmission vs Price:")
print(transmission)

# INSIGHT 1: Automatic cars command 93% price premium over manual
# (₹8.99L vs ₹4.65L median) with nearly equal listing volume
# → Transmission should be a first-level filter on platforms like Spinny


print()
print()
# How does fuel type affect price?
fuel = df.groupby('FuelType')['Price'].agg(['median', 'mean', 'count'])
print("Fuel Type vs Price:")
print(fuel)

# INSIGHT 2: Diesel median price (₹9.4L) is 79% higher than petrol (₹5.25L)
# BUT this may be confounded by car type (SUVs, MUVs tend to be diesel)
# Need to compare within same age groups to see true depreciation pattern


print()
print()
# How does owner type affect price?
owner = df.groupby('Owner')['Price'].agg(['median', 'mean', 'count'])
print("Owner Type vs Price:")
print(owner)

## INSIGHT 3: First owner cars command ₹2.35L premium over second owner
# (₹7.25L vs ₹4.90L median)
# → 'Family Transfer' badge on second owner cars could reduce buyer hesitation
# and help sellers justify better pricing


print()
print()
# Which brands dominate the market?
brands = df['Brand'].value_counts().head(10)
print("Top 10 Brands by Listings:")
print(brands)
print()
print("Top 3 brands share:", round(brands.head(3).sum() / len(df) * 100, 1), "%")


# INSIGHT 4: Top 3 brands (Maruti, Hyundai, Honda) = 53% of all listings
# Maruti alone = 28%
# → Platform UX, staff training, and search experience should be
# optimised around these 3 brands first


print()
print()
# Create age buckets
df['AgeBucket'] = pd.cut(df['Age'], 
                          bins=[0, 3, 6, 10, 15, 50],
                          labels=['0-3 yrs', '4-6 yrs', '7-10 yrs', '11-15 yrs', '15+ yrs'])

# Diesel vs Petrol median price by age group
depreciation = df[df['FuelType'].isin(['Petrol', 'Diesel'])].groupby(
    ['FuelType', 'AgeBucket'], observed=True)['Price'].median().unstack(0)

print("Median Price by Age Group (Diesel vs Petrol):")
print(depreciation)


# INSIGHT 5: Diesel holds higher absolute price across all age groups
# but carries hidden risk for buyers — DPF issues, odd-even restrictions
# → Spinny should add a risk flag on diesel cars older than 7 years
# to help buyers make informed decisions

print()
print()
# How does price drop as car gets older?
depreciation_curve = df.groupby('Age')['Price'].median().reset_index()
depreciation_curve = depreciation_curve[depreciation_curve['Age'] <= 20]
print("Median Price by Age:")
print(depreciation_curve)

# INSIGHT 6: Steepest depreciation happens in first 4 years
# Car loses roughly 40% of value by age 4
# → Buyers looking for value should target 4-6 year old cars
# → Sellers should list early before the steep drop


print()
print()
# Does higher mileage mean lower price?
# First remove nulls in km column
df_km = df.dropna(subset=['km'])

# Create km buckets
df_km['kmBucket'] = pd.cut(df_km['km'],
                            bins=[0, 30000, 60000, 100000, 150000, 999999],
                            labels=['0-30k', '30-60k', '60-100k', '100-150k', '150k+'])

km_price = df_km.groupby('kmBucket', observed=True)['Price'].agg(['median', 'count'])
print("KM Driven vs Median Price:")
print(km_price)

# INSIGHT 7: Steepest price drop happens between 0-30k and 30-60k km (38% drop)
# Price plateaus and slightly rises after 100k due to larger/expensive car types
# → Buyers should target 60-100k km range for best value
# → Platforms should highlight 'low mileage' badge for cars under 30k km

print()
print()
# Which brands hold value best?
# Only look at brands with enough listings to be meaningful (min 50 cars)
brand_price = df.groupby('Brand').agg(
    MedianPrice=('Price', 'median'),
    Count=('Price', 'count')
).reset_index()

brand_price = brand_price[brand_price['Count'] >= 50].sort_values('MedianPrice', ascending=False)
print("Brand vs Median Price (min 50 listings):")
print(brand_price.to_string(index=False))

# INSIGHT 8: MG and Kia hold value surprisingly well despite being newer brands
# Chevrolet collapsed to ₹1.99L median after exiting India in 2017
# → Brand exit risk is real — platforms should flag discontinued brands
# → Buyers should factor in service network availability, not just price

print()
print()
import matplotlib.pyplot as plt

# Chart 1: Transmission vs Median Price
trans = df.groupby('Transmission')['Price'].median() / 100000  # convert to lakhs

plt.figure(figsize=(7, 5))
bars = plt.bar(trans.index, trans.values, 
               color=['#8B5CF6', '#F59E0B'], width=0.5)

# Add value labels on top of bars
for bar, val in zip(bars, trans.values):
    plt.text(bar.get_x() + bar.get_width()/2, 
             bar.get_height() + 0.2,
             f'₹{val:.1f}L', 
             ha='center', fontweight='bold')

plt.title('Automatic vs Manual: Median Price', fontweight='bold')
plt.ylabel('Median Price (₹ Lakhs)')
plt.ylim(0, trans.max() * 1.3)
plt.tight_layout()
plt.savefig('chart1_transmission.png', dpi=150)
plt.show()
print("Chart 1 saved!")

print()
print()
# Chart 2: Diesel vs Petrol depreciation by age group
dep = df[df['FuelType'].isin(['Petrol', 'Diesel'])].groupby(
    ['FuelType', 'AgeBucket'], observed=True)['Price'].median() / 100000

dep = dep.unstack(0)

x = np.arange(len(dep.index))
w = 0.35

plt.figure(figsize=(9, 5))
bars1 = plt.bar(x - w/2, dep['Diesel'], width=w, label='Diesel', color='#EF4444', alpha=0.85)
bars2 = plt.bar(x + w/2, dep['Petrol'], width=w, label='Petrol', color='#3B82F6', alpha=0.85)

# Value labels
for bar in bars1:
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
             f'₹{bar.get_height():.1f}L', ha='center', fontsize=8)
for bar in bars2:
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
             f'₹{bar.get_height():.1f}L', ha='center', fontsize=8)

plt.xticks(x, dep.index)
plt.title('Diesel vs Petrol: Median Price by Car Age', fontweight='bold')
plt.ylabel('Median Price (₹ Lakhs)')
plt.legend()
plt.tight_layout()
plt.savefig('chart2_fuel_depreciation.png', dpi=150)
plt.show()
print("Chart 2 saved!")


# Chart 3: First vs Second Owner price distribution
first = df[df['Owner'] == 'first']['Price'].clip(0, 5000000) / 100000
second = df[df['Owner'] == 'second']['Price'].clip(0, 5000000) / 100000

plt.figure(figsize=(9, 5))
plt.hist(first, bins=40, alpha=0.6, color='#10B981',
         label=f'First Owner (n={len(first):,})', density=True)
plt.hist(second, bins=40, alpha=0.6, color='#F59E0B',
         label=f'Second Owner (n={len(second):,})', density=True)

# Median lines
plt.axvline(first.median(), color='#10B981', linestyle='--', linewidth=2)
plt.axvline(second.median(), color='#F59E0B', linestyle='--', linewidth=2)

# Labels on median lines
plt.text(first.median() + 0.3, 0.08, f'₹{first.median():.1f}L', color='#10B981', fontweight='bold')
plt.text(second.median() + 0.3, 0.06, f'₹{second.median():.1f}L', color='#F59E0B', fontweight='bold')

plt.title('Price Distribution: First vs Second Owner', fontweight='bold')
plt.xlabel('Ask Price (₹ Lakhs, capped at 50L)')
plt.ylabel('Density')
plt.legend()
plt.tight_layout()
plt.savefig('chart3_owner_price.png', dpi=150)
plt.show()
print("Chart 3 saved!")


# Chart 3: First vs Second Owner - Box Plot
fig, ax = plt.subplots(figsize=(7, 5))

first = df[df['Owner'] == 'first']['Price'].clip(0, 5000000) / 100000
second = df[df['Owner'] == 'second']['Price'].clip(0, 5000000) / 100000

ax.boxplot([first, second],
           labels=['First Owner', 'Second Owner'],
           patch_artist=True,
           boxprops=dict(facecolor='#10B981', alpha=0.6),
           medianprops=dict(color='black', linewidth=2))

ax.set_title('Price Comparison: First vs Second Owner', fontweight='bold')
ax.set_ylabel('Ask Price (₹ Lakhs, capped at 50L)')

# Add median labels
ax.text(1, first.median() + 0.5, f'Median: ₹{first.median():.1f}L',
        ha='center', fontsize=9, fontweight='bold')
ax.text(2, second.median() + 0.5, f'Median: ₹{second.median():.1f}L',
        ha='center', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('chart3_owner_price.png', dpi=150)
plt.show()
print("Chart 3 saved!")

# Chart 4: Top 10 Brands by Volume
top_brands = df['Brand'].value_counts().head(10)

plt.figure(figsize=(9, 6))
bars = plt.barh(top_brands.index[::-1], top_brands.values[::-1],
                color=['#2563EB' if i >= 7 else '#6B7280' for i in range(10)])

# Value labels
for bar, val in zip(bars, top_brands.values[::-1]):
    plt.text(bar.get_width() + 20, bar.get_y() + bar.get_height()/2,
             f'{val:,}', va='center', fontsize=9)

plt.title('Top 10 Brands by Listing Volume', fontweight='bold')
plt.xlabel('Number of Listings')
plt.tight_layout()
plt.savefig('chart4_brands.png', dpi=150)
plt.show()
print("Chart 4 saved!")

# Chart 5: Overall Depreciation Curve
depr = df.groupby('Age')['Price'].median().reset_index()
depr = depr[depr['Age'] <= 20]
depr['PriceLakh'] = depr['Price'] / 100000

plt.figure(figsize=(10, 5))
plt.fill_between(depr['Age'], depr['PriceLakh'], alpha=0.15, color='#2563EB')
plt.plot(depr['Age'], depr['PriceLakh'], color='#2563EB',
         linewidth=2.5, marker='o', markersize=5)

# Annotate key age points
for age in [0, 3, 5, 10, 15, 20]:
    row = depr[depr['Age'] == age]
    if not row.empty:
        val = row['PriceLakh'].values[0]
        plt.annotate(f'₹{val:.1f}L',
                     xy=(age, val),
                     xytext=(age + 0.3, val + 0.8),
                     fontsize=8, color='#1E293B')

plt.title('Median Price Depreciation Curve (All Cars)', fontweight='bold')
plt.xlabel('Car Age (Years)')
plt.ylabel('Median Ask Price (₹ Lakhs)')
plt.xticks(range(0, 21, 2))
plt.tight_layout()
plt.savefig('chart5_depreciation.png', dpi=150)
plt.show()
print("Chart 5 saved!")

# Chart 6: KM Driven vs Median Price
df_km = df.dropna(subset=['km'])
df_km['kmBucket'] = pd.cut(df_km['km'],
                            bins=[0, 30000, 60000, 100000, 150000, 999999],
                            labels=['0-30k', '30-60k', '60-100k', '100-150k', '150k+'])

km_price = df_km.groupby('kmBucket', observed=True)['Price'].median() / 100000

plt.figure(figsize=(9, 5))
bars = plt.bar(km_price.index, km_price.values, color='#2563EB', alpha=0.85, width=0.5)

# Value labels
for bar, val in zip(bars, km_price.values):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
             f'₹{val:.1f}L', ha='center', fontweight='bold', fontsize=10)

plt.title('KM Driven vs Median Price', fontweight='bold')
plt.xlabel('Kilometers Driven')
plt.ylabel('Median Ask Price (₹ Lakhs)')
plt.ylim(0, km_price.max() * 1.3)
plt.tight_layout()
plt.savefig('chart6_km_price.png', dpi=150)
plt.show()
print("Chart 6 saved!")


# Chart 7: Brand vs Median Price (min 50 listings)
brand_price = df.groupby('Brand').agg(
    MedianPrice=('Price', 'median'),
    Count=('Price', 'count')
).reset_index()

brand_price = brand_price[brand_price['Count'] >= 50].sort_values('MedianPrice', ascending=True)
brand_price['MedianPriceLakh'] = brand_price['MedianPrice'] / 100000

# Color code — premium vs mass market
colors = ['#EF4444' if p >= 10 else '#2563EB' if p >= 5 else '#6B7280' 
          for p in brand_price['MedianPriceLakh']]

plt.figure(figsize=(10, 8))
bars = plt.barh(brand_price['Brand'], brand_price['MedianPriceLakh'],
                color=colors, alpha=0.85)

# Value labels
for bar, val in zip(bars, brand_price['MedianPriceLakh']):
    plt.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height()/2,
             f'₹{val:.1f}L', va='center', fontsize=9)

plt.title('Brand vs Median Ask Price\n(min 50 listings)', fontweight='bold')
plt.xlabel('Median Ask Price (₹ Lakhs)')

# Legend
from matplotlib.patches import Patch
legend = [Patch(color='#EF4444', label='Premium (₹10L+)'),
          Patch(color='#2563EB', label='Mid (₹5-10L)'),
          Patch(color='#6B7280', label='Budget (under ₹5L)')]
plt.legend(handles=legend, loc='lower right')

plt.tight_layout()
plt.savefig('chart7_brand_price.png', dpi=150)
plt.show()
print("Chart 7 saved!")