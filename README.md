# CS5260 Final Project

## Group members

Yizhou Guo & Zhenyu Liu

## New features

> Split road trip into separate days, with user specify number of days and hours of trip per day

> Use of dynamic preference adjustment based on visit history to ensure a more engaging journey

> Integrated neural network trained from project 3 for predicting user preference

## Package Requirements

numpy, pandas, joblib, scikit-learn

## Usage

To train the neural network with a new model (it is recommended to backup the old model), use

```
python3 train_model.py DataFile
```

To use the search algorithm, use

```
python3 main.py LocationFile EdgeFile OutputFile StartLocation 
```

## Additional input

```
Please enter days of road trip:
Please enter maximum hours per day:
Please enter your expected driving speed:
Please enter your theme preference from most preferred first, enter stop to auto-fill the rest:
```

## Sample Output

Input: From ChicagoIL/ 5 days/ 10 hours per day/ 65 miles per hour

Food Art History MusicHistory Garden Landmark Nature Building Animals Kids

Output:

```
Solution label: 1  ChicagoIL  max_days:5  max_hours_per_day:10  mph:65
  Day 1:
    1  ChicagoIL          IndianapolisIN     Chicago_tofrom_Indianapolis                                     2.82hours   0.32hours
    2  IndianapolisIN     FortWayneIN        IndianapolisIN_tofrom_FortWayneIN                               1.92hours   0.70hours
    3  FortWayneIN        DetroitMI          FortWayneIN_tofrom_DetroitMI                                    2.49hours   0.35hours
  Day 2:
    1  DetroitMI          ClevelandOH        DetroitMI_tofrom_ClevelandOH                                    2.62hours   0.87hours
    2  ClevelandOH        ToledoOH           ToledoOH_tofrom_ClevelandOH                                     1.75hours   0.57hours
    3  ToledoOH           CincinnatiOH       CincinnatiOH_tofrom_ToledoOH                                    2.75hours   0.82hours
  Day 3:
    1  CincinnatiOH       LexingtonKY        Cincinnati_tofrom_Lexington                                     1.28hours   0.47hours
    2  LexingtonKY        LouisvilleKY       Louisville_tofrom_Lexington                                     1.22hours   0.42hours
    3  LouisvilleKY       BowlingGreenKY     Louisville_tofrom_BowlingGreen_on_I65                           1.80hours   0.60hours
    4  BowlingGreenKY     NashvilleTN        Nashville_tofrom_BowlingGreen_on_I65                            1.02hours   1.16hours
  Day 4:
    1  NashvilleTN        MetropolisIL       Metropolis_tofrom_Nashville_on_I24E                             2.28hours   0.64hours
    2  MetropolisIL       StLouisMO          StLouis_tofrom_Metropolis_on_I57_and_I64                        2.57hours   0.49hours
    3  StLouisMO          SpringfieldIL      StLouis_tofrom_Springfield                                      1.51hours   0.37hours
  Day 5:
    1  SpringfieldIL      ChicagoIL          Chicago_tofrom_Springfield                                      3.08hours   1.03hours
1891.0 total miles  5 days  37.90 total hours  Total Themes satisfied: 25

Solution label: 10  ChicagoIL  max_days:5  max_hours_per_day:10  mph:65
  Day 1:
    1  ChicagoIL          ToledoOH           ChicagoIL_tofrom_ToledoOH                                       2.48hours   0.63hours
    2  ToledoOH           DetroitMI          DetroitMI_tofrom_ToledoOH                                       0.91hours   0.33hours
    3  DetroitMI          ClevelandOH        DetroitMI_tofrom_ClevelandOH                                    2.62hours   0.91hours
  Day 2:
    1  ClevelandOH        PittsburghPA       ClevelandOH_tofrom_PittsburghPA_on_I76                          2.05hours   0.61hours
    2  PittsburghPA       ColumbusOH         ColumbusOH_tofrom_PittsburghPA_on_I70E                          2.85hours   0.71hours
    3  ColumbusOH         IndianapolisIN     Indianapolis_tofrom_Columbus                                    2.71hours   0.54hours
  Day 3:
    1  IndianapolisIN     CincinnatiOH       Cincinnati_tofrom_Indianapolis                                  1.72hours   0.39hours
    2  CincinnatiOH       LouisvilleKY       Cincinnati_tofrom_Lousville                                     1.54hours   0.55hours
    3  LouisvilleKY       LexingtonKY        Louisville_tofrom_Lexington                                     1.22hours   0.77hours
    4  LexingtonKY        KnoxvilleTN        Knoxville_tofrom_Lexington                                      2.62hours   0.42hours
  Day 4:
    1  KnoxvilleTN        ChattanoogaTN      Knoxville_tofrom_Chattanooga                                    1.72hours   0.59hours
    2  ChattanoogaTN      McMinnvilleTN      McMinnville_tofrom_Chattanooga_on_I24E                          1.14hours   0.66hours
    3  McMinnvilleTN      NashvilleTN        McMinnville_tofrom_Nashville_onI_24E                            1.18hours   0.82hours
    4  NashvilleTN        MetropolisIL       Metropolis_tofrom_Nashville_on_I24E                             2.28hours   0.43hours
  Day 5:
    1  MetropolisIL       StLouisMO          StLouis_tofrom_Metropolis_on_I57_and_I64                        2.57hours   0.40hours
    2  StLouisMO          SpringfieldIL      StLouis_tofrom_Springfield                                      1.51hours   0.39hours
    3  SpringfieldIL      ChicagoIL          Chicago_tofrom_Springfield                                      3.08hours   1.00hours
2221.0 total miles  5 days  44.34 total hours  Total Themes satisfied: 25
```

## Test Cases

Some test cases are already given, but you are welcomed to create you own. To use, simple use pipeline in linux terminal like
``` 
python3 main.py Locations_large_1.csv Edges_large_1.csv output.txt NashvilleTN < test1
```

For test cases that has a larger number of days/hours (e.g., 30 days / 12 hours), the program may run very slow