import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix


pd.set_option("display.max_rows", 120)
pd.set_option("display.width", 1000)
pd.set_option("display.expand_frame_repr", False)

data = pd.read_csv("../listing+post+pre_data.csv")
data = data.dropna()

conditions = [
    data['one_month_post_listing_performance'] > 0,
    data['one_month_post_listing_performance'] <= 0
]
choices = [1, -1]
data['signal'] = np.select(conditions, choices, default=0)

signal_counts = data['signal'].value_counts()
features = [
    'asset_type',
    'listing_order',
    'one_hour_post_listing_performance',
    'one_day_post_listing_performance',
    'marketcap_minus1d',
    'price_change_minus1d',
    'price_change_minus7d',
    'volume_change_minus1d',
    'volume_change_minus7d'
]


X = data[features]
y = data.signal

train_X, val_X, train_y, val_y = train_test_split(X, y, random_state=1)

clf = RandomForestClassifier(random_state=1, class_weight="balanced")
clf.fit(train_X, train_y)


rf_val_predictions = clf.predict(val_X)
rf_val_mae = mean_absolute_error(rf_val_predictions, val_y)

val_results = pd.DataFrame({
    "Actual": val_y,
    "Predicted": rf_val_predictions
})

print(val_results)

accuracy = accuracy_score(val_y, rf_val_predictions)
print(f"Accuracy: {accuracy}\n")

print(classification_report(val_y, rf_val_predictions))

print("Confusion Matrix:")
print(confusion_matrix(val_y, rf_val_predictions))
