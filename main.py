import pandas as pd
import seaborn as sns 
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler

# 1. Load data
df = pd.read_csv("data/dummy_house_prices.csv")
print(df.describe())

# 2. Pilih kolom numerik & buang NaN
df = df.select_dtypes(include=[int, float]).dropna()

# 3. Korelasi dan visualisasi (optional)
# plt.figure(figsize=(10, 8))
# sns.heatmap(df.corr(), annot=True, fmt=".2f", cmap="coolwarm")
# plt.show()

# 4. Pisahkan fitur & target
X = df.drop("SalePrice", axis=1)
y = df["SalePrice"]

# 5. Scaling (optional tapi membantu model yang sensitif)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 6. Split data
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

# 7. Model lebih kuat → Gradient Boosting
model = GradientBoostingRegressor(n_estimators=150, learning_rate=0.1, max_depth=4, random_state=42)
model.fit(X_train, y_train)

# 8. Evaluasi
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
rmse = mse**0.5
print("MSE:", mse)
print("RMSE:", rmse)

# 9. Prediksi contoh
sample = X_test[0:1]
prediction = model.predict(sample)
print("Prediksi harga:", prediction)
