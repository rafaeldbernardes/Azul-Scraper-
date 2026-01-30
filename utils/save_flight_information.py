import os
import pandas as pd

def save_flight_information(flight_data, aggregated_df) -> None:
    # Convert flight data to a DataFrame
    df = pd.DataFrame(flight_data)

    # Append the current flight data to the aggregated DataFrame
    aggregated_df = pd.concat([aggregated_df, df], ignore_index=True)

    return aggregated_df

def save_aggregated_csv(aggregated_df, aggregated_file_name):
    # Save the aggregated flight information to a single CSV file
    os.makedirs('./Flights', exist_ok=True)
    aggregated_file_path = f'./Flights/{aggregated_file_name}.csv'
    aggregated_df.to_csv(aggregated_file_path, index=False)

    print(f"{aggregated_file_path} saved.")