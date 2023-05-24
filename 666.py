plt.style.use('ggplot')

            # Создание базовой карты
            m1 = folium.Map(location=[0, 0], zoom_start=2)

            # Настройка стиля и отображение границ карты
            m1.choropleth(geo_data=None, fill_color='#A6CAE0', fill_opacity=0.3, line_opacity=0.1)

            # Добавление теней рельефа
            folium.raster_layers.WmsTileLayer(
                url='http://ows.mundialis.de/services/service',
                layers='TOPO-OSM-WMS',
                name='shadedrelief'
            ).add_to(m1)

            # Создание кластера маркеров
            marker_cluster = MarkerCluster().add_to(m1)

            # Добавление маркеров на карту
            for index, row in location.iterrows():
                lat, lon = row['lat'], row['Lon']
                avg = np.log(row['Average'])
                hour = row['averaged_over_in_hours']
                folium.Marker(
                    location=[lat, lon],
                    popup=f"Average AQI: {avg}, Hours: {hour}",
                    icon=folium.Icon(icon='cloud', color='red')
                ).add_to(marker_cluster)

            # Отображение цветовой шкалы
            folium.plugins.FloatImage(
                plt.colorbar().get_children()[1].get_array().reshape(-1, 1),
                colormap='hot_r',
                height=500,
                position='bottomright'
            ).add_to(m1)

            # Отображение заголовка и сохранение карты
            plt.title('Average Air Quality Index in unit $ug/m^3$ value')
            m1.save('map.html')