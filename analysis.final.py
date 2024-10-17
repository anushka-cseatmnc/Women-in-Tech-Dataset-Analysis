from pyspark.sql import SparkSession

# Initialize Spark session in local mode
spark = SparkSession.builder \
    .appName("Merge Example") \
    .master("local[*]") \
    .getOrCreate()

# Define file paths
country_mapping_path = r"C:\Users\anush\Downloads\dataset\Country-Code-Mapping.csv"
codebook_path = r"C:\Users\anush\Downloads\dataset\HackerRank-Developer-Survey-2018-Codebook.csv"
numeric_mapping_path = r"C:\Users\anush\Downloads\dataset\HackerRank-Developer-Survey-2018-Numeric-Mapping.csv"
numeric_data_path = r"C:\Users\anush\Downloads\dataset\HackerRank-Developer-Survey-2018-Numeric.csv"
values_data_path = r"C:\Users\anush\Downloads\dataset\HackerRank-Developer-Survey-2018-Values.csv"

# Load data
country_mapping = spark.read.csv(country_mapping_path, header=True)
codebook = spark.read.csv(codebook_path, header=True)
numeric_mapping = spark.read.csv(numeric_mapping_path, header=True)
numeric_data = spark.read.csv(numeric_data_path, header=True)
values_data = spark.read.csv(values_data_path, header=True)

# Merge data based on relevant keys
merged_data = numeric_data.join(country_mapping, numeric_data['CountryNumeric2'] == country_mapping['Value'], 'inner')

# Optionally, merge other dataframes similarly
merged_data = merged_data.join(numeric_mapping, 'RespondentID', 'inner')
merged_data = merged_data.join(values_data, 'RespondentID', 'inner')
merged_data = merged_data.join(codebook, 'RespondentID', 'inner')

# Show the merged data sample
merged_data.show()

# Stop Spark session
spark.stop()
