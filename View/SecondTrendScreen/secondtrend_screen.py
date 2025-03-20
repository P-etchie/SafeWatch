import json, kivy.logger, matplotlib.figure
from View import screens
from View.base_screen import BaseScreenView
import matplotlib.pyplot as plt
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.list import OneLineListItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import ObjectProperty
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg


class SecondTrendScreenView(BaseScreenView):
    county_list = ObjectProperty(None)
    _observers = []
    _county = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = None
        self.data = None

    @property
    def county(self):
        return self._county

    @county.setter
    def county(self, countyVal):
        self._county = countyVal

    def on_enter(self):
        if self.app is None:
            self.app = MDApp.get_running_app()

        if self.data is None:
            self.data = self.app.app_data

        if self._county is not None:
            self.load_county_info(self._county)
            self.update_chart(self._county)
            self.update_stats_container(self._county)

    def model_is_changed(self):
        self.model.notify_observers("secondtrend screen")

    def switch_screen(self, scr, *args):
        screen_ = screens.screens.get(scr)
        if screen_:
            self.model = screen_['model']
            self.controller =  screen_['controller'](self.model)
            self.view = self.controller.get_view()
            self.app.prev = self.app.manager_screens.current_screen.name
            self.app.manager_screens.current = self.view.name
        else:
            kivy.logger.Logger.info(f"Got None As Screen")

    def load_county_info(self, countyVal):
        county_data = self.data.get("ReportedCrimes2023", {})
        population_data = self.data.get("Population2023", {})
        county_details = self.data.get("CountiesData", {})

        for county, crime_count in sorted(county_data.items(), key=lambda x: x[1], reverse=True):
            population = population_data[countyVal]
            crimes = county_details.get(countyVal, {}).get("crimes", [])
            percentages = county_details.get(county, {}).get("county_percent", [])

            if len(crimes) != len(percentages):
                percentages = [0] * len(crimes)

            crime_counts = [(crime, int((percent / 100) * crime_count)) for crime, percent in zip(crimes, percentages)]
            crime_counts.sort(key=lambda x: x[1], reverse=True)
            most_reported_crime = crime_counts[0] if crime_counts else ("N/A", 0)
            least_reported_crime = crime_counts[-1] if crime_counts else ("N/A", 0)

            self.ids.county_population.text = f"[b][size=16sp][color=#FF5722]Population:[/size][/color]  {population:,}[/b]"
            self.ids.crime_rate.text = f"[size=16sp][color=#FF5722][b]Total Crimes (2018-2023):[/color][/size]  {crime_count:,}[/b]"
            self.ids.most_reported_crime.text = f"[color=#FF5722][b][size=16sp]Most Reported:[/size][/color]  {most_reported_crime[0]}[/b]"
            self.ids.least_reported_crime.text = f"[color=#FF5722][b][size=16sp]Least Reported:[/size][/color]  {least_reported_crime[0]}[/b]"

    def update_chart(self, county):
        years = [2018, 2019, 2020, 2021, 2022, 2023]
        crime_counts = []
        for year in years:
            crime_counts.append(self.data.get(f"ReportedCrimes{year}", {}).get(county, 0))
        fig = matplotlib.figure.Figure(figsize=(10, 6))
        ax = fig.add_subplot(111)

        ax.barh(years, crime_counts, color="teal")
        ax.set_title(f"Crime Trends in {county}", fontsize=14, color="teal", fontweight="bold")
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.spines['left'].set_visible(False)
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        fig.patch.set_facecolor(self.app.md_bg_color)
        ax.set_facecolor(self.app.md_bg_color)
        self.ids.crime_chart.clear_widgets()
        self.ids.crime_chart.add_widget(FigureCanvasKivyAgg(fig, size_hint=(1, 1)))

        total_crimes = sum(crime_counts)
        self.ids.county_name.text = f"[color=#FF5722][b]{self.county}[/color][/b]"
        self.ids.crime_rate.text = f"[color=#FF5722][b][size=16sp]Total Crimes (2018-2023):[/color][/size] {total_crimes}[/b]"
        self.ids.peak_crime_yr.text = f"[color=#FF5722][b][size=16sp]Peak Year:[/color][/size] {years[crime_counts.index(max(crime_counts))]}[/b]" if max(
            crime_counts) > 0 else ""
        self.update_chart2(county)

    def update_chart2(self, county):
        years = [2018, 2019, 2020, 2021, 2022, 2023]
        yearstr = ["2018", "2019", "2020", "2021", "2022", "2023"]
        crime_counts = [self.data.get(f"ReportedCrimes{year}", {}).get(county, 0) for year in years]

        fig = matplotlib.figure.Figure(figsize=(10, 6))
        ax = fig.add_subplot(111)
        max_index = crime_counts.index(max(crime_counts)) if max(crime_counts) > 0 else -1
        explode = [0.1 if i == max_index else 0 for i in range(len(crime_counts))]

        ax.pie(
            x=crime_counts,
            labels=yearstr,
            autopct=lambda p: f'{p:.1f}%' if p > 0 else '',
            textprops={'color': "white", 'fontweight': 'bold'},
            explode=explode,
            shadow=True,
            startangle=90
        )
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_visible(False)
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')

        fig.patch.set_facecolor(self.app.md_bg_color)
        ax.set_facecolor(self.app.md_bg_color)

        self.ids.crime_chart_field2.clear_widgets()
        self.ids.crime_chart_field2.add_widget(FigureCanvasKivyAgg(fig, size_hint=(1, 1)))

    def update_stats_container(self, countyVal):
        years = [2018, 2019, 2020, 2021, 2022, 2023]
        crime_counts = [self.data.get(f"ReportedCrimes{year}", {}).get(countyVal, 0) for year in years]
        total_crimes = sum(crime_counts)
        population = self.data.get("Population2023", {}).get(countyVal, 1)
        crime_density = round((total_crimes / population) * 1000, 2)
        crime_growth_rate = 0
        if crime_counts[0] > 0:
            crime_growth_rate = ((crime_counts[-1] - crime_counts[0]) / crime_counts[0]) * 100
        peak_year = years[crime_counts.index(max(crime_counts))] if max(crime_counts) > 0 else "N/A"
        lowest_year = years[crime_counts.index(min(crime_counts))] if crime_counts[0] > 0 else "N/A"
        county_data = self.data.get("ReportedCrimes2023", {})
        all_county_totals = {
            county: sum([self.data.get(f"ReportedCrimes{year}", {}).get(county, 0) for year in years])
            for county in county_data.keys()
        }
        sorted_counties = sorted(all_county_totals.items(), key=lambda x: x[1], reverse=True)
        county_rank = next((i + 1 for i, (c, _) in enumerate(sorted_counties) if c == countyVal), "N/A")
        county_details = self.data.get("CountiesData", {}).get(countyVal, {})
        crimes = county_details.get("crimes", [])
        percentages = county_details.get("county_percent", [])
        most_common_crime = "N/A"
        if percentages and crimes and len(percentages) == len(crimes):
            most_common_crime = crimes[percentages.index(max(percentages))]

        self.ids.crime_density.text = f"[b][color=#FF5722]Crime Density (per 1,000 people):[/color][/b] {crime_density}"
        self.ids.crime_growth_rate.text = f"[b][color=#FF5722]Crime Growth Rate:[/color][/b] {crime_growth_rate:.2f}%"
        self.ids.crime_rank.text = f"[b][color=#FF5722]Crime Rank:[/color][/b] #{county_rank}"
        self.ids.peak_crime_year.text = f"[b][color=#FF5722]Peak Crime Year:[/color][/b] {peak_year}"
        self.ids.lowest_crime_year.text = f"[b][color=#FF5722]Lowest Crime Year:[/color][/b] {lowest_year}"
        self.ids.most_common_crime.text = f"[b][color=#FF5722]Most Common Crime:[/color][/b] {most_common_crime}"

    def process_search_activity(self, instance_text):
        counties = self.data.get("Counties")
        for county in counties:
            if str(instance_text).lower() in str(county).lower() or instance_text.lower() == str(county).lower():
                self.county = county
                self.update_chart(self.county)
                self.load_county_info(self.county)
                self.update_stats_container(self.county)