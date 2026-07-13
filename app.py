import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title and description
st.title("Interactive sales dashboard")
st.write("Upload a CSV file with sales and profit data to analyze and visualize results.")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the CSV file
    data = pd.read_csv(uploaded_file)

    # Display the data
    st.write("Data Preview:")
    st.dataframe(data.head())

    # Dropdown for metric selection

    metric=st.selectbox("Select a metric to visualize:", ["Sales", "Profit"])
    # calculate total
    total_value=data[metric].sum()
    st.write(f"Total {metric.capitalize()}: **{total_value}")

    # Aggregate by region
    agg_by_region = data.groupby('region')[metric].sum()
    st.write(f"Total {metric.capitalize()} by Region:**")
    st.dataframe(agg_by_region)

    #Dropdown for chart type
    chart_type=st.selectbox("Select a chart type:", ["Bar Chart", "Line Chart","Pie Chart"]) 
    fig,ax=plt.subplots()

    if chart_type=="Bar Chart":
        agg_by_region.plot(kind='bar', ax=ax, color='skyblue', edgecolor='black')
        ax.set_title(f"{metric} by Region")
        ax.set_xlabel("Region")
        ax.set_ylabel(metric.capitalize())
    elif chart_type=="Line Chart":
        agg_by_region.plot(kind='line', ax=ax, marker='o', color='green')
        ax.set_title(f"{metric.capitalize()} by Region(Line Chart)")
        ax.set_xlabel("Region")
        ax.set_ylabel(metric.capitalize())
    elif chart_type=="Pie Chart":
        agg_by_region.plot(kind='pie', ax=ax, autopct='%1.1f%%', startangle=90)
        ax.set_ylabel("")
        ax.set_title(f"{metric.capitalize()} Distribution by Region")

    st.pyplot(fig)

    # Prepare processed results for download
    processed_results = agg_by_region.reset_index()
    processed_results.columns = ['Region',  metric.capitalize()]

    # download button for processed results
    st.download_button(
        label="Download Processed Results as CSV",
        data=processed_results.to_csv(index=False).encode('utf-8'),
        file_name='processed_results.csv',
        mime='text/csv'
    )
    # # Check if required columns exist
    # if 'Sales' in data.columns and 'Profit' in data.columns:
    #     # Create a scatter plot of Sales vs Profit
    #     plt.figure(figsize=(10, 6))
    #     plt.scatter(data['Sales'], data['Profit'], alpha=0.5)
    #     plt.title('Sales vs Profit')
    #     plt.xlabel('Sales')
    #     plt.ylabel('Profit')
    #     plt.grid(True)
    #     st.pyplot(plt)
    # else:
    #     st.error("The uploaded CSV file must contain 'Sales' and 'Profit' columns.")