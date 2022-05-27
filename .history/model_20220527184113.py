
df=pd.read_csv(r'C:\Users\HP\Desktop\Trojan-Code\Training.csv')
df.drop(df.columns[3:127],axis=1,inplace=True)
train_df = df.drop('Unnamed: 133', axis=1)

test_df=pd.read_csv(r'C:\Users\HP\Desktop\Trojan-Code\Testing.csv')
test_df.drop(test_df.columns[3:127],axis=1,inplace=True)
x=train_df.iloc[:,:-1]
y=train_df.iloc[:,8]
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state=42)
tree = DecisionTreeClassifier()
tree.fit(x_train, y_train)
input_data = [1,1,1,1,1,1,1,1]

input_data_as_numpy_array= np.asarray(input_data)

input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)

prediction = tree.predict(input_data_reshaped)

print(prediction)
