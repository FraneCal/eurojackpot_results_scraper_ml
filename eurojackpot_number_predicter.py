import pandas as pd
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np

# Load the CSV file
df = pd.read_csv('results_2012_to_2024.csv')

# Exclude the last 5 rows for testing
train_df = df.iloc[6:]
test_df = df.iloc[0:5]

# Split features and target
X_train = train_df.drop(columns=['Date'])
y_train = train_df[['Main1', 'Main2', 'Main3', 'Main4', 'Main5', 'Add1', 'Add2']]

# Train the model
model = RandomForestRegressor()
model.fit(X_train, y_train)

# Predict on the test data
X_test = test_df.drop(columns=['Date'])
y_pred = model.predict(X_test)

# Round up the predictions to the next whole number
y_pred_rounded = np.ceil(y_pred)

# Convert the rounded predictions into a DataFrame
pred_df_rounded = pd.DataFrame(y_pred_rounded, columns=['Main1', 'Main2', 'Main3', 'Main4', 'Main5', 'Add1', 'Add2'])
pred_df_rounded['Date'] = test_df['Date'].values

# Calculate mean squared error
mse = mean_squared_error(test_df[['Main1', 'Main2', 'Main3', 'Main4', 'Main5', 'Add1', 'Add2']], y_pred_rounded)
print("Mean Squared Error:", mse)

# Display the rounded predictions
print("Predicted Results (Rounded Up) for the Last 5 Dates:")
print(pred_df_rounded)

# Predict the next numbers for today
last_date = datetime.strptime(df['Date'].iloc[-1], '%Y-%m-%d')
next_date = last_date + timedelta(days=7)  # Assuming the lottery is drawn every week
last_row = df.iloc[-1].drop('Date')  # Exclude the date column
next_numbers = model.predict([last_row.values])[0]
next_numbers_rounded = np.ceil(next_numbers)
today_date = datetime.today()
formatted_date = today_date.strftime('%Y-%m-%d')
print(f"\nPredicted Next Numbers for {formatted_date}:", next_numbers_rounded)
