import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read the CSV file directly (replace with your CSV file path)
def create_visualizations():
    try:
        # Replace this path with your actual CSV file path
        df = pd.read_csv('sample_demo.csv')
        
        # Create a simple line plot
        plt.figure(figsize=(10, 6))
        for column in df.select_dtypes(include=['int64', 'float64']).columns:
            plt.plot(df[column], label=column)
        
        plt.title('Data Visualization')
        plt.legend()
        plt.savefig('plot.png')
        plt.close()
        
        print("Visualization created successfully!")
        print("\nDataset Info:")
        print(df.head())
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    print("Starting program...")
    create_visualizations()
    print("Program finished!")