import plotly.express as px
import pycountry
from pandas import DataFrame


def group_country_code_list(country_codes: list[str]) -> dict:
    grouping = {}
    for country in country_codes:
        _out = grouping.setdefault(country, 0)
        grouping[country] += 1
    data = {"iso_alpha": [], "value": []}
    for key, val in grouping.items():
        data["iso_alpha"].append(key)
        data["value"].append(val)
    return data


def convert_alpha2_to_alpha3(country_codes: list[str]) -> list[str]:
    out = []
    for alpha2_code in country_codes:
        try:
            country = pycountry.countries.get(alpha_2=alpha2_code)
            out.append(country.alpha_3)
        except AttributeError:
            if alpha2_code == "QM" or alpha2_code == "QZ":
                out.append('USA')
    return out


def generate_map(data: dict) -> None:
    df = DataFrame(data)

    # Plot interactive choropleth map
    fig = px.choropleth(df, locations='iso_alpha', locationmode='ISO-3', color='value',
                        hover_name='iso_alpha', color_continuous_scale='Viridis',
                        title='Highlighted Countries')

    fig.update_geos(showcoastlines=True, coastlinecolor="Black",
                    showland=True, landcolor="white")

    fig.show()
