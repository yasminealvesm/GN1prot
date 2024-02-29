import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Import the file containing log2 data
data = pd.read_excel('GOEnri_log2_0.58.xlsx')

# Filter data for specific group and p-value less than 0.05
filtered_data = data[(data['Comparison (condition 1 / condition 2)'] == 'Test 2 / Test 1') & (data['Pvalue'] < 0.05)]

# Map categories to colors
category_colors = {'Process': 'blue', 'Function': 'green', 'Component': 'red'}

# Add a new 'Category Color' column based on the category
filtered_data.loc[:, 'Category Color'] = filtered_data['Namespace'].map(category_colors).copy()

# Group by GO ID and average Log2 Fold Enrichment
grouped_data = filtered_data.groupby(['GO Id', 'Namespace']).agg({'Log2 Fold Enrichment': 'mean', 'GO Name': 'first', 'Category Color': 'first'})

# Select the top 20 terms from 'Process', top 15 terms from 'Component' and top 10 terms from 'Function'
top_terms_process = grouped_data[grouped_data.index.get_level_values('Namespace') == 'Process'].nlargest(20, 'Log2 Fold Enrichment')
top_terms_component = grouped_data[grouped_data.index.get_level_values('Namespace') == 'Component'].nlargest(14, 'Log2 Fold Enrichment')
top_terms_function = grouped_data[grouped_data.index.get_level_values('Namespace') == 'Function'].nlargest(10, 'Log2 Fold Enrichment')

# Concatenate the results
top_terms_per_category = pd.concat([top_terms_process, top_terms_component, top_terms_function])

# Create a horizontal bar chart with adjusted size
fig, ax = plt.subplots(figsize=(12, 8))  # Ajuste o tamanho conforme necessário

# Initialize a dictionary for unique labels
legend_labels = {}

# Modify the line below to include the "GO ID"
for namespace, color in category_colors.items():
    subset = top_terms_per_category[top_terms_per_category['Category Color'] == color]
    bars = ax.barh(subset['GO Name'] + ' (' + subset.index.get_level_values('GO Id').astype(str) + ')',
                   subset['Log2 Fold Enrichment'],
                   color=color,
                   label=namespace)  # Adicionar rótulos aos objetos de barras
    
    # Add unique labels to dictionary
    legend_labels[namespace] = bars[0]

# Add labels and title
ax.set_xlabel('Log2 Fold Enrichment')
ax.set_ylabel('GO Name (GO ID)')
ax.set_title('Top Termos de GO Enriquecidos para GN em LCH/YPD')

# Adjust the initial position of the bars
ax.set_xlim(min(top_terms_per_category['Log2 Fold Enrichment']) - 0.25, max(top_terms_per_category['Log2 Fold Enrichment']) + 0.25)

# Add the caption with unique labels
ax.legend(legend_labels.values(), legend_labels.keys(), loc='upper left', bbox_to_anchor=(1, 1))

# Adjust font size value as needed
ax.yaxis.set_tick_params(labelsize=10)

# Adjust the position of the chart to accommodate the legend
fig.subplots_adjust(right=0.90, left=0.65)

plt.show()
