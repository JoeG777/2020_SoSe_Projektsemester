import pandas as pd
import model_persistor


d = {'col1': [1, 2], 'col2': [3, 4]}
df = pd.DataFrame(data=d)

dict = {
    "a": "1",
    "b": df
}
print(model_persistor.load())

