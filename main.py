from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.container import BarContainer

BASE_DIR = Path(__file__).resolve().parent

df = pd.read_csv(BASE_DIR / 'data/raw/data of gurugram real Estate.csv')

# Data Cleaning

df.columns = df.columns.str.strip().str.replace(' ', '_').str.lower()

df = df.drop_duplicates()

#Numeric Columns Cleaning

df['price'] = df['price'].astype(str).str.replace(',', '').astype(float)

df['area'] = df['area'].astype(str).str.replace(',', '').astype(int)

df['rate_per_sqft'] = df['rate_per_sqft'].astype(str).str.replace(',', '').astype(int)

#Categorical Columns Cleaning

df['status'] = df['status'].str.strip().str.lower()

df['rera_approval'] = df['rera_approval'].str.strip().str.lower().map({'approved by rera': True, 'not approved by rera': False})

df['flat_type'] = df['flat_type'].str.strip().str.lower()

df = df.drop_duplicates()

# convert all string to object type

for col in df.select_dtypes(include='object').columns:

    df[col] = df[col].astype('object')

# Which is the costliest flat in the dataset?

costliest_flat = df.loc[df['price'].idxmax()]

print(costliest_flat)

print(f"The costliest flat is a {costliest_flat['bhk_count']} BHK flat with a price of {costliest_flat['price']/10000000} Crores, in {costliest_flat['society']} society.")

# Which locality has the highest average price?

highest_avg_price_locality = df.groupby('locality')['price'].mean().idxmax()

print(f"The locality with the highest average price is {highest_avg_price_locality}.")

# Which locality has the highest rate per square foot?

highest_avg_rate_locality = df.groupby('locality')['rate_per_sqft'].mean().idxmax()

print(f"The locality with the highest average rate per square foot is {highest_avg_rate_locality}.")

# Do ready-to-move properties cost more than under-construction properties?

ready_to_move_avg_price = df[df['status'] == 'ready to move']['price'].mean()

under_construction_avg_price = df[df['status'] == 'under construction']['price'].mean()

if ready_to_move_avg_price > under_construction_avg_price:

    print(f"Ready-to-move properties cost more on average than under-construction properties.")

else:

    print(f"Under-construction properties cost more on average than ready-to-move properties.")

# Do RERA-approved properties command a price premium?

rera_approved_avg_price = df[df['rera_approval'] == True]['price'].mean()

non_rera_approved_avg_price = df[df['rera_approval'] == False]['price'].mean()

if rera_approved_avg_price > non_rera_approved_avg_price:

    print(f"RERA-approved properties command a price premium on average.")

else:

    print(f"RERA-approved properties do not command a price premium on average.")

# How does area (sqft) impact property price?

sns.scatterplot(data=df, x='area', y='price')

plt.close()

# Which BHK configuration is the most expensive on average?

most_expensive_bhk = df.groupby('bhk_count')['rate_per_sqft'].mean().idxmax()

print(f"The most expensive BHK configuration on average is {most_expensive_bhk} BHK.")

# Which property type (Apartment, Floor, Plot) is the costliest?

most_expensive_property_type = df.groupby('property_type')['rate_per_sqft'].mean().idxmax()

print(f"The costliest property type is {most_expensive_property_type}.")

# Do certain builders or companies consistently price higher?

#print(df.groupby('company_name')['rate_per_sqft'].mean().sort_values(ascending=False).head(5))

#Print name of top 5 companies

top_5_companies = df.groupby('company_name')['rate_per_sqft'].mean().sort_values(ascending=False).head(5)

print("Top 5 companies taht price higher are:", end=" ")

for company in top_5_companies.index:

    print(company, end=", ")

# Are larger homes always more expensive per square foot?

sns.scatterplot(data=df, x='area', y='rate_per_sqft')

plt.close()


# 1: DATA QUALITY AUDIT

print("\n===== DATA QUALITY REPORT =====")

# 1. Dataset dimensions

print("\nDataset Shape:")

print(df.shape)

# 2. Column names and data types

print("\nColumn Information:")

df.info()

# 3. Missing values

print("\nMissing Values:")

print(df.isnull().sum())

# 4. Duplicate records

print("\nDuplicate Records:")

print(df.duplicated().sum())

# 5. Numerical summary

print("\nStatistical Summary:")

print(df.describe())

# 6. Property status distribution

print("\nProperty Status:")

print(df['status'].value_counts())

# 7. RERA approval distribution

print("\nRERA Approval:")

print(df['rera_approval'].value_counts(dropna=False))


# 2: OUTLIER INVESTIGATION

# Find properties with unusually large areas

print("\n===== LARGEST PROPERTIES =====")

print(

    df.nlargest(10, 'area')[

        ['locality', 'property_type', 'area',

         'price', 'bhk_count']

    ].to_string(index=False)

)

# Find properties with unusual BHK counts

print("\n===== HIGHEST BHK COUNTS =====")

print(

    df.nlargest(10, 'bhk_count')[

        ['locality', 'property_type', 'area',

         'bhk_count', 'price']

    ].to_string(index=False)

)

# Find the most expensive properties

print("\n===== MOST EXPENSIVE PROPERTIES =====")

print(

    df.nlargest(10, 'price')[

        ['locality', 'property_type', 'area',

         'price', 'rate_per_sqft']

    ].to_string(index=False)

)

# Investigate area distribution

print("\n===== AREA PERCENTILES =====")

print(

    df['area'].quantile(

        [0.01, 0.25, 0.50, 0.75, 0.95, 0.99]

    )

)


# 3: PROPERTY DATA VALIDATION

# 1. Count property categories

print("\n===== PROPERTY TYPES =====")

print(df['property_type'].value_counts().to_string())

# 2. Check suspicious BHK values

print("\n===== SUSPICIOUS BHK VALUES =====")

suspicious_bhk = df[

    (df['bhk_count'] > 10) |

    (df['bhk_count'] < 0)

]

print("Suspicious records:", len(suspicious_bhk))

print(

    suspicious_bhk[

        ['locality', 'property_type', 'bhk_count']

    ].head(15).to_string(index=False)

)

# 3. Examine BHK counts for plots

print("\n===== PLOT BHK DISTRIBUTION =====")

plot_records = df[

    df['property_type'].str.contains(

        'plot', case=False, na=False

    )

]

print("Plot records:", len(plot_records))

print(

    plot_records['bhk_count']

    .value_counts()

    .head(15)

)

# 4. Check extreme areas

print("\n===== EXTREME AREA RECORDS =====")

extreme_area = df[df['area'] > 10000]

print("Properties above 10,000 sqft:", len(extreme_area))

print(

    extreme_area['property_type']

    .value_counts()

    .head(10)

)


# 4: FEATURE ENGINEERING

# Create a working copy

df_clean = df.copy()

# Categorize properties

def categorize_property(property_name):

    name = str(property_name).lower()

    if 'plot' in name:

        return 'Plot'

    elif 'independent floor' in name:

        return 'Independent Floor'

    elif 'apartment' in name:

        return 'Apartment'

    elif 'villa' in name:

        return 'Villa'

    elif 'independent house' in name:

        return 'Independent House'

    elif 'penthouse' in name:

        return 'Penthouse'

    else:

        return 'Other'

# Apply the function

df_clean['property_category'] = (

    df_clean['property_type']

    .apply(categorize_property)

)

# Inspect the new categories

print("\n===== PROPERTY CATEGORIES =====")

print(

    df_clean['property_category']

    .value_counts()

)

# Correct BHK for plot listings

df_clean.loc[

    df_clean['property_category'] == 'Plot',

    'bhk_count'

] = float('nan')

print("\n===== BHK VALIDATION =====")

print(

    df_clean.groupby('property_category')

    ['bhk_count'].agg(['count', 'min', 'max'])

)


# 5: FINAL DATA VALIDATION

# Investigate properties with more than 10 BHK

high_bhk = df_clean[

    (df_clean['bhk_count'] > 10) &

    (df_clean['property_category'] != 'Plot')

]

print("\n===== HIGH BHK PROPERTIES =====")

print("Total records:", len(high_bhk))

print(

    high_bhk[

        ['locality', 'property_type',

         'property_category', 'bhk_count',

         'area', 'price']

    ].to_string(index=False)

)

# Check for invalid numerical values

print("\n===== INVALID NUMERICAL VALUES =====")

print("Price <= 0:",

      (df_clean['price'] <= 0).sum())

print("Area <= 0:",

      (df_clean['area'] <= 0).sum())

print("Rate per sqft <= 0:",

      (df_clean['rate_per_sqft'] <= 0).sum())

# Check consistency between price, area and rate

df_clean['calculated_rate'] = (

    df_clean['price'] / df_clean['area']

)

df_clean['rate_difference_pct'] = (

    abs(

        df_clean['calculated_rate']

        - df_clean['rate_per_sqft']

    )

    / df_clean['rate_per_sqft']

    * 100

)

print("\n===== PRICE CONSISTENCY =====")

print("Listings with > 10% rate difference:",

      (df_clean['rate_difference_pct'] > 10).sum())

print(

    df_clean.nlargest(

        10, 'rate_difference_pct'

    )[

        ['property_type', 'price', 'area',

         'rate_per_sqft', 'calculated_rate',

         'rate_difference_pct']

    ].to_string(index=False)

)


# 6: CREATE CLEANED DATASET

# Create the output directory if needed

output_dir = BASE_DIR / "data/processed"

output_dir.mkdir(parents=True, exist_ok=True)

# Flag inconsistent price-per-sqft records

df_clean['rate_consistent'] = (

    df_clean['rate_difference_pct'] <= 10

)

# Create price in crores for easier analysis

df_clean['price_crore'] = (

    df_clean['price'] / 10000000

)

# Create a reliable calculated rate

df_clean['price_per_sqft_calculated'] = (

    df_clean['price'] / df_clean['area']

)

# Create a separate dataset for rate analysis

df_rate_analysis = df_clean[

    df_clean['rate_consistent']

].copy()

# Save cleaned data

df_clean.to_csv(

    output_dir / "gurugram_cleaned.csv",

    index=False

)

# Save rate-analysis data

df_rate_analysis.to_csv(

    output_dir / "gurugram_rate_analysis.csv",

    index=False

)

print("\n===== CLEANED DATASET SAVED =====")

print("Full dataset:", df_clean.shape)

print("Rate analysis dataset:", df_rate_analysis.shape)

print("Flagged records:",

      (~df_clean['rate_consistent']).sum())


# 7: PROPERTY MARKET OVERVIEW

sns.set_theme(style="whitegrid")

# Calculate property category counts

category_counts = (

    df_clean['property_category']

    .value_counts()

)

# Calculate median price by category

category_prices = (

    df_clean.groupby('property_category')

    ['price_crore']

    .median()

    .sort_values(ascending=False)

)

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Chart 1: Property distribution

sns.barplot(

    x=category_counts.values,

    y=category_counts.index,

    ax=axes[0],

    color="#C49A6C"

)

axes[0].set_title(

    "Property Listings by Category",

    fontsize=14,

    fontweight="bold"

)

axes[0].set_xlabel("Number of Listings")

axes[0].set_ylabel("")

# Chart 2: Median property prices

sns.barplot(

    x=category_prices.values,

    y=category_prices.index,

    ax=axes[1],

    color="#526D82"

)

axes[1].set_title(

    "Median Property Price by Category",

    fontsize=14,

    fontweight="bold"

)

axes[1].set_xlabel("Median Price (INR Crores)")

axes[1].set_ylabel("")

# Add chart values

for ax in axes:

    for container in ax.containers:

        ax.bar_label(

            container,

            fmt="%.2f" if ax == axes[1] else "%.0f",

            padding=4

        )

plt.suptitle(

    "Gurugram Real Estate | Market Overview",

    fontsize=18,

    fontweight="bold"

)

plt.tight_layout(rect=(0.02, 0.02, 0.98, 0.94))

plt.subplots_adjust(wspace=0.45)

plt.savefig(

    BASE_DIR / "reports/figures/market_overview.png",

    dpi=300,

    bbox_inches="tight"

)

plt.close()

print("\n===== MARKET OVERVIEW =====")

print("\nProperty distribution:")

print(category_counts)

print("\nMedian prices (Crores):")

print(category_prices.round(2))


# 8: LOCALITY PRICE INTELLIGENCE

# Filter apartments with consistent rates

apartment_df = df_rate_analysis[

    df_rate_analysis['property_category'] == 'Apartment'

].copy()

locality_analysis = (

    apartment_df.groupby('locality')

    .agg(

        listing_count=('price', 'size'),

        median_price_crore=('price_crore', 'median'),

        median_rate_sqft=('price_per_sqft_calculated', 'median')

    )

    .reset_index()

)

# Only localities with at least 20 listings

locality_analysis = locality_analysis[

    locality_analysis['listing_count'] >= 20

].copy()

# Top 10 premium localities

top_localities = (

    locality_analysis

    .sort_values('median_rate_sqft', ascending=False)

    .head(10)

)

print("\n===== TOP 10 PREMIUM LOCALITIES =====")

print(top_localities.to_string(index=False))

plt.figure(figsize=(12, 7))

ax = sns.barplot(

    data=top_localities,

    x='median_rate_sqft',

    y='locality',

    color="#526D82"

)

plt.title(

    "Top 10 Premium Apartment Localities in Gurugram",

    fontsize=16,

    fontweight="bold",

    pad=20

)

plt.xlabel("Median Asking Price per Sqft (INR)")

plt.ylabel("")

for container in ax.containers:

    if isinstance(container, BarContainer):

        ax.bar_label(

            container,

            fmt="%.0f",

            padding=5

        )

plt.xlim(0, top_localities['median_rate_sqft'].max() * 1.18)

plt.tight_layout()

plt.savefig(

    BASE_DIR / "reports/figures/top_10_premium_localities.png",

    dpi=300,

    bbox_inches="tight"

)

plt.close()


# 9: AFFORDABLE LOCALITY ANALYSIS

# Find 10 localities with lowest median rate

affordable_localities = (

    locality_analysis

    .sort_values('median_rate_sqft', ascending=True)

    .head(10)

)

print("\n===== TOP 10 AFFORDABLE LOCALITIES =====")

print(

    affordable_localities.to_string(index=False)

)

plt.figure(figsize=(12, 7))

ax = sns.barplot(

    data=affordable_localities,

    x='median_rate_sqft',

    y='locality',

    color="#C49A6C"

)

plt.title(

    "Top 10 Relatively Affordable Apartment Localities",

    fontsize=16,

    fontweight="bold",

    pad=20

)

plt.xlabel("Median Asking Price per Sqft (INR)")

plt.ylabel("")

from matplotlib.container import BarContainer

for container in ax.containers:

    if isinstance(container, BarContainer):

        ax.bar_label(

            container,

            fmt="%.0f",

            padding=5

        )

plt.xlim(

    0,

    affordable_localities['median_rate_sqft'].max() * 1.2

)

plt.tight_layout()

plt.savefig(

    BASE_DIR / "reports/figures/top_10_affordable_localities.png",

    dpi=300,

    bbox_inches="tight"

)

plt.close()


# 10: AREA VS PRICE ANALYSIS

# Use apartment listings with consistent rates

area_analysis = apartment_df.copy()

# Calculate 99th percentile of area

area_limit = area_analysis['area'].quantile(0.99)

# Restrict visualizations to typical area range

area_visual = area_analysis[

    area_analysis['area'] <= area_limit

].copy()

# Calculate Spearman correlations on full

# apartment analysis data

price_corr = area_analysis['area'].corr(

    area_analysis['price_crore'],

    method='spearman'

)

rate_corr = area_analysis['area'].corr(

    area_analysis['price_per_sqft_calculated'],

    method='spearman'

)

print("\n===== AREA VS PRICE ANALYSIS =====")

print(f"Area 99th percentile: {area_limit:.0f} sqft")

print(f"Area vs Total Price: {price_corr:.3f}")

print(f"Area vs Price per Sqft: {rate_corr:.3f}")

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

sns.regplot(

    data=area_visual,

    x='area',

    y='price_crore',

    ax=axes[0],

    scatter_kws={'alpha': 0.18, 's': 12},

    line_kws={'color': '#C49A6C'},

    ci=None

)

axes[0].set_title("Apartment Area vs Total Asking Price")

axes[0].set_xlabel("Area (sqft)")

axes[0].set_ylabel("Asking Price (INR Crores)")

sns.scatterplot(

    data=area_visual,

    x='area',

    y='price_per_sqft_calculated',

    ax=axes[1],

    alpha=0.2,

    s=15,

    color="#526D82"

)

axes[1].set_title("Apartment Area vs Asking Rate")

axes[1].set_xlabel("Area (sqft)")

axes[1].set_ylabel("Asking Price per Sqft (INR)")

plt.suptitle(

    "Gurugram Apartment Market | Size & Pricing",

    fontsize=17,

    fontweight="bold"

)

plt.tight_layout(rect=(0, 0, 1, 0.94))

plt.savefig(

    BASE_DIR / "reports/figures/area_vs_price.png",

    dpi=300,

    bbox_inches="tight"

)

plt.close()


# 11: BHK CONFIGURATION ANALYSIS

# Use apartment data with valid BHK counts

bhk_df = apartment_df[

    apartment_df['bhk_count'].notna()

    & (apartment_df['bhk_count'] > 0)

].copy()

# Calculate BHK-level statistics

bhk_analysis = (

    bhk_df.groupby('bhk_count')

    .agg(

        listing_count=('price', 'size'),

        median_price_crore=('price_crore', 'median'),

        median_rate_sqft=('price_per_sqft_calculated', 'median')

    )

    .reset_index()

)

# Keep configurations with at least 20 listings

bhk_analysis = bhk_analysis[

    bhk_analysis['listing_count'] >= 20

].sort_values('bhk_count')

print("\n===== BHK PRICING ANALYSIS =====")

print(bhk_analysis.to_string(index=False))

fig, axes = plt.subplots(1, 2, figsize=(15, 6))

sns.barplot(

    data=bhk_analysis,

    x='bhk_count',

    y='listing_count',

    color="#C49A6C",

    ax=axes[0]

)

axes[0].set_title("Apartment Listings by BHK")

axes[0].set_xlabel("BHK Configuration")

axes[0].set_ylabel("Number of Listings")

sns.barplot(

    data=bhk_analysis,

    x='bhk_count',

    y='median_price_crore',

    color="#526D82",

    ax=axes[1]

)

axes[1].set_title("Median Asking Price by BHK")

axes[1].set_xlabel("BHK Configuration")

axes[1].set_ylabel("Median Price (INR Crores)")

plt.suptitle(

    "Gurugram Apartment Market | BHK Analysis",

    fontsize=17,

    fontweight="bold"

)

plt.tight_layout(rect=(0, 0, 1, 0.94))

plt.savefig(

    BASE_DIR / "reports/figures/bhk_analysis.png",

    dpi=300,

    bbox_inches="tight"

)

plt.close()


# 12: RERA & PROPERTY STATUS ANALYSIS

# RERA approval analysis

rera_analysis = (

    apartment_df.groupby('rera_approval')

    .agg(

        listing_count=('price', 'size'),

        median_price_crore=('price_crore', 'median'),

        median_rate_sqft=('price_per_sqft_calculated', 'median')

    )

    .reset_index()

)

rera_analysis['rera_label'] = (

    rera_analysis['rera_approval']

    .map({True: 'RERA Approved', False: 'Not RERA Approved'})

)

print("\n===== RERA APPROVAL ANALYSIS =====")

print(rera_analysis.to_string(index=False))

# Property status analysis

status_analysis = (

    apartment_df.groupby('status')

    .agg(

        listing_count=('price', 'size'),

        median_price_crore=('price_crore', 'median'),

        median_rate_sqft=('price_per_sqft_calculated', 'median')

    )

    .reset_index()

)

print("\n===== PROPERTY STATUS ANALYSIS =====")

print(status_analysis.to_string(index=False))

# Create visualizations

fig, axes = plt.subplots(1, 2, figsize=(15, 6))

sns.barplot(

    data=rera_analysis,

    x='rera_label',

    y='median_rate_sqft',

    color="#526D82",

    ax=axes[0]

)

axes[0].set_title("RERA Approval vs Median Asking Rate")

axes[0].set_xlabel("")

axes[0].set_ylabel("Median Asking Price per Sqft (INR)")

sns.barplot(

    data=status_analysis,

    x='status',

    y='median_price_crore',

    color="#C49A6C",

    ax=axes[1]

)

axes[1].set_title("Median Apartment Price by Status")

axes[1].set_xlabel("")

axes[1].set_ylabel("Median Asking Price (INR Crores)")

axes[1].tick_params(axis='x', rotation=20)

plt.suptitle(

    "Gurugram Apartment Market | RERA & Status",

    fontsize=17,

    fontweight="bold"

)

plt.tight_layout(rect=(0, 0, 1, 0.94))

plt.savefig(

    BASE_DIR / "reports/figures/rera_status_analysis.png",

    dpi=300,

    bbox_inches="tight"

)

plt.close()