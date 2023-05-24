# СТОРІНКА "КАРТА ТА ГРАФІК"
if select_page == 'Візуалізація':
    st.sidebar.info(
        """
        На цій сторінці можна на власні очі можете побачити та проаналізувати одну з глобальних проблем людства 
        """
    )
    st.sidebar.title('Фільтри')

    with st.container():
        st.header("Назви забруднювачів")

    col1, col2 = st.columns(2)

    with col1:
        st.text("1.  NO2 - діоксид азоту \n2.  NO - оксид азоту \n3.  CO - вуглекислий газ \n4.  BC - чорний вуглець \n5.  O3 - озон \n6.  PM2.5 - частки розміром менше 2.5 мікрометрів (забруднювачі повітря)")

    with col2:
        st.text("7.  SO2 - діоксид сірки \n8.  NOX - суміш оксидів азоту \n9.  PM1 - частки розміром менше 1 мікрометра (забруднювачі повітря) \n10.  PM10 - частки розміром менше 10 мікрометрів (забруднювачі повітря)")


    # загрузка даних
    @st.cache_data
    def load_data():
        df_air = pd.read_excel("C:/Users/kalok/PycharmProjects/mkalokhina/openaq.xlsx")
        df_geo = pd.read_excel("C:/Users/kalok/PycharmProjects/mkalokhina/worldcities1.xlsx")
        df = pd.merge(df_air, df_geo, left_on=['Country Code', 'City'], right_on=[
            'iso2', 'City'], how='left')
        df = df.dropna(subset=['Coordinates'])
        df[['Lat', 'Lon']] = df['Coordinates'].str.split(
            ',', expand=True).astype(float)
        df['Last Updated'] = pd.to_datetime(df['Last Updated'], utc=True)
        return df


    df = load_data()

    country = st.sidebar.multiselect("Оберіть країну", df["Country Label"].unique())
    year_options = df[df["Country Label"].isin(country)]["Last Updated"].dt.year.unique()
    year = st.sidebar.selectbox("Оберіть рік", year_options)
    pollutant_options = df['Pollutant'].unique()
    pollutant = st.sidebar.multiselect("Оберіть забруднювач", pollutant_options)
    save_data_button = st.sidebar.button('Зберегти дані')
    show_data = st.sidebar.checkbox('Показати дані')
    button1 = st.sidebar.checkbox("Показати карту")
    button2 = st.sidebar.checkbox("Показати графіки")

    if save_data_button:
        st.subheader("Збережено дані")

    # відображення ексель данних + скачування
    filtered_df = df[df['Country Label'] == country[0]]
    columns_to_display = ['Country Label', 'Last Updated', 'City', 'Pollutant', 'Value']

    if show_data:
        st.subheader('Дані ро забруднення повітря у вибраній країні')
        st.table(filtered_df[columns_to_display])
        csv = filtered_df[columns_to_display].to_csv(index=False)
        st.download_button("Download CSV", data=csv, file_name='data.csv', mime='text/csv')


    # фільтруємо обрані дані

    inCountry = df["Country Label"].isin(country)
    withCords = df['Lon'].notna() & df['Lat'].notna()
    selectedPollutants = df['Pollutant'].isin(pollutant)
    selectedYear = df['Last Updated'].dt.year == year
    filtered_df = df[inCountry & withCords & selectedPollutants & selectedYear]



    if button1:
        st.subheader("{} в {}".format(", ".join(pollutant), ", ".join(country)))

        high_threshold = 5.0
        medium_threshold = 3.0
        map_air = folium.Map()
        heat_data = []

        # позначки на карті
        for index, row in filtered_df.iterrows():
            if row['Pollutant'] in pollutant:
                heat_data.append([row['Lat'], row['Lon'], row['Value']])
        plugins.HeatMap(heat_data).add_to(map_air)

        # додаємо позначки на місца
        cities_data = filtered_df[['Lat', 'Lon', 'City']].drop_duplicates()
        for _, city_row in cities_data.iterrows():
            city_location = [city_row['Lat'], city_row['Lon']]
            city_name = city_row['City']
            folium.Marker(city_location, popup=city_name).add_to(map_air)

        marker_cluster = plugins.MarkerCluster().add_to(map_air)

        for _, heat_row in filtered_df.iterrows():
            heat_location = [heat_row['Lat'], heat_row['Lon']]
            heat_value = heat_row['Value']
            radius = 5

            # колір позначок
            if heat_value >= high_threshold:
                color = 'red'
            elif heat_value >= medium_threshold:
                color = 'yellow'
            else:
                color = 'blue'

        st_data = st_folium(map_air, width=700)

    if button2:

        # графік для відображення забруднення повітря в містах обраних країн
        st.subheader("Відображення забруднювачів {} в містах {}".format(", ".join(pollutant), ", ".join(country)))

        if len(filtered_df) > 0:
            filtered_df[['Country Label', 'City', 'Pollutant', 'Value']].groupby(
                ['Country Label', 'City', 'Pollutant']).max().unstack('Pollutant').plot.bar()
            plt.xlabel('Місто')
            plt.ylabel('Рівень забруднення')
            plt.xticks(rotation=90)
            st.pyplot(plt)

        # 2 графік для порівнянь обраних країн по рівню забруднення повітря
        st.subheader("Порівння забруднення повітря в {} ".format(", ".join(country)))
        if len(filtered_df) > 0:
            df_selected = filtered_df[filtered_df['Country Label'].isin(country)][
                ['Country Label', 'Pollutant', 'Value']]
            df_agg = df_selected.groupby(['Country Label', 'Pollutant']).max().reset_index()
            sns.set(style="whitegrid")
            plt.figure(figsize=(12, 6))
            ax = sns.barplot(x='Country Label', y='Value', hue='Pollutant', data=df_agg)
            ax.set_xlabel('Країни')
            ax.set_ylabel('Рівень забруднення повітря')
            plt.xticks(rotation=45)
            st.pyplot(plt)

        # кругова діаграма
        st.subheader("Діграма з порівнянням обраних забруднювачів")

        if len(filtered_df) > 0:
            pollutant_counts = filtered_df['Pollutant'].value_counts()
            plt.figure(figsize=(8, 8))
            plt.pie(pollutant_counts, labels=pollutant_counts.index, autopct='%1.1f%%')
            plt.axis('equal')
            st.pyplot(plt)