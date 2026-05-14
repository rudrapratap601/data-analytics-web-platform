def generate_quality_report(df):

    report = {}

    report["Rows"] = df.shape[0]
    report["Columns"] = df.shape[1]

    report["Missing Values"] = (
        df.isnull().sum().sum()
    )

    report["Duplicate Rows"] = (
        df.duplicated().sum()
    )

    return report