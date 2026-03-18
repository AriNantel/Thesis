import pandas as pd
#from sklearn.linear_model import LinearRegression
#import statsmodels.api as sm


def corrolation_analysis ():
    df = pd.read_excel("Wildfire_Burning_Alg_WS.xlsx", sheet_name="WS")
    corr = df[["nx.density(G)", "nx,average_clustering(G)","nx.eccentricity(G,starting_node)","steps"]].corr()
    print (corr)

def r_squared_regression ():
    # Load your Excel file
    df = pd.read_excel("Wildfire_Burning_Alg DD.xlsx", sheet_name="DD")   # replace with your file name

    # Compute correlations
    corr_density = df["nx.density(G)"].corr(df["steps"])
    corr_clustering = df["nx,average_clustering(G)"].corr(df["steps"])
    corr_eccentricity = df["nx.eccentricity(G,starting_node)"].corr(df["steps"])

    # Compute R^2 values
    r2_density = corr_density ** 2
    r2_clustering = corr_clustering ** 2
    r2_eccentricity = corr_eccentricity ** 2

    # Print results
    print("\nCorrelation with burning steps:")
    print("--------------------------------")
    print(f"Density:       r = {corr_density:.3f},  R² = {r2_density:.3f}")
    print(f"Clustering:    r = {corr_clustering:.3f},  R² = {r2_clustering:.3f}")
    print(f"Eccentricity:  r = {corr_eccentricity:.3f},  R² = {r2_eccentricity:.3f}")

#corrolation_analysis()
r_squared_regression ()