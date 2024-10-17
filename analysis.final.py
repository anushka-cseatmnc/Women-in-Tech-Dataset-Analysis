import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go  # Importing plotly for interactive plots



# File paths
country_mapping_path = r"C:/Users/anush/Downloads/dataset/Country-Code-Mapping.csv"
codebook_path = r"C:/Users/anush/Downloads/dataset/HackerRank-Developer-Survey-2018-Codebook.csv"
numeric_mapping_path = r"C:/Users/anush/Downloads/dataset/HackerRank-Developer-Survey-2018-Numeric-Mapping.csv"
numeric_data_path = r"C:\Users\anush\Downloads\dataset\HackerRank-Developer-Survey-2018-Numeric.csv\HackerRank-Developer-Survey-2018-Numeric.csv"
values_data_path = r"C:/Users/anush/Downloads/dataset/HackerRank-Developer-Survey-2018-Values.csv"


# Load datasets
def load_data(path):
    try:
        data = pd.read_csv(path, dtype=str)
        print(f"{path} loaded successfully.")
        return data
    except Exception as e:
        print(f"Error loading {path}: {e}")
        return None

country_mapping = load_data(country_mapping_path)
codebook = load_data(codebook_path)
numeric_mapping = load_data(numeric_mapping_path)
numeric_data = load_data(numeric_data_path)
values = load_data(values_data_path)  # Assign values_data to the variable 'values'

# Verify the gender ratio
if values is not None:
    gender_count = values['q3Gender'].value_counts(normalize=True).mul(100).round(1)
    print("Gender Ratio:\n", gender_count)

    # Analyze the age when people started coding
    age_begin_coding = values.groupby(['q3Gender', 'q1AgeBeginCoding'])['q1AgeBeginCoding'].count().unstack(fill_value=0)
    age_begin_coding_percent = age_begin_coding.div(age_begin_coding.sum(axis=1), axis=0).mul(100).round(1)

    fig = go.Figure(data=[
        go.Bar(name='Male', x=age_begin_coding_percent.index, y=age_begin_coding_percent.loc['Male'], marker=dict(color='lightgoldenrodyellow')),
        go.Bar(name='Female', x=age_begin_coding_percent.index, y=age_begin_coding_percent.loc['Female'], marker=dict(color='forestgreen'))
    ])
    fig.update_layout(
        title='Age when they started coding - Male vs Female',
        xaxis_title='Age when coding is begun',
        yaxis_title='Percentage of Respondents',
    )
    fig.show()

    # Analyze the degree focus
    degree_focus = values.groupby(['q3Gender', 'q5DegreeFocus'])['q5DegreeFocus'].count().unstack(fill_value=0)
    degree_focus_percent = degree_focus.div(degree_focus.sum(axis=1), axis=0).mul(100).round(1)

    fig = go.Figure(data=[
        go.Bar(name='Male', x=degree_focus_percent.index, y=degree_focus_percent.loc['Male'], marker=dict(color='lightgoldenrodyellow')),
        go.Bar(name='Female', x=degree_focus_percent.index, y=degree_focus_percent.loc['Female'], marker=dict(color='forestgreen'))
    ])
    fig.update_layout(
        title='Degree Focus - Male vs Female',
        xaxis_title='Degree Focus',
        yaxis_title='Percentage of Respondents',
    )
    fig.show()

    # Analyze the gender ratio by country
    values['is_student'] = values['q8Student'].apply(lambda x: 'Students' if x == '' else 'Developers')
    f2m_ratio = values.groupby('CountryNumeric')['q3Gender'].value_counts(normalize=True).unstack(fill_value=0)
    f2m_ratio = f2m_ratio.div(f2m_ratio.sum(axis=1), axis=0).mul(100).round(1)  # Normalize

    fig = go.Figure(data=[
        go.Bar(name='Female-to-Male Ratio', x=f2m_ratio.index, y=f2m_ratio['Female'], marker=dict(color='lightblue'))
    ])
    fig.update_layout(
        title='Female-to-Male Ratio by Country',
        xaxis_title='Country',
        yaxis_title='Female-to-Male Ratio (%)',
    )
    fig.show()
else:
    print("The values dataset failed to load. Please check the file path.")

print("Data processing and visualization complete!")
