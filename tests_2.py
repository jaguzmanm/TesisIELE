import pandas as pd

n = 10
df = pd.DataFrame(columns=("reward", "final_state"))

i = 0
while i < n:
    
    new_row = [i*10, i]
    df.loc[len(df)] = new_row   
    i += 1

print(df) 