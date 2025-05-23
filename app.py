from flask import Flask, render_template, request
import pandas as pd
import folium

app = Flask(__name__)

# Load the events data
events_data = pd.read_csv('data/events_data.csv')

@app.route('/', methods=['GET', 'POST'])
def index():
    # Get unique categories from the 'Kategorie' column
    unique_categories = events_data['Kategorie'].dropna().unique().tolist()

    # Get selected category from the form
    selected_category = request.form.get('category')

    # Filter events based on selected category
    if selected_category:
        filtered_events = events_data[events_data['Kategorie'] == selected_category]
    else:
        filtered_events = events_data

    # Create a Folium map centered on Warsaw
    map_warsaw = folium.Map(location=[52.2297, 21.0122], zoom_start=12)

    # Add events to the map, checking for NaN values in Latitude and Longitude
    for _, event in filtered_events.iterrows():
        if pd.notna(event['Latitude']) and pd.notna(event['Longitude']):
            folium.Marker(
                location=[event['Latitude'], event['Longitude']],
                popup=f"<strong>{event['Wydarzenie']}</strong><br>{event['Data']} {event['Godzina']}<br>{event['Miejsce']}",
                icon=folium.Icon(color='blue')
            ).add_to(map_warsaw)

    # Save the map to an HTML file
    map_warsaw.save('templates/map.html')

    # Pass unique categories and filtered events to the template
    return render_template('index.html', categories=unique_categories, filtered_events=filtered_events.to_json(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
