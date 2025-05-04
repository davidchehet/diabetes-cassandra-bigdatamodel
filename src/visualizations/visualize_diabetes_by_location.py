from ..config import get_session
from ..utils import get_query_by_tag
import pandas as pd
import geopandas
import matplotlib.pyplot as plt
import os

session = get_session()
if session:
    print('Connected!')
else:
    print('Error occurrred')

# Query the gold table by location
rows = session.execute(get_query_by_tag('src/cql_scripts/gold_scripts.cql', 'SELECT_FROM_NEW_GOLD_BY_LOC'))

# Make DF for visualization tools
diabetes_by_state = pd.DataFrame(list(rows))
diabetes_by_state.rename(columns={'location': 'name'}, inplace=True)

# Begin plotting the data
world = geopandas.read_file('src/ne_110m_admin_1_states_provinces/ne_110m_admin_1_states_provinces.shp')
us_states = world[world['admin'] == 'United States of America']
us_states = us_states[['name', 'geometry']]

merged_data = us_states.merge(diabetes_by_state, on='name', how='left')

fig, ax = plt.subplots(1, 1, figsize=(15, 10))
merged_data.plot(column='diabetes_prevalence', cmap='viridis', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)

# Plot the state boundaries
us_states.plot(ax=ax, linewidth=0.5, edgecolor='black', facecolor='none')

ax.set_title('Prevalence of Diabetes by US State')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')

ax.set_xticks([])
ax.set_yticks([])

plt.tight_layout()
plt.show()

session.shutdown()

