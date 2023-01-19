import pandas as pd
import os
import sys
import numpy as np

# "Topis-Algorithm/Arjun Pundir-102003742"


def main():
    
    if len(sys.argv) != 5:
        print("ERROR : NUMBER OF PARAMETERS ARE NOT SAME AS CSV FILE PROVIDED")
        print("USAGE : python topsis.py inputfile.csv '1,1,1,1,1' '+,+,-,+,+' result.csv ")
        exit(1)

    # File Not Found error
    elif not os.path.isfile(sys.argv[1]):
        print(f"ERROR : {sys.argv[1]} Don't exist!!")
        exit(1)

    # File extension not csv
    elif ".csv" != (os.path.splitext(sys.argv[1]))[1]:
        print(f"ERROR : {sys.argv[1]} is not a csv!!")
        exit(1)

    else:
        dataset, temp_data = pd.read_csv(
            sys.argv[1]), pd.read_csv(sys.argv[1])
        ColNum = len(temp_data.columns.values)

        
        if ColNum < 3:
            print("ERROR : Input file have less then 3 columns,keep decision matrix columns atleast 3")
            exit(1)

        for i in range(1, ColNum):
            pd.to_numeric(dataset.iloc[:, i], errors='coerce')
            dataset.iloc[:, i].fillna(
                (dataset.iloc[:, i].mean()), inplace=True)

       
        try:
            weights = [int(i) for i in sys.argv[2].split(',')]
        except:
            print("ERROR : In weights array please check again, Should contain integers only seperated by commas")
            exit(1)
        impact = sys.argv[3].split(',')
        for i in impact:
            if not (i == '+' or i == '-'):
                print("ERROR : In impact array please check again, only '+' and '-' permitted")
                exit(1)

        # Checking number of column,weights and impacts is same or not
        if ColNum != len(weights)+1 or ColNum != len(impact)+1:
            print(
                "ERROR : Number of weights, number of impacts and number of columns are not same")
            exit(1)

        if (".csv" != (os.path.splitext(sys.argv[4]))[1]):
            print("ERROR : Output file extension is wrong")
            exit(1)
        if os.path.isfile(sys.argv[4]):
            os.remove(sys.argv[4])
        topsis(temp_data, dataset, ColNum, weights, impact)


def Normalize(temp_data, ColNum, weights):
    for i in range(1, ColNum):
        temp = 0
        for j in range(len(temp_data)):
            temp = temp + temp_data.iloc[j, i]**2
        temp = temp**0.5
        for j in range(len(temp_data)):
            temp_data.iat[j, i] = (
                temp_data.iloc[j, i] / temp)*weights[i-1]
    return temp_data


def Calculate_Values(temp_data, ColNum, impact):
    positive_sol = (temp_data.max().values)[1:]
    negative_sol = (temp_data.min().values)[1:]
    for i in range(1, ColNum):
        if impact[i-1] == '-':
            positive_sol[i-1], negative_sol[i-1] = negative_sol[i-1], positive_sol[i-1]
    return positive_sol, negative_sol


def topsis(temp_data, dataset, ColNum, weights, impact):
    temp_data = Normalize(temp_data, ColNum, weights)
    positive_sol, negative_sol = Calculate_Values(temp_data, ColNum, impact)

    # calculating topsis score
    
    score = []
    for i in range(len(temp_data)):
        temp_p, temp_n = 0, 0
        for j in range(1, ColNum):
            temp_p = temp_p + (positive_sol[j-1] - temp_data.iloc[i, j])**2
            temp_n = temp_n + (negative_sol[j-1] - temp_data.iloc[i, j])**2
        temp_p, temp_n = temp_p**0.5, temp_n**0.5
        score.append(temp_n/(temp_p + temp_n))
    dataset['Topsis Score'] = score

    dataset['Ranking'] = (dataset['Topsis Score'].rank(
        method='max', ascending=False))
    dataset = dataset.astype({"Ranking": int})

    # Writing to the csv
    dataset.to_csv(sys.argv[4], index=False)


if __name__ == "__main__":
    main()