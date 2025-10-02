# Assignment 5

used : 
```bash
(head -n 1 data/311_Service_Requests_from_2010_to_Present.csv && awk -F',' '$2 ~ /2024/' data/311_Service_Requests_from_2010_to_Present.csv) > data/2024_incidents.csv 
```
 to get only the 2024 incidents